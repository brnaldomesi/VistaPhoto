import os
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.files.images import ImageFile
from django.core.urlresolvers import reverse
from PIL import Image
from faker import Factory

from app.models import Photo


class TestBaseClass(TestCase):
	"""Base class for all the tests in this app."""

	def setUp(self):
		"""Create objects which will be used throughout the tests."""
		self.client = Client()
		self.fake = Factory.create()
		self.username = self.fake.user_name()
		self.password = self.fake.password()
		self.user = User.objects.create_user(
			username=self.username,
			password=self.password
		)
		self.test_image = Image.new(mode='L', size=(400, 576), color=0)
		self.test_image.save('test.jpg')

	def tearDown(self):
		"""Destroy resources after they have been used in the tests."""
		del self.fake
		self.user.delete()
		# delete all Photo objects (In the process, deletes all edits, previews
		# and all associated files on disk )
		Photo.objects.all().delete()

		del self.test_image
		# delete image created during setUp
		if os.path.exists('test.jpg'):
			os.remove('test.jpg')
		self.logout_user()

	def login_user(self):
		"""Authenticate 'self.user'."""
		url = reverse('rest_framework:login')
		data = {
			'username': self.username,
			'password': self.password
		}
		self.client.post(url, data=data)

	def logout_user(self):
		"""Send get request to '/logout/' url to logout authenticated users.
		"""
		url = reverse('rest_framework:logout')
		self.client.get(url)

	def uploadable_image(self):
		"""Create an uploadable object from the 'test.jpg' file on disk."""
		f = open('test.jpg', 'rb')
		imf = ImageFile(f)
		return imf
