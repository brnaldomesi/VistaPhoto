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
			photo = Photo(**serializer.validated_data)
			photo.owner = current_user
			photo.save()
			return Response(
				{
					'status': 'Success',
					'message': 'Photo uploaded'
				}, status=status.HTTP_201_CREATED
			)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
