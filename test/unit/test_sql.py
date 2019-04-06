import unittest
import mock
import sql


class TestSQL(unittest.TestCase):

    def test_execute_sql(self):
        with mock.patch('sql.sqlite3') as mocksql:
            conn = mocksql.connect()
            call = """some sql"""
            sql.execute_sql(conn, call)
            mocksql.connect().execute.assert_called_with(call, ())

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
        self.assertEqual(sql.create_accounts_table(), """CREATE TABLE IF NOT EXISTS accounts (
               id integer PRIMARY KEY,
               username varchar NOT NULL,
               password varchar NOT NULL);""")

    def test_sql_characters_table(self):
        self.assertEqual(sql.create_characters_table(), """CREATE TABLE IF NOT EXISTS characters (
               id integer PRIMARY KEY,
               account_id integer,
               name text,
               currency integer,
               FOREIGN KEY (account_id) REFERENCES accounts (id));""")

    def test_sql_inventories_table(self):
        self.assertEqual(sql.create_inventories_table(), """CREATE TABLE IF NOT EXISTS inventories (
               id integer PRIMARY KEY,
               account_id integer,
               character_id integer,
               name text,
               FOREIGN KEY (account_id) REFERENCES accounts (id),
               FOREIGN KEY (character_id) REFERENCES characters(id));""")

    def test_sql_items_table(self):
        self.assertEqual(sql.create_items_table(), """CREATE TABLE IF NOT EXISTS items (
               id integer PRIMARY KEY,
               account_id,
               character_id,
               inventory_id integer,
               item text,
               api varchar,
               unit_value,
               quantity integer,
               store text,
               FOREIGN KEY (account_id) REFERENCES accounts (id),
               FOREIGN KEY (character_id) REFERENCES characters (id),
               FOREIGN KEY (inventory_id) REFERENCES inventories (id));""")

    def test_sql_username_password(self):
        self.assertEqual(sql.query_username_password(),
                         """SELECT username, password FROM accounts;""")

    def test_sql_account_row(self):
        self.assertEqual(sql.query_account_row(),
                         """SELECT id, username, password FROM accounts WHERE username = ?;""")

    def test_sql_character_row(self):
        self.assertEqual(sql.query_character_row(),
                         """SELECT id, name, currency FROM characters WHERE name = ?;""")

    def test_sql_inventory_row(self):
        self.assertEqual(sql.query_inventory_row(),
                         """SELECT id, name FROM inventories WHERE name = ?;""")

    def test_sql_all_characters(self):
        self.assertEqual(sql.query_all_characters(),
                         """SELECT id, name, currency FROM characters WHERE account_id = ?;""")

    def test_sql_accounts_with_characters(self):
        self.assertEqual(sql.query_accounts_with_characters(),
                         """SELECT DISTINCT account_id FROM characters;""")

    def test_sql_characters_with_inventories(self):
        self.assertEqual(sql.query_characters_with_inventories(),
                         """SELECT DISTINCT character_id FROM inventories;""")

    def test_all_inventory_names(self):
        self.assertEqual(sql.query_all_inventory_names(),
                         """SELECT name FROM inventories WHERE character_id = ?;""")

    def test_sql_query_accounts_with_characters(self):
        self.assertEqual(sql.query_accounts_with_characters(),
                         """SELECT DISTINCT account_id FROM characters;""")

    def test_sql_delete(self):
        self.assertEqual(sql.delete_all('items', 'character_id'),
                         """DELETE FROM items WHERE character_id = ?""")

    def test_sql_query_items_in_inventory(self):
        self.assertEqual(sql.query_items_in_inventory(),
                         """SELECT item, quantity FROM items WHERE inventory_id = ?""")

    def test_sql_item_quantity(self):
        self.assertEqual(sql.query_item_quantity(),
                         """SELECT quantity FROM items where item = ? AND inventory_id = ?""")

    def test_sql_delete_item(self):
        self.assertEqual(sql.delete_item(),
                         """DELETE FROM items WHERE item = ? AND inventory_id = ?""")

    def test_sql_add_item_row(self):
        self.assertEqual(sql.add_item_row(),
                         """INSERT INTO items (account_id, character_id, inventory_id, item, api, unit_value, quantity)
            VALUES(?,?,?,?,?,?,?)""")

    def test_sql_add_account_row(self):
        self.assertEqual(sql.add_account_row(),
                         """INSERT INTO accounts (username, password)
            VALUES(?,?)""")

    def test_sql_add_inventory_row(self):
        self.assertEqual(sql.add_inventory_row(),
                         """INSERT INTO inventories (account_id, character_id, name)
            VALUES(?,?,?)""")

    def test_sql_add_character_row(self):
        self.assertEqual(sql.add_character_row(),
                         """INSERT INTO characters (account_id, name, currency)
            VALUES(?,?,?)""")

    def test_sql_add_store_item(self):
        self.assertEqual(sql.add_store_item(),
                         """INSERT INTO items (item, api, unit_value, store)
             VALUES(?,?,?,?)""")

    def test_sql_count_rows(self):
        self.assertEqual(sql.count_table_rows(),
                         """SELECT count(*) FROM {};""")

    def test_update_quantity(self):
        self.assertEqual(sql.update_quantity(),
                         """UPDATE items SET quantity = ? WHERE item = ? AND character_id = ?""")

