import os

from django.conf import settings
from django.core.urlresolvers import reverse
from .test_base import TestBaseClass
from app.models import Preview, Photo


class TestPhotoEffects(TestBaseClass):
    """Test the '/api/preview/' url."""

    def test_successful_post(self):
        """Test successful POST on '/api/preview/' url."""
        # build the url
        url = reverse('preview-list')
        # authenticate a user
        self.login_user()
        # create a Photo object (the Preview's foreign key)
        photo_url = reverse('photo-list')
        data = {
            'path': self.uploadable_image(),
            'filter_effects': 'BLUR'
        }
        self.client.post(photo_url, data)
        # get the Photo's id to use when creating a Preview
        response = self.client.get(photo_url)
        photo_id = response.data[0].get('photo_id')
        # now create the Preview
        data = {
            'photo': photo_id
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.status_text, 'Created')
        self.assertTrue('Success' in response.data.get('status'))

    def test_unsuccessful_post_non_existent_fk(self):
        """Test a POST on '/api/preview' with an ID of a non-existent Photo"""
        url = reverse('preview-list')
        self.login_user()
        data = {
            'photo': 3457
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.status_text, 'Bad Request')
        self.assertTrue('Invalid pk' in response.data.get('photo')[0])

    def test_successful_get(self):
        """Test successful GET on '/api/preview/' url."""
        self.login_user()
        # create a photo and get the photo (whose id is used as a fk)
        photo_url = reverse('photo-list')
        data = {
            'path': self.uploadable_image(),
            'filter_effects': 'BLUR'
        }
        self.client.post(photo_url, data=data)
        response = self.client.get(photo_url)
        photo_id = response.data[0].get('photo_id')
        # use the photo
        data = {
            'photo': photo_id
        }
        url = reverse('preview-list')
        response = self.client.post(url, data=data)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.status_text, 'OK')
        # assert that 6 previews have been created
        self.assertEqual(len(response.data), 6)

    def test_successful_delete(self):
        """TesT successful DELETE on '/api/preview/' url."""
        # build the URL
        url = reverse('preview-list')
        # authenticate user
        self.login_user()
        # Create a Photo (the foreign key to a preview)
        photo_url = reverse('photo-list')
        data = {
            'path': self.uploadable_image(),
            'filter_effects': 'BLUR'
        }
        self.client.post(photo_url, data)
        # get the photo's id to use when creating a preview
        response = self.client.get(photo_url)
        photo_id = response.data[0].get('photo_id')
        # use the photo id to create a preview
        data = {
            'photo': photo_id
        }
        self.client.post(url, data=data)
        # retrieve the preview id in index 0
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

