import unittest
from unittest.mock import patch
from database import create_connection, execute_fetchall_sql, execute_fetchone_sql
from database import sql_username_password, sql_account_row, sql_accounts_with_characters, sql_all_characters
from database import sql_all_inventories, sql_character_row, sql_characters_with_inventories, sql_inventory_row
from database import add_account_row, add_inventory_row, add_item_row, add_character_row, add_store_item


class TestDatabase(unittest.TestCase):

    # def test_create_connection(self):
        # self.assertIsNotNone(create_connection(':memory:'))

    def test_create_connection(self):
        with patch('database.sqlite3.connect') as mocksql:
            mocksql.return_value = 'Success'
            self.assertEqual(create_connection(':memory:'), 'Success')

    def test_execute_fetchall_sql(self):
        with patch('database.sqlite3') as mocksql:
            conn = mocksql.connect()
            mocksql.connect().cursor().fetchall.return_value = 'Success'
            response = execute_fetchall_sql(conn, """SELECT username, password FROM accounts;""")
            self.assertEqual(response, 'Success')

    def test_execute_fetchone_sql(self):
        with patch('database.sqlite3') as mocksql:
            conn = mocksql.connect()
            mocksql.connect().cursor().fetchone.return_value = 'Success'
            response = execute_fetchone_sql(conn, """SELECT username, password FROM accounts;""")
            self.assertEqual(response, 'Success')

    def test_sql_username_password(self):
        self.assertEqual(sql_username_password(), """SELECT username, password FROM accounts;""")

    def test_sql_account_row(self):
        self.assertEqual(sql_account_row(), """SELECT id, username, password FROM accounts WHERE username = ?;""")

    def test_sql_character_row(self):
        self.assertEqual(sql_character_row(), """SELECT id, name, currency FROM characters WHERE name = ?;""")

    def test_sql_inventory_row(self):
        self.assertEqual(sql_inventory_row(), """SELECT id, name FROM inventories WHERE name = ?;""")

    def test_sql_all_characters(self):
        self.assertEqual(sql_all_characters(), """SELECT name, currency FROM characters WHERE account_id = ?;""")

    def test_sql_accounts_with_characters(self):
        self.assertEqual(sql_accounts_with_characters(), """SELECT DISTINCT account_id FROM characters;""")

    def test_sql_characters_with_inventories(self):
        self.assertEqual(sql_characters_with_inventories(), """SELECT DISTINCT character_id FROM inventories;""")

    def test_sql_all_inventories(self):
        self.assertEqual(sql_all_inventories(), """SELECT name FROM inventories WHERE character_id = ?;""")

    def test_add_account_row(self):
        with patch('database.sqlite3') as mocksql:
            conn = mocksql.connect()
            self.assertEqual(add_account_row(conn, [1, 2]), """INSERT INTO accounts (username, password)
            VALUES(?,?)""")

    def test_add_inventory_row(self):
        with patch('database.sqlite3') as mocksql:
            conn = mocksql.connect()
            self.assertEqual(add_inventory_row(conn, [1, 2]), """INSERT INTO inventories (character_id, name)
            VALUES(?,?)""")

    def test_add_character_row(self):
        with patch('database.sqlite3') as mocksql:
            conn = mocksql.connect()
            self.assertEqual(add_character_row(conn, [1, 2, 3]), """INSERT INTO characters (account_id, name, currency)
            VALUES(?,?,?)""")

    def test_add_item_row(self):
        with patch('database.sqlite3') as mocksql:
            conn = mocksql.connect()
            self.assertEqual(add_item_row(conn, [1, 2, 3, 4]), """INSERT INTO items (inventory_id, item, api, quantity)
            VALUES(?,?,?,?)""")

    def test_add_store_item(self):
        with patch('database.sqlite3') as mocksql:
            conn = mocksql.connect()
            self.assertEqual(add_store_item(conn, [1, 2, 3]), """INSERT INTO items (item, api, store)
             VALUES(?,?,?)""")

    def test_create_schema(self):
        self.assertEqual(print(1), 2)


if __name__ == '__main__':
    unittest.main()

