import json

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from .test_base import TestBaseClass
from app.models import Photo


class TestPhotoEditsURL(TestBaseClass):
    """Test the '/api/edit/' Django route.
    """

    def test_authenticated_get(self):
        """Test an authenticated GET request to '/api/edit/' route.
        """
        url = reverse('edit-list')

        # authenticate the user
        self.login_user()
        # attemot the get
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        self.assertEqual('OK', response.status_text)

    def test_unauthenticated_get(self):
        """Test unauthenticateed GET request to '/api/edit/' route.
        """
        url = reverse('edit-list')

        response = self.client.get(url)
        self.assertEqual(403, response.status_code)
        self.assertEqual('Forbidden', response.status_text)
        self.assertTrue(
            'credentials were not provided.' in response.data.get('detail'))

    def test_access_permissions(self):
        """Test permissions to '/api/edit/:edit_id/'.

        Test access to a photoedit that was created by another user.
        """
        # create a photo under user1 and get the photo id

        self.login_user()
        data = {
            'path': self.uploadable_image(),
            'filter_effects': 'BLUR'
        }
        photo_url = reverse('photo-list')
        response = self.client.post(photo_url, data=data)
        response = self.client.get(photo_url)
        photo_id = response.data[0].get('photo_id')
        # user1 edits the photo
        photo_url += str(photo_id) + '/'
        data = {
            'filter_effects': self.get_random_filter()
        }
        json_data = json.dumps(data)
        response = self.client.put(
            photo_url, data=json_data, content_type='application/json')
        # get the photoedit id
        url = reverse('edit-list')
        response = self.client.get(url)
        edit_id = response.data[0].get('photo_edit_id')
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
        # attempt to access edit route as user2
        url += str(edit_id) + '/'
        response = self.client.get(url)
        self.assertTrue(
            'You do not have permission' in response.data.get('detail'))
        self.assertEqual(403, response.status_code)
        self.assertEqual('Forbidden', response.status_text)
