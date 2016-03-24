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

    # def test_authenticated_post(self):
    #     """Test authenticateed POST request to '/api/edit/' route.
    #     """
    #     url = '/api/edit/'

    #     # authenticate
    #     self.login_user()
    #     # create a photo
    #     photo =

    #     response = self.client.post(url)
    #     self.assertEqual(403, response.status_code)
    #     self.assertEqual('Forbidden', response.status_text)
