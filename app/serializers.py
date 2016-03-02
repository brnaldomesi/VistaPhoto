from rest_framework import serializers

from .models import Photo

class PhotoSerializer(serializers.ModelSerializer):
	"""Serialize the Photo model and also specify the Photo model fields to be
	returned to the user/ to be expected of the user."""

	class Meta:
		model = Photo
		fields = ('photo_id', 'path',)