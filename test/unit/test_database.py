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

    def test_add_account_row(self):
        with mock.patch('database.sqlite3') as mocksql:
            conn = mocksql.connect()
            self.assertEqual(database.add_account_row(conn, [1, 2]), """INSERT INTO accounts (username, password)
            VALUES(?,?)""")

    def test_add_inventory_row(self):
        with mock.patch('database.sqlite3') as mocksql:
            conn = mocksql.connect()
            self.assertEqual(database.add_inventory_row(conn, [1, 2, 3]), """INSERT INTO inventories (account_id, character_id, name)
            VALUES(?,?,?)""")

    def test_add_character_row(self):
        with mock.patch('database.sqlite3') as mocksql:
            conn = mocksql.connect()
            self.assertEqual(database.add_character_row(conn, [1, 2, 3]), """INSERT INTO characters (account_id, name, currency)
            VALUES(?,?,?)""")

    def test_add_item_row(self):
        with mock.patch('database.sqlite3') as mocksql:
            conn = mocksql.connect()
            self.assertEqual(database.add_item_row(conn, [1, 2, 3, 4, 5, 6]), """INSERT INTO items (account_id, character_id, inventory_id, item, api, quantity)
            VALUES(?,?,?,?,?,?)""")

    def test_add_store_item(self):
        with mock.patch('database.sqlite3') as mocksql:
            conn = mocksql.connect()
            self.assertEqual(database.add_store_item(conn, [1, 2, 3]), """INSERT INTO items (item, api, store)
             VALUES(?,?,?)""")


if __name__ == '__main__':
    unittest.main()

