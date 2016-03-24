from .test_base import TestBaseClass


class TestRootURL(TestBaseClass):
    """Test the '/' Django route.
    """

    def test_get(self):
        """Test a successful GET request to '/' route.
        """
        response = self.client.get('/')
        self.assertEqual(200, response.status_code)
