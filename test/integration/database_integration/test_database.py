import unittest
import database
import sql
import setup
# import os
db = 'C:\\sqlite\\db\\test.db'
mem = ':memory:'


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
        self.item1 = [1, 1, 1, 'Club', 'http://www.dnd5eapi.co/api/equipment/1', 1]
        self.item2 = [1, 1, 1, 'Dagger', 'http://www.dnd5eapi.co/api/equipment/2', 1]
        self.item3 = [2, 2, 2, 'Greatclub', 'http://www.dnd5eapi.co/api/equipment/3', 1]
        self.item4 = [2, 2, 2, 'Handaxe', 'http://www.dnd5eapi.co/api/equipment/4', 1]
        self.item5 = [2, 2, 2, 'Javelin', 'http://www.dnd5eapi.co/api/equipment/5', 1]
        self.item6 = [2, 3, 3, 'Light hammer', 'http://www.dnd5eapi.co/api/equipment/6', 1]
        self.item7 = [2, 3, 3, 'Mace', 'http://www.dnd5eapi.co/api/equipment/7', 1]
        sql.execute_sql(self.conn, sql.sql_add_account_row(), self.account1[0], self.account1[1])
        sql.execute_sql(self.conn, sql.sql_add_account_row(), self.account2[0], self.account2[1])
        sql.execute_sql(self.conn, sql.sql_add_character_row(), self.player1[0], self.player1[1], self.player1[2])
        sql.execute_sql(self.conn, sql.sql_add_character_row(), self.player2[0], self.player2[1], self.player2[2])
        sql.execute_sql(self.conn, sql.sql_add_character_row(), self.player3[0], self.player3[1], self.player3[2])
        sql.execute_sql(self.conn, sql.sql_add_inventory_row(), self.inventory1[0], self.inventory1[1], self.inventory1[2])
        sql.execute_sql(self.conn, sql.sql_add_inventory_row(), self.inventory2[0], self.inventory2[1], self.inventory2[2])
        sql.execute_sql(self.conn, sql.sql_add_inventory_row(), self.inventory3[0], self.inventory3[1], self.inventory3[2])
        sql.execute_sql(self.conn, sql.sql_add_item_row(), self.item1[0], self.item1[1], self.item1[2], self.item1[3], self.item1[4], self.item1[5])
        sql.execute_sql(self.conn, sql.sql_add_item_row(), self.item2[0], self.item2[1], self.item2[2], self.item2[3], self.item2[4], self.item2[5])
        sql.execute_sql(self.conn, sql.sql_add_item_row(), self.item3[0], self.item3[1], self.item3[2], self.item3[3], self.item3[4], self.item3[5])
        sql.execute_sql(self.conn, sql.sql_add_item_row(), self.item4[0], self.item4[1], self.item4[2], self.item4[3], self.item4[4], self.item4[5])
        sql.execute_sql(self.conn, sql.sql_add_item_row(), self.item5[0], self.item5[1], self.item5[2], self.item5[3], self.item5[4], self.item5[5])
        sql.execute_sql(self.conn, sql.sql_add_item_row(), self.item6[0], self.item6[1], self.item6[2], self.item6[3], self.item6[4], self.item6[5])
        sql.execute_sql(self.conn, sql.sql_add_item_row(), self.item7[0], self.item7[1], self.item7[2], self.item7[3], self.item7[4], self.item7[5])

    def tearDown(self):
        self.conn.close()
        # os.remove('C:\\sqlite\\db\\test.db')

    def test_queries(self):
        self.assertEqual(sql.execute_fetchone_sql(self.conn, sql.sql_username_password()), ('acc1', 'pass1'))
        self.assertEqual(sql.execute_fetchone_sql(self.conn, sql.sql_account_row(), self.account2[0]), (2, 'acc2', 'pass2'))
        self.assertEqual(sql.execute_fetchone_sql(self.conn, sql.sql_character_row(), self.player2[1]), (2, 'char2', 5000))
        self.assertEqual(sql.execute_fetchone_sql(self.conn, sql.sql_inventory_row(), self.inventory1[2]), (1, 'inv1'))
        self.assertEqual(sql.execute_fetchall_sql(self.conn, sql.sql_all_characters(), self.player2[0]), [('char2', 5000), ('char3', 5000)])
        self.assertEqual(sql.execute_fetchall_sql(self.conn, sql.sql_accounts_with_characters()), [(1,), (2,)])
        self.assertEqual(sql.execute_fetchall_sql(self.conn, sql.sql_characters_with_inventories()), [(1,), (2,), (3,)])
        self.assertEqual(sql.execute_fetchall_sql(self.conn, sql.sql_characters_inventory_ids(), 1), [(1,)])
        self.assertEqual(sql.execute_fetchall_sql(self.conn, sql.sql_all_inventory_names(), 1), [('inv1',)])
        self.assertEqual(sql.execute_fetchall_sql(self.conn, sql.sql_query_accounts_with_characters()), [(1,), (2,)])

    def test_delete(self):
        sql.execute_sql(self.conn, sql.sql_delete('items', 'character_id'), 1)
        self.assertEqual(database.count_rows(self.conn, sql.sql_count_rows(), 'items'), (261,))
