import unittest
import mock
import sql


class TestSQL(unittest.TestCase):

    def test_execute_fetchall_sql(self):
        with mock.patch('sql.sqlite3') as mocksql:
            conn = mocksql.connect()
            mocksql.connect().cursor().fetchall.return_value = 'Success'
            response = sql.execute_fetchall_sql(conn, """SELECT username, password FROM accounts;""")
            self.assertEqual(response, 'Success')

    def test_execute_fetchone_sql(self):
        with mock.patch('sql.sqlite3') as mocksql:
            conn = mocksql.connect()
            mocksql.connect().cursor().fetchone.return_value = 'Success'
            response = sql.execute_fetchone_sql(conn, """SELECT username, password FROM accounts;""")
            self.assertEqual(response, 'Success')

    def test_sql_accounts_table(self):
        self.assertEqual(sql.sql_accounts_table(), """CREATE TABLE IF NOT EXISTS accounts (
               id integer PRIMARY KEY,
               username varchar NOT NULL,
               password varchar NOT NULL);""")

    def test_sql_characters_table(self):
        self.assertEqual(sql.sql_characters_table(), """CREATE TABLE IF NOT EXISTS characters (
               id integer PRIMARY KEY,
               account_id integer,
               name text,
               currency integer,
               FOREIGN KEY (account_id) REFERENCES accounts (id));""")

    def test_sql_inventories_table(self):
        self.assertEqual(sql.sql_inventories_table(), """CREATE TABLE IF NOT EXISTS inventories (
               id integer PRIMARY KEY,
               character_id integer,
               name text,
               FOREIGN KEY (character_id) REFERENCES characters (id));""")

    def test_sql_items_table(self):
        self.assertEqual(sql.sql_items_table(), """CREATE TABLE IF NOT EXISTS items (
               id integer PRIMARY KEY,
               inventory_id integer,
               item text,
               api varchar,
               quantity integer,
               store text,
               FOREIGN KEY (inventory_id) REFERENCES inventories (id));""")

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
        self.assertEqual(sql.sql_all_inventory_names(),
                         """SELECT name FROM inventories WHERE character_id = ?;""")

    def test_sql_query_accounts_with_characters(self):
        self.assertEqual(sql.sql_query_accounts_with_characters(),
                         """SELECT DISTINCT account_id FROM characters;""")
