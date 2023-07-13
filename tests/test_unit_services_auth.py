import unittest
import asyncio

from src.services.auth import auth  # Import the function we want to test

class TestAuthService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('Start before all test')

    @classmethod
    def tearDownClass(cls):
        print('End after all test')
        
    def setUp(self):
        print('Start before each test')
        
    def tearDown(self):
        print('End after each test')
        
    def test_get_email_from_token(self, token):
        print('Test get_email_from_token')
        self.assertEqual(auth.get_email_from_token(token), None)    


if __name__ == '__main__':
    unittest.main()