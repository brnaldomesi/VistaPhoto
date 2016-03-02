from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Photo(models.Model):
	"""Photo ORM model."""
	path = models.FileField()
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
