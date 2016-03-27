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
	"""Photo ORM model.
	"""
	photo_id = models.AutoField(primary_key=True)
	path = models.ImageField(upload_to='photo/')
	owner = models.ForeignKey(User, on_delete=models.CASCADE)

	@staticmethod
	def use_effect(effect, photo_edit):
		"""Modifies an image with the specified effect.
		"""
		if effect in FILTERS:
			photo = Image.open(photo_edit.upload)
			photo = photo.filter(FILTERS.get(effect))

			photo.save(photo_edit.upload.url[1:])

	def get_file_name(self):
		"""Returns the name of the file that this model is associated with.
		"""
		return self.path.name[6:]

	def __str__(self):
		"""Customize representation of this model's instance.
		"""
		return '{0}'.format(self.path.name[2:])


class PhotoEdit(models.Model):
	"""Associate edits on Photo with this model.
	"""
	photo_edit_id = models.AutoField(primary_key=True)
	effect_name = models.CharField(max_length=20)
	photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
	upload = models.ImageField(upload_to='edits/')

	def get_file_name(self):
		"""Returns the name of the file that this model is associated with.
		"""
		return self.upload.name[6:]

	def __str__(self):
		"""Customize representation of this model's instance.
		"""
		return '{0}'.format(self.effect_name)


class Preview(models.Model):
	"""Preview ORM to generate previews of effects on Photo.
	"""
	preview_id = models.AutoField(primary_key=True)
	preview_name = models.CharField(max_length=20)
	path = models.ImageField(upload_to='preview/')
	photo = models.ForeignKey(Photo, on_delete=models.CASCADE)

	def use_effect(self):
		"""Apply the effect that corresponds to current value of 'self.effect_name'
		in the FILTERS dictionary.
		"""
		if self.preview_name in FILTERS:
			photo = Image.open(self.path.url[1:])
			preview = photo.filter(FILTERS.get(self.preview_name))
			preview.save(self.path.url[1:])

	def save(self, *args, **kwargs):
		"""Apply the effects to the file on disk whenever model.save() is called.

		This method is called after save because the 'path' attribute will refer
		to 'MEDIA_ROOT' until the model instance is saved. After saving, it refers
		to 'MEDIA_ROOT/preview/' (which is where we want effects to be uploaded
		when applying effect previews).
		"""
		super(Preview, self).save(*args, **kwargs)
		self.use_effect()

	def __str__(self):
		"""Customize representation of this model's instance.
		"""
		return '{0}'.format(self.path.name[8:], )


class SocialAuthUsersocialauth(models.Model):
	"""
	A read only ORM to query information that is populated by python-social-auth
	in the 'social_auth_usersocialauth' table.
	"""
	id = models.IntegerField(primary_key=True)
	provider = models.CharField(max_length=32)
	uid = models.CharField(max_length=255)
	extra_data = models.TextField()
	user = models.ForeignKey(User, models.DO_NOTHING)

	class Meta:
		managed = False
		db_table = 'social_auth_usersocialauth'
		unique_together = (('provider', 'uid'),)

	def __str__(self):
		"""Customize representation of this model's instance.
		"""
		return '{0}{1}'.format(self.user.username, self.provider)


@receiver(post_delete, sender=Preview)
def file_cleanup(sender, **kwargs):
	"""This method deletes associated 'Preview' files on disk every time 'delete()'
	is called on a model instance (or on a queryset of 'Preview' objects).
	"""

	instance = kwargs.get('instance')
	filename = instance.path.url[1:]
	if os.path.exists(filename):
		os.remove(filename)


@receiver(post_delete, sender=Photo)
def file_cleanup(sender, **kwargs):
	"""This method deletes associated 'Photo' files on disk every time 'delete()'
	is called on a model instance (or on a queryset of 'Photo' objects).
	"""
	instance = kwargs.get('instance')
	filename = instance.path.url[1:]
	if os.path.exists(filename):
		os.remove(filename)


@receiver(post_delete, sender=PhotoEdit)
def file_cleanup(sender, **kwargs):
	"""This method deletes associated 'PhotoEdit' files on disk every time 'delete()'
	is called on a model instance (or on a queryset of 'PhotoEdit' objects).
	"""
	instance = kwargs.get('instance')
	filename = instance.upload.url[1:]
	if os.path.exists(filename):
		os.remove(filename)
