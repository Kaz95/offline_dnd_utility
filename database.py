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
def add_account_row(conn, some_account):
    some_sql = """INSERT INTO accounts (username, password)
            VALUES(?,?)"""

    sql.execute_sql(conn, some_sql, some_account[0], some_account[1])
    # cursor = conn.cursor()
    # cursor.execute(sql, some_account)
    return some_sql


# Inserts given values into accounts table at given columns. Returns last row id.
def add_inventory_row(conn, some_inventory):
    some_sql = """INSERT INTO inventories (character_id, name)
            VALUES(?,?)"""
    sql.execute_sql(conn, some_sql, some_inventory[0], some_inventory[1])
    return some_sql


# Inserts given values into accounts table at given columns. Returns last row id.
def add_character_row(conn, some_character):
    some_sql = """INSERT INTO characters (account_id, name, currency)
            VALUES(?,?,?)"""
    sql.execute_sql(conn, some_sql, some_character[0], some_character[1], some_character[2])
    return some_sql


# Inserts given values into accounts table at given columns. Returns last row id.
def add_item_row(conn, some_item):
    some_sql = """INSERT INTO items (inventory_id, item, api, quantity)
            VALUES(?,?,?,?)"""
    sql.execute_sql(conn, some_sql, some_item[0], some_item[1], some_item[2], some_item[3])
    return some_sql


# Used to populate stores
def add_store_item(con, item_info):
    some_sql = """INSERT INTO items (item, api, store)
             VALUES(?,?,?)"""
    sql.execute_sql(con, some_sql, item_info[0], item_info[1], item_info[2])
    return some_sql


# QUERY
def query_fetchone(conn, some_sql):
    return sql.execute_fetchone_sql(conn, some_sql)


def query_fetchall(conn, some_sql):
    return sql.execute_fetchall_sql(conn, some_sql)


def query_fetchone_list(conn, some_sql, var):
    return list(sql.execute_fetchone_sql(conn, some_sql, var))


def query_fetchall_list(conn, some_sql, var=None):
    if var is not None:
        return list(sql.execute_fetchall_sql(conn, some_sql, var))
    else:
        return list(sql.execute_fetchall_sql(conn, some_sql))


# def query_username_password(conn, sql):
#     # sql = """SELECT username, password FROM accounts;"""
#     some_account = execute_fetchall_sql(conn, sql)
#     return some_account
#
#
# def query_account_row(conn, sql, username):
#     # sql = """SELECT id, username, password FROM accounts WHERE username = ?;"""
#     some_account = execute_fetchone_sql(conn, sql, username)
#     return list(some_account)
#
#
# def query_character_row(conn, sql, character_name):
#     # sql = """SELECT id, name, currency FROM characters WHERE name = ?;"""
#     some_account = execute_fetchone_sql(conn, sql, character_name)
#     return list(some_account)
#
#
# def query_inventory_row(conn, sql, inventory_name):
#     # sql = """SELECT id, name FROM inventories WHERE name = ?;"""
#     some_account = execute_fetchone_sql(conn, sql, inventory_name)
#     return list(some_account)
#
#
# def query_all_characters(conn, sql, account_id):
#     # sql = """SELECT name, currency FROM characters WHERE account_id = ?;"""
#     some_account = execute_fetchall_sql(conn, sql, account_id)
#     for character in some_account:
#         print(list(character))
#
#
# def query_all_inventories(conn, some_sql, character_id):
#     # sql = """SELECT name FROM inventories WHERE character_id = ?;"""
#     some_account = sql.execute_fetchall_sql(conn, some_sql, character_id)
#     for character in some_account:
#         print(list(character))


# TODO BRING THIS SHIT BACK ITS WAY BETTER. ADD INTO MAIN.PY @ TRASH BLOCK
# def query_accounts_with_characters(conn, some_sql):
#     temp = []
#     # sql = """SELECT DISTINCT account_id FROM characters;"""
#     account_id_list = sql.execute_fetchall_sql(conn, some_sql)
#     print(account_id_list)
#     for tup in account_id_list:
#         # print(tup)
#         temp.append(tup[0])
#     return temp
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

# TODO decouple sql and test....maybe?
def count_rows(conn, some_table):
    some_sql = """SELECT count(*) FROM {};""".format(some_table)
    yup = sql.execute_fetchone_sql(conn, some_sql)
    return yup[0]


if __name__ == '__main__':
    acc = ('username', 'password')
    inv = (1, 'inv name')
    char = (1, 'char name', 420)
    item = (1, 'item name', 'api url', 1)
    # con = create_connection(db)
    # with con:
        # add_account_row(con, acc)
        # add_inventory_row(con, inv)
        # add_character_row(con, char)
        # add_item_row(con, item)

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

