import unittest
from search import search
# tests will live here once day. I promise


class TestSearch(unittest.TestCase):
    def test_search(self):
        result = search('Club')
        self.assertEqual(result, ['Club', 'http://www.dnd5eapi.co/api/equipment/1'])
# if __name__ == '__main__':
#     unittest.main()
