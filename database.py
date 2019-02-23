import sqlite3
from sqlite3 import Error
import sql
#
db = 'C:\\sqlite\\db\\test.db'
mem = ':memory:'

# TODO: Not sure if still want to do this. Figure it out

# TODO: Write query functions similar to the add functions i have now.
# TODO: This will allow a dictionary to be passed. Meaning my variables can be passed unordered
# TODO: Refactor database integration tests when this is done.

# TODO: Comment all of the things. Every block if it makes sense to do so.


# Creates a connection to test.db
def create_connection(db_path):
    try:
        conn = sqlite3.connect(db_path)
        return conn
    except Error as e:
        print(e)
    return None


# INSERT


# Inserts given values into accounts table at given columns.
def add_account_row(conn, some_sql, some_account):
    sql.execute_sql(conn, some_sql, some_account['user'], some_account['pass'])


# Inserts given values into accounts table at given columns.
def add_inventory_row(conn, some_sql, some_inventory):
    sql.execute_sql(conn, some_sql, some_inventory['acc_id'], some_inventory['char_id'], some_inventory['name'])


# Inserts given values into accounts table at given columns.
def add_character_row(conn, some_sql, some_character):
    sql.execute_sql(conn, some_sql, some_character['acc_id'], some_character['name'], some_character['currency'])


# Inserts given values into accounts table at given columns.
def add_item_row(conn, some_sql, some_item):
    sql.execute_sql(conn, some_sql, some_item['acc_id'], some_item['char_id'], some_item['inv_id'], some_item['item'],
                    some_item['api'], some_item['quant'])


# Used to populate store tables
def add_store_item(conn, some_sql, item_info):
    sql.execute_sql(conn, some_sql, item_info['item'], item_info['api'], item_info['store'])


# SELECT

def count_rows(conn, some_sql, some_table):
    new_sql = some_sql.format(some_table)
    count_tuple = sql.execute_fetchone_sql(conn, new_sql)
    return count_tuple


# TODO Reminder: Complex is better than complicated. Remember the shit block. Never forget.
def query_accounts_with_characters(conn, some_sql):
    temp = []
    account_id_list = sql.execute_fetchall_sql(conn, some_sql)
    for tup in account_id_list:
        temp.append(tup[0])
    return temp


def query_characters_with_inventories(conn,  some_sql):
    temp = []
    account_id_list = sql.execute_fetchall_sql(conn, some_sql)
    print(account_id_list)
    for tup in account_id_list:
        temp.append(tup[0])
    return temp


# Delete
# TODO: test this
def delete_item(conn, item, inv_id):
    sql.execute_sql(conn, sql.sql_delete_item(), item, inv_id)


# TODO: test this
def delete_all_character_items(conn, char_id):
    sql.execute_sql(conn, sql.sql_delete_all('items', 'character_id'), char_id)


# TODO: test this
def delete_character_inventories(conn, char_id):
    sql.execute_sql(conn, sql.sql_delete_all('inventories', 'character_id'), char_id)


# TODO: test this
def delete_character(conn, char_id):
    delete_all_character_items(conn, char_id)
    delete_character_inventories(conn, char_id)
    sql.execute_sql(conn, sql.sql_delete_all('characters', 'id'), char_id)


# Update
# TODO: test this
def item_in_inventory_add(conn, inv_id, item):
    with conn:
        items_in_inv = sql.execute_fetchall_sql(conn, sql.sql_query_items_in_inventory(), inv_id)
        # print(items_in_inv)8
        for i in items_in_inv:
            if item in i:
                int_quant = int(i[1])
                int_quant += 1
                sql.execute_sql(conn, sql.update_quantity(), int_quant, i[0], inv_id)
                return True
        return False


# TODO: test this
def item_in_inventory_minus(conn, inv_id, item):
    with conn:
        items_in_inv = sql.execute_fetchall_sql(conn, sql.sql_query_items_in_inventory(), inv_id)
        # print(items_in_inv)8
        for i in items_in_inv:
            if item in i:
                int_quant = int(i[1])
                int_quant -= 1
                sql.execute_sql(conn, sql.update_quantity(), int_quant, i[0], inv_id)
                return True
        return False


# if __name__ == '__main__':
#     acc = ('username', 'password')
#     inv = (1, 'inv name')
#     char = (1, 'char name', 420)
#     item = (2, 2, 2, 'item name', 'api url', 1)
#     account1 = {'user': 'kaza', 'pass': 'tree'}
#     character1 = {'acc_id': 1, 'name': 'char name', 'currency': 5000}
#     inventory1 = {'acc_id': 1, 'char_id': 1, 'name': 'inv name'}
#     item1 = {'acc_id': 1, 'char_id': 1, 'inv_id': 1, 'item': 'item name', 'api': 'api url', 'quant': 1}
#     con = create_connection(db)
    # with con:
        # add_account_row(con, sql.sql_add_account_row(), account1)
        # add_inventory_row(con, sql.sql_add_inventory_row(), inventory1)
        # add_character_row(con, sql.sql_add_character_row(), character1)
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
