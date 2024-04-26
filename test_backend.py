import unittest
from app import app

class TestBackend(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_user_repos_route(self):
        response = self.app.get('/api/repos/username')
        self.assertEqual(response.status_code, 200)
        # Add more assertions based on expected response data

if __name__ == '__main__':
    unittest.main()
