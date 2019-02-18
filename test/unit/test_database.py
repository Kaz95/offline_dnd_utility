import unittest
import mock
import database


class TestDatabase(unittest.TestCase):

    # def test_create_connection(self):
        # self.assertIsNotNone(create_connection(':memory:'))

    def test_create_connection(self):
        with mock.patch('database.sqlite3.connect') as mocksql:
            mocksql.return_value = 'Success'
            self.assertEqual(database.create_connection(':memory:'), 'Success')


if __name__ == '__main__':
    unittest.main()

