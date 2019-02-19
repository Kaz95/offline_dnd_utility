import sqlite3
from sqlite3 import Error
import sql
#
db = 'C:\\sqlite\\db\\test.db'
mem = ':memory:'


# Creates a connection to test.db
def create_connection(db_path):
    try:
        conn = sqlite3.connect(db_path)
        return conn
    except Error as e:
        print(e)
    return None


# Verifies store item count via sqlite count(*) method which returns row count for a given table.
# Not currently used.
# def wrong_item_count():
#     store_item_count = 256
#     con = create_connection(mem)
#     with con:
#         cursor = con.cursor()
#         cursor.execute("SELECT count(*) FROM items;")
#         cur_item_count = cursor.fetchone()
#         cur_item_count = cur_item_count[0]
#         if cur_item_count == store_item_count:
#             return False
#         else:
#             return True

# SQL statements


# def execute_sql_2(con, sql_statement, var=None):
#     cur = con.cursor()
#     cur.execute(sql_statement, var)


# def execute_fetchone_sql_2(con, sql_statement, var=None):
#     cur = con.cursor()
#     if var is not None:
#         cur.execute(sql_statement, var)
#     else:
#         cur.execute(sql_statement)
#
#     return cur.fetchone()


# def execute_fetchall_sql_2(con, sql_statement, var=None):
#     cur = con.cursor()
#     if var is not None:
#         cur.execute(sql_statement, var)
#     else:
#         cur.execute(sql_statement)
#
#     return cur.fetchall()


# INSERT


# Inserts given values into accounts table at given columns. Returns last row id.
def add_account_row(conn, some_sql, some_account):
    # some_sql = """INSERT INTO accounts (username, password)
    #         VALUES(?,?)"""

    sql.execute_sql(conn, some_sql, some_account['user'], some_account['pass'])
    # cursor = conn.cursor()
    # cursor.execute(sql, some_account)


# Inserts given values into accounts table at given columns. Returns last row id.
def add_inventory_row(conn, some_sql, some_inventory):
    # some_sql = """INSERT INTO inventories (account_id, character_id, name)
    #         VALUES(?,?,?)"""
    sql.execute_sql(conn, some_sql, some_inventory['acc_id'], some_inventory['char_id'], some_inventory['name'])


# Inserts given values into accounts table at given columns. Returns last row id.
def add_character_row(conn, some_sql, some_character):
    # some_sql = """INSERT INTO characters (account_id, name, currency)
    #         VALUES(?,?,?)"""
    sql.execute_sql(conn, some_sql, some_character['acc_id'], some_character['name'], some_character['currency'])


# Inserts given values into accounts table at given columns. Returns last row id.
def add_item_row(conn, some_sql, some_item):
    # some_sql = """INSERT INTO items (account_id, character_id, inventory_id, item, api, quantity)
    #         VALUES(?,?,?,?,?,?)"""
    sql.execute_sql(conn, some_sql, some_item['acc_id'], some_item['char_id'], some_item['inv_id'], some_item['item'],
                    some_item['api'], some_item['quant'])


# Used to populate stores
def add_store_item(con, some_sql, item_info):
    # some_sql = """INSERT INTO items (item, api, store)
    #          VALUES(?,?,?)"""
    sql.execute_sql(con, some_sql, item_info['item'], item_info['api'], item_info['store'])


# TODO Reminder: Complex is better than complicated. Remember the shit block. Never forget.
def query_accounts_with_characters(conn, some_sql):
    temp = []
    # sql = """SELECT DISTINCT account_id FROM characters;"""
    account_id_list = sql.execute_fetchall_sql(conn, some_sql)
    # print(account_id_list)
    for tup in account_id_list:
        # print(tup)
        temp.append(tup[0])
    return temp
#
#
#
# def query_characters_with_inventories(conn,  some_sql):
#     temp = []
#     # sql = """SELECT DISTINCT character_id FROM inventories;"""
#     account_id_list = sql.execute_fetchall_sql(conn, some_sql)
#     print(account_id_list)
#     for tup in account_id_list:
#         # print(tup)
#         temp.append(tup[0])
#     return temp


# SELECT


def count_rows(conn, some_sql, some_table):
    new_sql = some_sql.format(some_table)
    yup = sql.execute_fetchone_sql(conn, new_sql)
    return yup


if __name__ == '__main__':
    acc = ('username', 'password')
    inv = (1, 'inv name')
    char = (1, 'char name', 420)
    item = (2, 2, 2, 'item name', 'api url', 1)
    account1 = {'user': 'kaza', 'pass': 'tree'}
    character1 = {'acc_id': 1, 'name': 'char name', 'currency': 5000}
    inventory1 = {'acc_id': 1, 'char_id': 1, 'name': 'inv name'}
    item1 = {'acc_id': 1, 'char_id': 1, 'inv_id': 1, 'item': 'item name', 'api': 'api url', 'quant': 1}
    # con = create_connection(db)
    # with con:
        # add_account_row(con, account1)
        # add_inventory_row(con, inv)
        # add_character_row(con, char)
        # add_item_row(con, sql.sql_add_item_row(), item1)

        # modular queries
        # print('1', query_fetchall(con, sql.sql_username_password()))
        # print('2', query_fetchone_list(con, sql.sql_account_row(), acc[0]))
        # print('3', query_fetchone_list(con, sql.sql_character_row(), char[1]))
        # print('4', query_fetchone_list(con, sql.sql_inventory_row(), inv[1]))
        # print('5', query_fetchall_list(con, sql.sql_all_characters(), 1))
        # print('6', query_fetchall_list(con, sql.sql_all_inventory_names(), 1))
        # print('7', query_fetchall(con, sql.sql_accounts_with_characters()))
        # print('8', query_fetchall(con, sql.sql_characters_with_inventories()))

        # Use these as reference for new queries

        # print('1' + query_username_password(con, sql_username_password()))
        # print('2', query_account_row(con, sql_account_row(), 'Kazact'))
        # print('3', query_character_row(con, sql_character_row(), 'char name'))
        # print('4', query_inventory_row(con, sql_inventory_row(), 'Kazact'))
        # print('5', query_all_characters(con, sql_all_characters(), '1'))
        # print('6', query_all_inventories(con, sql.sql_all_inventory_names(), 1))
        # print('7', query_accounts_with_characters(con, sql.sql_accounts_with_characters()))
        # print('7', query_characters_with_inventories(con, sql.sql_characters_with_inventories()))
        # print(count_rows(con, 'items'))

if __name__ == '__main__':
    con = create_connection(db)
    with con:
        print(count_rows(con, sql.sql_count_rows(), 'items')[0])
