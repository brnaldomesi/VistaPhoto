from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Photo(models.Model):
	"""Photo ORM model."""
	photo_id = models.AutoField(primary_key=True)
	path = models.ImageField()
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
