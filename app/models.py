from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from PIL import Image, ImageFilter


# Create your models here.
class Photo(models.Model):
	"""Photo ORM model."""
	photo_id = models.AutoField(primary_key=True)
	path = models.ImageField()
	owner = models.ForeignKey(User, on_delete=models.CASCADE)

	# Associate filter strings from viewsets to ImageFilter effects
	FILTERS = {
		'BLUR': ImageFilter.BLUR,
		'EMBOSS': ImageFilter.EMBOSS,
		'DETAIL': ImageFilter.DETAIL,
		'CONTOUR': ImageFilter.CONTOUR,
		'SMOOTH': ImageFilter.SMOOTH,
		'SHARPEN': ImageFilter.SHARPEN
	}

	def use_effect(self, effect):
		"""Modifies an image with the specified effect."""
		if effect in self.FILTERS:
			photo = Image.open(self.path)
			photo = photo.filter(self.FILTERS.get(effect))

			photo.save(self.path.url[1:])
