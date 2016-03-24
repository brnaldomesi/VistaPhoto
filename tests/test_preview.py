import os

from django.conf import settings
from django.core.urlresolvers import reverse
from .test_base import TestBaseClass
from app.models import Preview


class TestPhotoEffects(TestBaseClass):
	"""Test the '/api/preview/' url."""

	def tearDown(self):
		"""Delete all Effects objects.

		(To clean up associated effect files on disk).
		"""
		all_previews = Preview.objects.all()
		all_previews.delete()

	def test_successful_post(self):
		"""Test successful POST on '/api/preview/' url."""
		url = reverse('preview-list')
		self.login_user()
		data = {
			'path': self.uploadable_image(),
			'preview_name': 'BLUR'
		}
		response = self.client.post(url, data=data)
		self.assertEqual(response.status_code, 201)
		self.assertEqual(response.status_text, 'Created')
		self.assertTrue('Success' in response.data.get('status'))

	def test_successful_get(self):
		"""Test successful GET on '/api/preview/' url."""
		url = reverse('preview-list')
		self.login_user()
		data = {
			'path': self.uploadable_image()
		}
		self.client.post(url, data=data)
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.status_text, 'OK')

	def test_successful_delete(self):
		"""TesT successful DELETE on '/api/preview/' url."""
		url = reverse('preview-list')
		self.login_user()
		data = {
			'path': self.uploadable_image()
		}
		self.client.post(url, data=data)
		# retrieve the effect's id
		response = self.client.get(url)
		effect_id = response.data[0].get('preview_id')
		# get the file name from an effect object's path attribute
		effect_obj = Preview.objects.get(pk=effect_id)
		filename = settings.BASE_DIR + effect_obj.path.url
		# send a delete request
		url += str(effect_id) + '/'
		# confirm the file has been created in the system
		self.assertTrue(os.path.exists(filename))
		response = self.client.delete(url)
		self.assertEqual(response.status_code, 204)
		self.assertEqual(response.status_text, 'No Content')
		# confirm the file has been deleted from the system (when the delete
		# request was sent)
		self.assertFalse(os.path.exists(filename))

