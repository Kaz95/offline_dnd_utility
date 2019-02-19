import unittest
import mock
import database
import sql


class TestDatabase(unittest.TestCase):

    def test_add_account_row(self):
        with mock.patch('database.sqlite3') as mocksql:
            some_account = {'user': 'kaza', 'pass': 'tree'}
            conn = mocksql.connect()
            database.add_account_row(conn, sql.sql_add_account_row(), some_account)
            mocksql.connect().cursor().execute.assert_called_with(sql.sql_add_account_row(), ('kaza', 'tree'))

    def test_add_inventory_row(self):
        with mock.patch('database.sqlite3') as mocksql:
            some_inventory = {'acc_id': 1, 'char_id': 1, 'name': 'inv name'}
            conn = mocksql.connect()
            database.add_inventory_row(conn, sql.sql_add_inventory_row(), some_inventory)
            mocksql.connect().cursor().execute.assert_called_with(sql.sql_add_inventory_row(), (1, 1, 'inv name'))

    def test_add_item_row(self):
        with mock.patch('database.sqlite3') as mocksql:
            some_item = {'acc_id': 1, 'char_id': 1, 'inv_id': 1, 'item': 'item name', 'api': 'api url', 'quant': 1}
            conn = mocksql.connect()
            database.add_item_row(conn, sql.sql_add_item_row(), some_item)
            mocksql.connect().cursor().execute.assert_called_with(sql.sql_add_item_row(), (1, 1, 1, 'item name',
                                                                                           'api url', 1))

    def test_add_character_row(self):
        with mock.patch('database.sqlite3') as mocksql:
            some_character = {'acc_id': 1, 'name': 'char name', 'currency': 5000}
            conn = mocksql.connect()
            database.add_character_row(conn, sql.sql_add_character_row(), some_character)
            mocksql.connect().cursor().execute.assert_called_with(sql.sql_add_character_row(), (1, 'char name', 5000))

    def test_add_store_item(self):
        with mock.patch('database.sqlite3') as mocksql:
            some_item = {'item': 'club', 'api': 'some api', 'store': 'bs'}
            conn = mocksql.connect()
            database.add_store_item(conn, sql.sql_add_store_item(), some_item)
            mocksql.connect().cursor().execute.assert_called_with(sql.sql_add_store_item(),
                                                                  ('club', 'some api', 'bs'))

    def test_query_accounts_with_characters(self):
        with mock.patch('database.sqlite3') as mocksql:
            conn = mocksql.connect()
            mocksql.connect().cursor().fetchall.return_value = [(1,), (2,), (3,)]
            returned_list = database.query_accounts_with_characters(conn, sql.sql_query_accounts_with_characters())
            self.assertEqual(returned_list, [1, 2, 3])

    def test_count_rows(self):
        with mock.patch('database.sqlite3') as mocksql:
            conn = mocksql.connect()
            mocksql.connect().cursor().fetchone.return_value = (256,)
            count = database.count_rows(conn, sql.sql_count_rows(), 'items')
            mocksql.connect().cursor().execute.assert_called_with('SELECT count(*) FROM items;', ())
            self.assertEqual(count, (256,))
