import unittest
import database
import sql
import setup
# import os
db = 'C:\\sqlite\\db\\test.db'
mem = ':memory:'
# TODO: This is not working whatsoever, will update_progressbar once bugs are fixed and reviewing code.


# TODO: Works fine with mem DB, not fine with test DB.
class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.conn = database.create_connection(mem)
        setup.create_schema(self.conn)
        self.assertFalse(setup.wrong_schema(self.conn))
        setup.stock_stores(self.conn)

        self.account1 = ['acc1', 'pass1']
        self.account2 = ['acc2', 'pass2']
        self.player1 = [1, 'char1', 5000]
        self.player2 = [2, 'char2', 5000]
        self.player3 = [2, 'char3', 5000]
        self.inventory1 = [1, 1, 'inv1']
        self.inventory2 = [2, 2, 'inv2']
        self.inventory3 = [2, 3, 'inv3']
        self.item1 = [1, 1, 1, 'Club', 'http://www.dnd5eapi.co/api/equipment/1', 0, 1]
        self.item2 = [1, 1, 1, 'Dagger', 'http://www.dnd5eapi.co/api/equipment/2', 0, 1]
        self.item3 = [2, 2, 2, 'Greatclub', 'http://www.dnd5eapi.co/api/equipment/3', 0, 1]
        self.item4 = [2, 2, 2, 'Handaxe', 'http://www.dnd5eapi.co/api/equipment/4', 0, 1]
        self.item5 = [2, 2, 2, 'Javelin', 'http://www.dnd5eapi.co/api/equipment/5', 0, 1]
        self.item6 = [2, 3, 3, 'Light hammer', 'http://www.dnd5eapi.co/api/equipment/6', 0, 1]
        self.item7 = [2, 3, 3, 'Mace', 'http://www.dnd5eapi.co/api/equipment/7', 0, 1]
        sql.execute_sql(self.conn, sql.add_account_row(), self.account1[0], self.account1[1])
        sql.execute_sql(self.conn, sql.add_account_row(), self.account2[0], self.account2[1])
        sql.execute_sql(self.conn, sql.add_character_row(), self.player1[0], self.player1[1], self.player1[2])
        sql.execute_sql(self.conn, sql.add_character_row(), self.player2[0], self.player2[1], self.player2[2])
        sql.execute_sql(self.conn, sql.add_character_row(), self.player3[0], self.player3[1], self.player3[2])
        sql.execute_sql(self.conn, sql.add_inventory_row(), self.inventory1[0], self.inventory1[1], self.inventory1[2])
        sql.execute_sql(self.conn, sql.add_inventory_row(), self.inventory2[0], self.inventory2[1], self.inventory2[2])
        sql.execute_sql(self.conn, sql.add_inventory_row(), self.inventory3[0], self.inventory3[1], self.inventory3[2])
        sql.execute_sql(self.conn, sql.add_item_row(), self.item1[0], self.item1[1], self.item1[2], self.item1[3], self.item1[4], self.item1[5], self.item1[6])
        sql.execute_sql(self.conn, sql.add_item_row(), self.item2[0], self.item2[1], self.item2[2], self.item2[3], self.item2[4], self.item2[5], self.item2[6])
        sql.execute_sql(self.conn, sql.add_item_row(), self.item3[0], self.item3[1], self.item3[2], self.item3[3], self.item3[4], self.item3[5], self.item3[6])
        sql.execute_sql(self.conn, sql.add_item_row(), self.item4[0], self.item4[1], self.item4[2], self.item4[3], self.item4[4], self.item4[5], self.item4[6])
        sql.execute_sql(self.conn, sql.add_item_row(), self.item5[0], self.item5[1], self.item5[2], self.item5[3], self.item5[4], self.item5[5], self.item5[6])
        sql.execute_sql(self.conn, sql.add_item_row(), self.item6[0], self.item6[1], self.item6[2], self.item6[3], self.item6[4], self.item6[5], self.item6[6])
        sql.execute_sql(self.conn, sql.add_item_row(), self.item7[0], self.item7[1], self.item7[2], self.item7[3], self.item7[4], self.item7[5], self.item7[6])

    def tearDown(self):
        self.conn.close()
        # os.remove('C:\\sqlite\\db\\test.db')

    def test_queries(self):
        self.assertEqual(sql.execute_fetchone_sql(self.conn, sql.query_username_password()), ('acc1', 'pass1'))
        self.assertEqual(sql.execute_fetchone_sql(self.conn, sql.query_account_row(), self.account2[0]), (2, 'acc2', 'pass2'))
        self.assertEqual(sql.execute_fetchone_sql(self.conn, sql.query_character_row(), self.player2[1]), (2, 'char2', 5000))
        self.assertEqual(sql.execute_fetchone_sql(self.conn, sql.query_inventory_row(), self.inventory1[2]), (1, 'inv1'))
        self.assertEqual(sql.execute_fetchall_sql(self.conn, sql.query_all_characters(), self.player2[0]), [(2, 'char2', 5000), (3, 'char3', 5000)])
        self.assertEqual(sql.execute_fetchall_sql(self.conn, sql.query_accounts_with_characters()), [(1,), (2,)])
        self.assertEqual(sql.execute_fetchall_sql(self.conn, sql.query_characters_with_inventories()), [(1,), (2,), (3,)])
        self.assertEqual(sql.execute_fetchall_sql(self.conn, sql.query_characters_inventory_ids(), 1), [(1,)])
        self.assertEqual(sql.execute_fetchall_sql(self.conn, sql.query_all_inventory_names(), 1), [('inv1',)])
        self.assertEqual(sql.execute_fetchall_sql(self.conn, sql.sql_query_accounts_with_characters()), [(1,), (2,)])

    def test_delete(self):
        sql.execute_sql(self.conn, sql.delete_all('items', 'character_id'), 1)
        self.assertEqual(database.count_rows(self.conn, sql.count_table_rows(), 'items'), (261,))
