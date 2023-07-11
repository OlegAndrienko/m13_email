import asyncio
import unittest

from src.services.email import send_email # Import the function we want to test

async def async_send_email(email: str, username: str, host: str):
    await send_email(email, username, host)
    return True

class TestEmailService(unittest.TestCase):
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
        
    async def test_send_email(self):
        print('Test send_email')
        self.assertEqual(send_email('   ', '    ', '    '), None)
        
        


if __name__ == '__main__':
    unittest.main()