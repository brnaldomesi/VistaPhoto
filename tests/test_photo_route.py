from random import random
from .test_base import TestBaseClass
from app.models import FILTERS, Photo


class TestPhotoAPIRoute(TestBaseClass):
	"""Test the '/api/photos/' url."""

	def get_random_filter(self):
		"""Return a random filter effect to use on photo."""
		filters = FILTERS.keys()
		rand_index = int(random() * len(filters))
		return filters[rand_index]

	def test_successful_upload(self):
		"""Test successful POST request to '/api/photos/' url."""
		url = '/api/photos/'
		# authenticate the user
		self.login_user()
		# attempt upload
		data = {
			'path': self.uploadable_image(),
			'filter_effects': 'BLUR'
		}
		response = self.client.post(url, data=data)
		self.assertEqual(response.status_code, 201)
		self.assertEqual(response.status_text, 'Created')
		self.assertTrue(
			'Success' in response.data.get('status')
		)

	def test_unauthenticated_upload(self):
		"""Test unauthenticated POST request to '/api/photos/' url."""
		url = '/api/photos/'
		# attempt upload
		data = {
			'path': self.uploadable_image(),
			'filter_effects': 'BLUR'
		}
		response = self.client.post(url, data=data)
		self.assertEqual(response.status_code, 403)
		self.assertEqual(response.status_text, 'Forbidden')
		self.assertTrue(
			'credentials were not provided' in response.data.get('detail')
		)

	def test_upload_no_photo_selected(self):
		"""Test authenticated POST request to '/api/photos/' url when no upload
		photo has been specified.
		"""
		url = '/api/photos/'
		# authenticate the user
		self.login_user()
		# attempt upload
		data = {
			'filter_effects': 'BLUR'
		}
		response = self.client.post(url, data=data)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.status_text, 'Bad Request')
		self.assertTrue(
			'No file was submitted' in response.data.get('path')[0]
		)

	def test_upload_no_effect_specified(self):
		"""Test authenticated POST request to '/api/photos/' url when no effect
		has been specified.
		"""
		url = '/api/photos/'
		# authenticate the user
		self.login_user()
		# attempt upload
		data = {
			'path': self.uploadable_image()
		}
		response = self.client.post(url, data=data)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.status_text, 'Bad Request')
		self.assertTrue(
			'This field is required' in response.data.get('filter_effects')[0]
		)

	def test_delete_upload(self):
		"""Test successful DELETE to '/api/photos/'."""
		url = '/api/photos/'
		self.login_user()
		data = {
			'path': self.uploadable_image(),
			'filter_effects': 'BLUR'
		}
		response = self.client.post(url, data=data)
		self.assertTrue(response.status_code, 201)
		response = self.client.get(url)
		photo_id = response.data[0].get('photo_id')
		url += str(photo_id) + '/'
		response = self.client.delete(url)
		self.assertEqual(response.status_code, 204)
		self.assertEqual(response.status_text, 'No Content')
		all_photos = Photo.objects.all()
		self.assertEqual(len(all_photos), 0)

	def test_image_effect(self):
		"""Test successful PUT to '/api/photos/' url."""
		pass
		# url = '/api/photos/'
		# self.login_user()
		# # create a photo
		# data = {
		# 	'path': self.uploadable_image(),
		# 	'filter_effects': 'BLUR'
		# }
		# self.client.post(url, data=data)
		# # fetch photo id
		# response = self.client.get(url)
		# photo_id = response.data[0].get('photo_id')
		# url += str(photo_id) + '/'

		# selected_effect = {
		# 	'filter_effects': self.get_random_filter()
		# }
		# response = self.client.put(url, data=selected_effect)
		# import ipdb; ipdb.set_trace()
		# login
		# post a photo
		# fetch its id
		# create url
		# send a PUT
		# assert results

