from rest_framework import serializers

from .models import Photo


class PhotoSerializer(serializers.ModelSerializer):
	"""Serialize the Photo model and also specify the Photo model fields to be
	returned to the user (or to be expected of the user)."""
	file_url = serializers.CharField(source='path.url', read_only=True)
	filter_effects = serializers.ChoiceField(
		['BLUR', 'EMBOSS', 'DETAIL', 'CONTOUR', 'SMOOTH', 'SHARPEN'],
		write_only=True,
		allow_null=True
	)

	class Meta:
		model = Photo
		fields = ('photo_id', 'path', 'file_url', 'filter_effects',)
