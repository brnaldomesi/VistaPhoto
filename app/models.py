from __future__ import unicode_literals

import os

from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_delete
from django.contrib.auth.models import User

from PIL import Image, ImageFilter


# Associate filter strings from viewsets to ImageFilter effects
FILTERS = {
	'BLUR': ImageFilter.BLUR,
	'EMBOSS': ImageFilter.EMBOSS,
	'DETAIL': ImageFilter.DETAIL,
	'CONTOUR': ImageFilter.CONTOUR,
	'SMOOTH': ImageFilter.SMOOTH,
	'SHARPEN': ImageFilter.SHARPEN
}


class Photo(models.Model):
	"""Photo ORM model."""
	photo_id = models.AutoField(primary_key=True)
	path = models.ImageField()
	owner = models.ForeignKey(User, on_delete=models.CASCADE)

	def use_effect(self, effect):
		"""Modifies an image with the specified effect."""
		if effect in FILTERS:
			photo = Image.open(self.path)
			photo = photo.filter(FILTERS.get(effect))

			photo.save(self.path.url[1:])

	def get_file_name(self):
		"""Returns the name of the file that this model is associated with."""
		return self.path.name[2:]


def effects_file_name(instance, filename):
	"""Return upload path to be used in path attribute of Effects model."""
	filetime = instance.file_name + instance.effect_name
	return 'effects/{0}'.format(filetime + '.jpg')


# Create your models here.
class Effects(models.Model):
	"""Photo edit effects preview ORM."""
	effect_id = models.AutoField(primary_key=True)
	effect_name = models.CharField(max_length=20)
	file_name = models.CharField(max_length=50)
	path = models.ImageField(upload_to=effects_file_name)

	def use_effect(self):
		"""Apply the effect that corresponds to current value of 'self.effect_name'
		in the FILTERS dictionary.
		"""
		if self.effect_name in FILTERS:
			photo = Image.open(self.path)
			preview = photo.filter(FILTERS.get(self.effect_name))
			preview.save(self.path.url[1:])

	def save(self, *args, **kwargs):
		"""Apply the effects to the file on disk whenever model.save() is called."""
		super(Effects, self).save(*args, **kwargs)
		# This method is called after save because the 'path' attribute will refer
		# to 'MEDIA_ROOT' until the model instance is saved. After saving, it refers
		#  to 'MEDIA_ROOT/effects/' (which is where we want effects to be uploaded
		# when applying effect previews)
		self.use_effect()


@receiver(post_delete, sender=Effects)
def file_cleanup(sender, **kwargs):
	"""This method deletes associated photo files on disk every time 'delete()'
	is called on a model instance (or on a queryset of Effect objects).
	"""
	instance = kwargs.get('instance')
	filename = instance.path.url[1:]
	if os.path.exists(filename):
			os.remove(filename)
