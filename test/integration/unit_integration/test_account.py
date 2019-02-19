import unittest
import mock
import account
import database
import sql


class TestAccount(unittest.TestCase):

    def test_user_creates_account(self):
        with mock.patch('database.sqlite3') as mocksql:
            conn = mocksql.connect()
            username = 'kaz'
            password = 'pass'
            account.user_creates_account(conn, username, password)
            mocksql.connect().cursor().execute.assert_called_with(sql.sql_add_account_row(), ('kaz', 'pass'))

    def test_load_account_archive(self):
        with mock.patch('database.sqlite3') as mocksql:
            conn = mocksql.connect()
            mocksql.connect().cursor().fetchall.return_value = [(1, 2), (2, 3), (3, 4)]
            account.load_account_archive(conn)
            self.assertEqual(account.Account.log_in_dic, {1: 2, 2: 3, 3: 4})

    def test_log_in(self):
        with mock.patch('database.sqlite3') as mocksql:
            conn = mocksql.connect()
            username = 'kaz'
            password = 'pass'
            mocksql.connect().cursor().fetchall.return_value = [(2, 3), (username, password), (3, 4)]
            self.assertEqual(account.log_in(conn, username, password), username)

    def test_load_account_object(self):
        with mock.patch('database.sqlite3') as mocksql:
            conn = mocksql.connect()
            mocksql.connect().cursor().fetchone.return_value = (1, 'kaz', 'pass')
            fake_acc = account.Account(1, 'kaz', 'pass')
            username = 'kaz'
            real_acc = account.load_account_object(conn, username)
            self.assertEqual(fake_acc.id, real_acc.id)
            self.assertEqual(fake_acc.name, real_acc.name)
            self.assertEqual(fake_acc.password, real_acc.password)

