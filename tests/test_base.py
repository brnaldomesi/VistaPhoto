import os
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.files.images import ImageFile
from PIL import Image
from faker import Factory


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
		del self.test_image
		if os.path.exists('test.jpg'):
			os.remove('test.jpg')

	def login_user(self):
		"""Authenticate 'self.user'."""
		url = '/api-auth/login/'
		data = {
			'username': self.username,
			'password': self.password
		}
		self.client.post(url, data=data)

	def uploadable_image(self):
		"""Create an uploadable object from the 'test.jpg' file on disk."""
		f = open('test.jpg', 'rb')
		imf = ImageFile(f)
		return imf
