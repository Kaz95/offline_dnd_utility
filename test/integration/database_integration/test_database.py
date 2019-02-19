import unittest
import database
import account
import player
import inventory
import sql
import setup
import sqlite3


# TODO: Write some tests that use actual (in memory) database

class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.conn = database.create_connection(':memory:')
        setup.create_schema(self.conn)
        self.assertFalse(setup.wrong_schema(self.conn))
        setup.stock_stores(self.conn)
        # account1 = {'user': 'acc1', 'pass': 'pass1'}
        # account2 = {'user': 'acc2', 'pass': 'pass2'}
        # player1 = {'acc_id': 1, 'name': 'char1', 'currency': 5000}
        # player2 = {'acc_id': 2, 'name': 'char2', 'currency': 5000}
        # player3 = {'acc_id': 2, 'name': 'char3', 'currency': 5000}
        # inventory1 = {'acc_id': 1, 'char_id': 1, 'name': 'inv1'}
        # inventory2 = {'acc_id': 2, 'char_id': 2, 'name': 'inv2'}
        # inventory3 = {'acc_id': 2, 'char_id': 3, 'name': 'inv3'}
        # item1 = {'acc_id': 1, 'char_id': 1, 'inv_id': 1, 'item': 'Club', 'api': 'http://www.dnd5eapi.co/api/equipment/1', 'quant': 1}
        # item2 = {'acc_id': 1, 'char_id': 1, 'inv_id': 1, 'item': 'Dagger', 'api': 'http://www.dnd5eapi.co/api/equipment/2', 'quant': 1}
        # item3 = {'acc_id': 2, 'char_id': 2, 'inv_id': 2, 'item': 'Greatclub', 'api': 'http://www.dnd5eapi.co/api/equipment/3', 'quant': 1}
        # item4 = {'acc_id': 2, 'char_id': 2, 'inv_id': 2, 'item': 'Handaxe', 'api': 'http://www.dnd5eapi.co/api/equipment/4', 'quant': 1}
        # item5 = {'acc_id': 2, 'char_id': 2, 'inv_id': 2, 'item': 'Javelin', 'api': 'http://www.dnd5eapi.co/api/equipment/5', 'quant': 1}
        # item6 = {'acc_id': 2, 'char_id': 3, 'inv_id': 3, 'item': 'Light hammer', 'api': 'http://www.dnd5eapi.co/api/equipment/6', 'quant': 1}
        # item7 = {'acc_id': 2, 'char_id': 3, 'inv_id': 3, 'item': 'Mace', 'api': 'http://www.dnd5eapi.co/api/equipment/7', 'quant': 1}
        account1 = ['acc1', 'pass1']
        account2 = ['acc2', 'pass2']
        player1 = [1, 'char1', 5000]
        player2 = [2, 'char2', 5000]
        player3 = [2, 'char3', 5000]
        inventory1 = [1, 1,'inv1']
        inventory2 = [2, 2, 'inv2']
        inventory3 = [2, 3, 'inv3']
        item1 = [1, 1, 1, 'Club', 'http://www.dnd5eapi.co/api/equipment/1', 1]
        item2 = [1, 1, 1, 'Dagger', 'http://www.dnd5eapi.co/api/equipment/2', 1]
        item3 = [2, 2, 2, 'Greatclub', 'http://www.dnd5eapi.co/api/equipment/3', 1]
        item4 = [2, 2, 2, 'Handaxe', 'http://www.dnd5eapi.co/api/equipment/4', 1]
        item5 = [2, 2, 2, 'Javelin', 'http://www.dnd5eapi.co/api/equipment/5', 1]
        item6 = [2, 3, 3, 'Light hammer', 'http://www.dnd5eapi.co/api/equipment/6', 1]
        item7 = [2, 3, 3, 'Mace', 'http://www.dnd5eapi.co/api/equipment/7', 1]
        sql.execute_sql(self.conn, sql.sql_add_account_row(), account1[0], account1[1])
        sql.execute_sql(self.conn, sql.sql_add_account_row(), account2[0], account2[1])
        sql.execute_sql(self.conn, sql.sql_add_character_row(), player1[0], player1[1], player1[2])
        sql.execute_sql(self.conn, sql.sql_add_character_row(), player2[0], player2[1], player2[2])
        sql.execute_sql(self.conn, sql.sql_add_character_row(), player3[0], player3[1], player3[2])
        sql.execute_sql(self.conn, sql.sql_add_inventory_row(), inventory1[0], inventory1[1], inventory1[2])
        sql.execute_sql(self.conn, sql.sql_add_inventory_row(), inventory2[0], inventory2[1], inventory2[2])
        sql.execute_sql(self.conn, sql.sql_add_inventory_row(), inventory3[0], inventory3[1], inventory3[2])
        sql.execute_sql(self.conn, sql.sql_add_item_row(), item1[0], item1[1], item1[2], item1[3], item1[4], item1[5])
        sql.execute_sql(self.conn, sql.sql_add_item_row(), item2[0], item2[1], item2[2], item2[3], item2[4], item2[5])
        sql.execute_sql(self.conn, sql.sql_add_item_row(), item3[0], item3[1], item3[2], item3[3], item3[4], item3[5])
        sql.execute_sql(self.conn, sql.sql_add_item_row(), item4[0], item4[1], item4[2], item4[3], item4[4], item4[5])
        sql.execute_sql(self.conn, sql.sql_add_item_row(), item5[0], item5[1], item5[2], item5[3], item5[4], item5[5])
        sql.execute_sql(self.conn, sql.sql_add_item_row(), item6[0], item6[1], item6[2], item6[3], item6[4], item6[5])
        sql.execute_sql(self.conn, sql.sql_add_item_row(), item7[0], item7[1], item7[2], item7[3], item7[4], item7[5])

    def test_queries(self):
        self.assertEqual(sql.execute_fetchone_sql(self.conn, sql.sql_username_password()), ('acc1', 'pass1'))
