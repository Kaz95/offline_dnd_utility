import unittest
import mock
import setup


class TestSetup(unittest.TestCase):

    def test_wrong_schema(self):
        with mock.patch('setup.sqlite3') as mocksql:
            mocksql.connect().cursor().fetchall.return_value = ['accounts', 'characters', 'inventories', 'items']
            self.assertFalse(setup.wrong_schema())
