import os

from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core.files import File
from django.core.files.uploadedfile import InMemoryUploadedFile

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from faker import Factory

from .serializers import PhotoSerializer, EffectSerializer, PhotoEditSerializer
from .models import Photo, Effects, FILTERS, PhotoEdit
from .permissions import IsOwner


class EffectViewSet(viewsets.ModelViewSet):
	"""Handle CRUD requests to '/effects/' url."""
	queryset = Effects.objects.all()
	serializer_class = EffectSerializer
	permission_classes = (permissions.IsAuthenticated, )

	def create(self, request):
		"""Use specified effect on the uploaded photo."""
		upload = request.data.get('path')
		data = {}
		fake = Factory.create()
		filename = fake.word()

		if isinstance(upload, InMemoryUploadedFile):
			data['path'] = upload
		elif isinstance(str(upload), str):
			file_object = open(upload[1:])
			django_file = File(file_object)
			data['path'] = django_file

		serializer = self.serializer_class(data=data)

		if serializer.is_valid():
			# delete all pre_existing effects objects
			self.queryset.delete()

			for key in FILTERS:
				effects = Effects(
					path=serializer.validated_data.get('path'),
					effect_name=key,
					file_name=filename
				)
				effects.save()
			return Response(
				{
					'status': 'Success',
					'message': 'Thumbnails created'
				}, status=status.HTTP_201_CREATED
			)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PhotoViewSet(viewsets.ModelViewSet):
	"""Handle CRUD requests to '/photos/' url."""
	queryset = Photo.objects.all().order_by('-photo_id')
	serializer_class = PhotoSerializer
	permission_classes = (permissions.IsAuthenticated, IsOwner)

	def get_queryset(self):
		"""Customize get_queryset method.

		Override this method to provide both retrieve and list views to user
		without a problem. Problem being anticipated here is as a result of
		overriding 'get_object' below (whose purpose is to apply IsOwner permissions
		on this viewset.)
		"""
		if self.kwargs.get('pk'):
			return Photo.objects.filter(pk=self.kwargs.get('pk'))
		return self.queryset.filter(owner=self.request.user)

	def get_object(self):
		"""Override this method so that IsOwner permissions can be applied.

		Override this method so as to call 'check_object_permissions' for IsOwner
		permissions to be applied.
		"""
		obj = get_object_or_404(self.get_queryset())
		self.check_object_permissions(self.request, obj)
		return obj

	def create(self, request):
		"""POST photos with the currently logged in user being the owner."""
		serializer = self.serializer_class(data=request.data)
		if serializer.is_valid():
			current_user = request.user
			photo = Photo(path=serializer.validated_data.get('path'))
			photo.owner = current_user
			photo.save()
			return Response(
				{
					'status': 'Success',
					'message': 'Photo uploaded'
				}, status=status.HTTP_201_CREATED
			)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def update(self, request, pk):
		"""Handle application of effects/filters on images when user clicks."""
		# import ipdb; ipdb.set_trace()
		try:
			photo = Photo.objects.get(pk=pk)
			photo_edit = PhotoEdit(photo=photo)
			file_photo = open(photo.path.url[1:], 'rb')
			photo_edit.upload.save(photo.get_file_name(), File(file_photo), save=True)
			photo_edit.save()
			# apply request if it has been requested
			effect = request.data.get('filter_effects')
			if effect:
				photo.use_effect(effect, photo_edit)
				# photo.save()
				return Response(
					{
						'status': 'Photo Updated',
						'message': 'Photo Updated'
					}, status=status.HTTP_200_OK
				)
			return Response(
				{
					'status': 'Photo not updated',
					'message': 'No image effect specified'
				}, status=status.HTTP_400_BAD_REQUEST
			)
		except Photo.DoesNotExist:
			return Response(
				{
					'detail': 'Not found.'
				}, status=status.HTTP_404_NOT_FOUND
			)

	def destroy(self, request, pk):
		"""Delete record from database as well as file photo on disk."""
		photo = Photo.objects.get(pk=pk)
		if photo:
			filename = settings.BASE_DIR + photo.path.url
			photo.delete()
			if os.path.exists(filename):
				os.remove(filename)
				return Response({}, status=status.HTTP_204_NO_CONTENT)
			return Response(
				{
					'detail': 'Photo file not found.'
				}, status=status.HTTP_404_NOT_FOUND
			)
		return Response(
			{
				'detail': 'Not found.'
			}, status=status.HTTP_404_NOT_FOUND
		)


class PhotoEditViewSet(viewsets.ModelViewSet):
	"""Viewset to handle CRUD requests to '/api/edit/'.
	"""
	queryset = PhotoEdit.objects.all()
	serializer_class = PhotoEditSerializer