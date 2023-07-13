import unittest
import asyncio

from src.database import db

class TestDatabase(unittest.TestCase):
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
        
    async def test_get_db(self):
        print('Test get_db')
        self.assertEqual(db.get_db(), None)
        
if __name__ == '__main__':
    unittest.main()
    
    