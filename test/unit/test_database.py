import unittest
import mock
import database
import sql


class TestDatabase(unittest.TestCase):

    # def test_create_connection(self):
        # self.assertIsNotNone(create_connection(':memory:'))

    def test_create_connection(self):
        with mock.patch('database.sqlite3.connect') as mocksql:
            mocksql.return_value = 'Success'
            self.assertEqual(database.create_connection(':memory:'), 'Success')


# TODO: Need to mock these connections in sql now....I think
class TestDatabaseUnitIntegration(unittest.TestCase):

    def test_add_account_row(self):
        with mock.patch('database.sqlite3') as mocksql:
            some_account = {'username': 'kaza', 'password': 'tree'}
            conn = mocksql.connect()
            database.add_account_row(conn, sql.add_account_row(), some_account)
            mocksql.connect().execute.assert_called_with(sql.add_account_row(), ('kaza', 'tree'))

    def test_add_character_row(self):
        with mock.patch('database.sqlite3') as mocksql:
            some_character = {'acc_id': 1, 'name': 'char name', 'currency': 5000}
            conn = mocksql.connect()
            database.add_character_row(conn, sql.add_character_row(), some_character)
            mocksql.connect().execute.assert_called_with(sql.add_character_row(), (1, 'char name', 5000))

    def test_add_inventory_row(self):
        with mock.patch('database.sqlite3') as mocksql:
            some_inventory = {'acc_id': 1, 'char_id': 1, 'name': 'inv name'}
            conn = mocksql.connect()
            database.add_inventory_row(conn, sql.add_inventory_row(), some_inventory)
            mocksql.connect().execute.assert_called_with(sql.add_inventory_row(), (1, 1, 'inv name'))

    def test_add_item_row(self):
        with mock.patch('database.sqlite3') as mocksql:

            some_item = {'acc_id': 1,
                         'char_id': 1,
                         'inv_id': 1,
                         'item': 'item name',
                         'api': 'api url',
                         'value': 1,
                         'quantity': 1}

            conn = mocksql.connect()
            database.add_item_row(conn, sql.add_item_row(), some_item)
            mocksql.connect().execute.assert_called_with(sql.add_item_row(), (1, 1, 1, 'item name',
                                                                                           'api url', 1, 1))

    def test_add_store_item(self):
        with mock.patch('database.sqlite3') as mocksql:
            some_item = {'item': 'club', 'api': 'some api', 'store': 'bs', 'currency': 1}
            conn = mocksql.connect()
            database.add_store_item_p1(conn, sql.add_store_item_p1(), some_item)
            mocksql.connect().execute.assert_called_with(sql.add_store_item_p1(),
                                                         ('club', 'some api', 1, 'bs'))

    def test_count_rows(self):
        with mock.patch('database.sqlite3') as mocksql:
            conn = mocksql.connect()
            mocksql.connect().cursor().fetchone.return_value = (256,)
            count = database.count_rows(conn, sql.count_table_rows(), 'items')
            mocksql.connect().cursor().execute.assert_called_with('SELECT count(*) FROM items;', ())
            self.assertEqual(count, 256)

    def test_query_accounts_with_characters(self):
        with mock.patch('database.sqlite3') as mocksql:
            conn = mocksql.connect()
            mocksql.connect().cursor().fetchall.return_value = [(1,), (2,), (3,)]
            returned_list = database.query_accounts_with_characters(conn, sql.query_accounts_with_characters())
            self.assertEqual(returned_list, [1, 2, 3])

    def test_delete_item(self):
        with mock.patch('database.sqlite3') as mocksql:
            conn = mocksql.connect()
            database.delete_item(conn, 'Club', 1)
            mocksql.connect().execute.assert_called_with(sql.delete_item(), ('Club', 1))

    def test_delete_all_character_items(self):
        with mock.patch('database.sqlite3') as mocksql:
            conn = mocksql.connect()
            database.delete_all_character_items(conn, 1)
            mocksql.connect().execute.assert_called_with(sql.delete_all('items', 'character_id'), (1,))

    def test_delete_character_inventories(self):
        with mock.patch('database.sqlite3') as mocksql:
            conn = mocksql.connect()
            database.delete_character_inventories(conn, 1)
            mocksql.connect().execute.assert_called_with(sql.delete_all('inventories', 'character_id'),
                                                                  (1,))

    def test_item_in_inventory_add(self):
        with mock.patch('database.sqlite3') as mocksql:
            conn = mocksql.connect()
            mocksql.connect().cursor().fetchall.return_value = [('Club', '1'), ('Dagger', '1')]
            database.in_inventory(conn, 1, 'Dagger', '+')
            mocksql.connect().execute.assert_called_with(sql.update_quantity(), (2, 'Dagger', 1))

    def test_item_in_inventory_minus(self):
        with mock.patch('database.sqlite3') as mocksql:
            conn = mocksql.connect()
            mocksql.connect().cursor().fetchall.return_value = [('Club', '3'), ('Dagger', '2')]
            database.in_inventory(conn, 1, 'Club', '-')
            mocksql.connect().execute.assert_called_with(sql.update_quantity(), (2, 'Club', 1))


if __name__ == '__main__':
    unittest.main()

