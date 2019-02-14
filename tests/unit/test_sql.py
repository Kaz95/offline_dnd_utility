import unittest
from unittest.mock import patch
import sql


class TestSQL(unittest.TestCase):

    def test_execute_fetchall_sql(self):
        with patch('database.sqlite3') as mocksql:
            conn = mocksql.connect()
            mocksql.connect().cursor().fetchall.return_value = 'Success'
            response = sql.execute_fetchall_sql(conn, """SELECT username, password FROM accounts;""")
            self.assertEqual(response, 'Success')

    def test_execute_fetchone_sql(self):
        with patch('database.sqlite3') as mocksql:
            conn = mocksql.connect()
            mocksql.connect().cursor().fetchone.return_value = 'Success'
            response = sql.execute_fetchone_sql(conn, """SELECT username, password FROM accounts;""")
            self.assertEqual(response, 'Success')

    def test_sql_username_password(self):
        self.assertEqual(sql.sql_username_password(),
                         """SELECT username, password FROM accounts;""")

    def test_sql_account_row(self):
        self.assertEqual(sql.sql_account_row(),
                         """SELECT id, username, password FROM accounts WHERE username = ?;""")

    def test_sql_character_row(self):
        self.assertEqual(sql.sql_character_row(),
                         """SELECT id, name, currency FROM characters WHERE name = ?;""")

    def test_sql_inventory_row(self):
        self.assertEqual(sql.sql_inventory_row(),
                         """SELECT id, name FROM inventories WHERE name = ?;""")

    def test_sql_all_characters(self):
        self.assertEqual(sql.sql_all_characters(),
                         """SELECT name, currency FROM characters WHERE account_id = ?;""")

    def test_sql_accounts_with_characters(self):
        self.assertEqual(sql.sql_accounts_with_characters(),
                         """SELECT DISTINCT account_id FROM characters;""")

    def test_sql_characters_with_inventories(self):
        self.assertEqual(sql.sql_characters_with_inventories(),
                         """SELECT DISTINCT character_id FROM inventories;""")

    def test_sql_all_inventories(self):
        self.assertEqual(sql.sql_all_inventories(),
                         """SELECT name FROM inventories WHERE character_id = ?;""")
