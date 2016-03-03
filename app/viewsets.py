from django.shortcuts import get_object_or_404

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from .serializers import PhotoSerializer
from .models import Photo


class PhotoViewSet(viewsets.ModelViewSet):
	"""Handle CRUD requests to '/photos/' url."""
	queryset = Photo.objects.all()
	serializer_class = PhotoSerializer
	permission_classes = (permissions.IsAuthenticated,)

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

	def retrieve(self, request, pk):
		"""Handle requests to get an upload. Also set the effects on thumbnails
		of available effects when a photo is clicked."""
		try:
			queryset = Photo.objects.filter(photo_id=pk)
			photo = get_object_or_404(queryset)
			serializer = PhotoSerializer(photo)
			return Response(serializer.data, status=status.HTTP_200_OK)
		except Photo.DoesNotExist:
			return Response(
				{
					'detail': 'Not found.'
				}, status=status.HTTP_404_NOT_FOUND
			)

	def update(self, request, pk):
		"""Handle application of effects/filters on images when user clicks."""
		try:
			photo = Photo.objects.get(pk=pk)
			# apply request if it has been requested
			effect = request.data.get('filter_effects')
			if effect:
				photo.use_effect(effect)
				photo.save()
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
