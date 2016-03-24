from .test_base import TestBaseClass


class TestUserAuthenticated(TestBaseClass):
    """Test the '/login/status/' Django route.
    """

    def test_authenticated_get(self):
        """Test an authenticated GET request to '/login/status/' route.
        """
        self.login_user()
        response = self.client.get('/api/login/status/')
        self.assertEqual(200, response.status_code)
        self.assertEqual('OK', response.status_text)
        self.assertTrue(
            'authenticated via Django' in response.data.get('status')
        )

    def test_unauthenticated_get(self):
        """Test an unauthenticated GET request to '/login/status/' route.
        """

        response = self.client.get('/api/login/status/')
        self.assertEqual(401, response.status_code)
        self.assertEqual('Unauthorized', response.status_text)
        self.assertTrue('notLoggedIn' in response.data.get('status'))
        self.assertNotEqual(200, response.status_code)

