import json
import os
from random import random

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.conf import settings

from .test_base import TestBaseClass
from app.models import FILTERS, Photo


class TestPhotoAPIRoute(TestBaseClass):
	"""Test the '/api/photo/' url."""

	def get_random_filter(self):
		"""Return a random filter effect to use on photo."""
		filters = list(FILTERS)
		rand_index = int(random() * len(filters))
		return filters[rand_index]

	def test_access_permissions(self):
		"""Test permissions to '/api/photo/:photo_id/'.

		Test access to a photo that was created by another user.
		"""
		url = reverse('photo-list')
		self.login_user()
		data = {
			'path': self.uploadable_image(),
			'filter_effects': 'BLUR'
		}
		# create a photo under user1 and get the photo id
		response = self.client.post(url, data=data)
		response = self.client.get(url)
		photo_id = response.data[0].get('photo_id')
		# logout user1
		self.logout_user()
		# create user2
		login_url = reverse('rest_framework:login')
		data = {
			'username': self.fake.user_name(),
			'password': self.fake.password()
		}
		user2 = User.objects.create_user(
			username=data.get('username'),
			password=data.get('password')
		)
		# login user2
		self.client.post(login_url, data=data)
		# attempt to access photo created earlier
		url += str(photo_id) + '/'
		response = self.client.get(url)
		self.assertTrue(
			'You do not have permission' in response.data.get('detail'))
		self.assertEqual(403, response.status_code)
		self.assertEqual('Forbidden', response.status_text)

	def test_successful_upload(self):
		"""Test successful POST request to '/api/photo/' url."""
		url = reverse('photo-list')
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
		"""Test unauthenticated POST request to '/api/photo/' url."""
		url = reverse('photo-list')
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

	def test_photo_detail_view(self):
		"""Test GET to '/api/photo/:photo_id/'."""
		# login a user
		self.login_user()
		# build url
		url = reverse('photo-list')
		# create a photo
		data = {
			'path': self.uploadable_image(),
			'filter_effects': 'BLUR'
		}
		self.client.post(url, data)
		# get the Photo's id
		response = self.client.get(url)
		photo_id = response.data[0].get('photo_id')
		# build the detail-view url
		url += str(photo_id) + '/'
		response = self.client.get(url)
		self.assertEqual(response.status_text, 'OK')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data.get('photo_id'), photo_id)

	def test_upload_no_photo_selected(self):
		"""Test authenticated POST request to '/api/photo/' url.

		Test this when no upload photo has been specified.
		"""
		url = reverse('photo-list')
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
		"""Test authenticated POST request to '/api/photo/' url.

		Test this when no effect has been specified.
		"""
		url = reverse('photo-list')
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
		"""Test successful DELETE to '/api/photo/'."""
		url = reverse('photo-list')
		self.login_user()
		data = {
			'path': self.uploadable_image(),
			'filter_effects': 'BLUR'
		}
		response = self.client.post(url, data=data)
		self.assertTrue(response.status_code, 201)
		response = self.client.get(url)
		photo_id = response.data[0].get('photo_id')
		file_url = response.data[0].get('file_url')
		filename = settings.BASE_DIR + file_url
		# Associated image file on disk exists before delete is called
		self.assertTrue(os.path.exists(filename))
		url += str(photo_id) + '/'
		response = self.client.delete(url)
		self.assertEqual(response.status_code, 204)
		self.assertEqual(response.status_text, 'No Content')
		all_photos = Photo.objects.all()
		self.assertEqual(len(all_photos), 0)
		# Associated image file has been deleted after DELETE request
		self.assertFalse(os.path.exists(filename))

	def test_delete_non_existent_photo_id(self):
		"""Test successful DELETE to '/api/photo/:photo_id'."""
		url = reverse('photo-list')
		self.login_user()
		# Random ID
		url += '67/'
		response = self.client.delete(url)
		self.assertEqual(response.status_code, 404)
		self.assertEqual(response.status_text, 'Not Found')
		self.assertTrue(
			'Not found' in response.data.get('detail'))

	def test_unauthenticated_put(self):
		"""Test an unauthenticated PUT request to '/api/photo/'.
		"""
		url = reverse('photo-list')
		# login
		self.login_user()
		# create a photo
		data = {
			'path': self.uploadable_image(),
			'filter_effects': 'BLUR'
		}
		response = self.client.post(url, data=data)
		# update it
		response = self.client.get(url)
		photo_id = response.data[0].get('photo_id')
		# logout
		self.logout_user()
		url += str(photo_id) + '/'

		data = {
			'photo_id': photo_id,
			'filter_effects': self.get_random_filter()
		}
		response = self.client.put(url, data=data)
		self.assertEqual(403, response.status_code)
		self.assertEqual('Forbidden', response.status_text)
		self.assertTrue(
			'credentials were not provided' in response.data.get('detail'))

	def test_authenticated_successful_put(self):
		"""Test an authenticated successful PUT request to '/api/photo/:photo_id/'.
		"""
		url = reverse('photo-list')
		# login
		self.login_user()
		# create a photo
		data = {
			'path': self.uploadable_image(),
			'filter_effects': 'BLUR'
		}
		response = self.client.post(url, data=data)
		# update it
		response = self.client.get(url)
		photo_id = response.data[0].get('photo_id')

		url += str(photo_id) + '/'
		data = {
			'filter_effects': self.get_random_filter()
		}
		# convert data to json and specify content_type as 'application/json'
		json_data = json.dumps(data)
		response = self.client.put(
			url, data=json_data, content_type='application/json')
		self.assertEqual(200, response.status_code)
		self.assertEqual('OK', response.status_text)
		self.assertEqual('Photo Updated', response.data.get('status'))

	def test_put_no_filter_effect_specified(self):
		"""Test a PUT request to '/api/photo/:photo_id/'.

		Test PUT request to '/api/photo/:photo_id/'' when no filter_effect has been
		specified.'
		"""
		url = reverse('photo-list')
		# login
		self.login_user()
		# create a photo
		data = {
			'path': self.uploadable_image(),
			'filter_effects': 'BLUR'
		}
		response = self.client.post(url, data=data)
		# update it
		response = self.client.get(url)
		photo_id = response.data[0].get('photo_id')

		url += str(photo_id) + '/'
		data = {
			'filter_effects': None
		}
		# convert data to json and specify content_type as 'application/json'
		json_data = json.dumps(data)
		response = self.client.put(
			url, data=json_data, content_type='application/json')

		self.assertEqual(400, response.status_code)
		self.assertEqual('Bad Request', response.status_text)
		self.assertTrue(
			'Photo not updated' in response.data.get('status'))

	def test_put_non_existent_photo_id(self):
		"""Test a PUT request to '/api/photo/:photo_id/'.

		Test PUT request to '/api/photo/:photo_id/' when invalid 'photo_id' is
		specified.'
		"""
		url = reverse('photo-list')
		# login
		self.login_user()
		# invalid photo_id (Not a special number, the first characters I typed
		# on keyboard)
		url += '6728/'

		data = {
			'filter_effects': self.get_random_filter()
		}
		# convert data to json and specify content_type as 'application/json'
		json_data = json.dumps(data)
		response = self.client.put(
			url, data=json_data, content_type='application/json')
		self.assertEqual(404, response.status_code)
		self.assertEqual('Not Found', response.status_text)
		self.assertTrue(
			'Not found' in response.data.get('detail'))