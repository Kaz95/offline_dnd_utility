import sqlite3
from sqlite3 import Error
import sql

# Test DB paths.
db = 'C:\\sqlite\\db\\test.db'
mem = ':memory:'

# TODO: Not sure if still want to do this. Figure it out

# TODO: Write query functions similar to the add functions I have now.
# TODO: This will allow a dictionary to be passed. Meaning my variables can be passed unordered
# TODO: Refactor database integration tests when this is done.


# Creates a connection to test.db
def create_connection(db_path):
    try:
        conn = sqlite3.connect(db_path)
        return conn
    except Error as e:
        print(e)
    return None


# INSERT
# These functions all assume acc_info is passed as a dictionary with known keys.


# Inserts given values into accounts table at given columns.
def add_account_row(conn, some_sql, acc_info):
    sql.execute_sql(conn, some_sql, acc_info['username'], acc_info['password'])


# Inserts given values into accounts table at given columns.
def add_inventory_row(conn, some_sql, inv_info):
    sql.execute_sql(conn, some_sql, inv_info['acc_id'], inv_info['char_id'], inv_info['name'])


# Inserts given values into accounts table at given columns.
def add_character_row(conn, some_sql, char_info):
    sql.execute_sql(conn, some_sql, char_info['acc_id'], char_info['name'], char_info['currency'])


# Inserts given values into accounts table at given columns.
def add_item_row(conn, some_sql, item_info):
    sql.execute_sql(conn, some_sql, item_info['acc_id'], item_info['char_id'], item_info['inv_id'], item_info['item'],
                    item_info['api'], item_info['value'], item_info['quantity'])


# Used to populate store tables
def add_store_item(conn, some_sql, item_info):
    sql.execute_sql(conn, some_sql, item_info['item'], item_info['api'], item_info['currency'], item_info['store'])


# SELECT

def count_rows(conn, some_sql, some_table):
    new_sql = some_sql.format(some_table)
    count_tuple = sql.execute_fetchone_sql(conn, new_sql)
    return count_tuple[0]


# TODO Reminder: Complex is better than complicated. Remember the shit block. Never forget.
# Returns a list of integers representing account IDs.
def query_accounts_with_characters(conn, some_sql):
    temp = []
    acc_id_list = sql.execute_fetchall_sql(conn, some_sql)
    for tup in acc_id_list:
        temp.append(tup[0])
    return temp


# Returns a list of integers representing character IDs.
# TODO: Test
# TODO: No apparent usage.
# def query_characters_with_inventories(conn,  some_sql):
#     temp = []
#     acc_id_list = sql.execute_fetchall_sql(conn, some_sql)
#     for tup in acc_id_list:
#         temp.append(tup[0])
#     return temp


# Delete

# Deletes a single item based on inventory ID.
def delete_item(conn, item, inv_id):
    sql.execute_sql(conn, sql.delete_item(), item, inv_id)


# Deletes all items based on character ID.
def delete_all_character_items(conn, char_id):
    sql.execute_sql(conn, sql.delete_all('items', 'character_id'), char_id)


# Deletes all character inventories based on character ID.
def delete_character_inventories(conn, char_id):
    sql.execute_sql(conn, sql.delete_all('inventories', 'character_id'), char_id)


# TODO: test this
# Deletes all information pertaining to a given character ID from DB.
def delete_character(conn, char_id):
    delete_all_character_items(conn, char_id)
    delete_character_inventories(conn, char_id)
    sql.execute_sql(conn, sql.delete_all('characters', 'id'), char_id)


# Update
# TODO: Verify if I need to change tup[1] to an integer or not.
# TODO: I may regret this change. We will see.

# Checks if item is in inventory. If it is,
# Adds or subtracts one based on add_subtract variable
# If subtracting, will check if item quantity > 1
# This allows the item to be deleted upon reaching 0 in another part of the program.
def in_inventory(conn, inv_id, item, add_subtract=None):
    with conn:
        # [('Club', '1'), ('Dagger', 1)]
        items_in_inv_list = sql.execute_fetchall_sql(conn, sql.query_items_in_inventory(), inv_id)

        for tup in items_in_inv_list:
            if item in tup:
                if add_subtract == '+':
                    int_quantity = int(tup[1])
                    int_quantity += 1
                    sql.execute_sql(conn, sql.update_quantity(), int_quantity, tup[0], inv_id)
                    return True

                elif add_subtract == '-':
                    int_quantity = int(tup[1])
                    if int_quantity > 1:
                        int_quantity -= 1
                        sql.execute_sql(conn, sql.update_quantity(), int_quantity, tup[0], inv_id)
                        return True
        return False


# Checks if item is in inventory. If it is, subtracts one from DB quantity column and returns True. Else returns False.
# def item_in_inventory_minus(conn, inv_id, item):
#     with conn:
#         items_in_inv_list = sql.execute_fetchall_sql(conn, sql.query_items_in_inventory(), inv_id)
#
#         for tup in items_in_inv_list:
#             if item in tup:
#                 int_quantity = int(tup[1])
#                 if int_quantity > 1:
#                     int_quantity -= 1
#                     sql.execute_sql(conn, sql.update_quantity(), int_quantity, tup[0], inv_id)
#                     return True
#         return False


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
        # add_account_row(con, sql.add_account_row(), account1)
        # add_inventory_row(con, sql.add_inventory_row(), inventory1)
        # add_character_row(con, sql.add_character_row(), character1)
        # add_item_row(con, sql.add_item_row(), item1)

        # modular queries
        # print('1', query_fetchall(con, sql.query_username_password()))
        # print('2', query_fetchone_list(con, sql.query_account_row(), acc[0]))
        # print('3', query_fetchone_list(con, sql.query_character_row(), char[1]))
        # print('4', query_fetchone_list(con, sql.query_inventory_row(), inv[1]))
        # print('5', query_fetchall_list(con, sql.query_all_characters(), 1))
        # print('6', query_fetchall_list(con, sql.query_all_inventory_names(), 1))
        # print('7', query_fetchall(con, sql.query_accounts_with_characters()))
        # print('8', query_fetchall(con, sql.query_characters_with_inventories()))

        # Use these as reference for new queries

        # print('1' + query_username_password(con, query_username_password()))
        # print('2', query_account_row(con, query_account_row(), 'Kazact'))
        # print('3', query_character_row(con, query_character_row(), 'char name'))
        # print('4', query_inventory_row(con, query_inventory_row(), 'Kazact'))
        # print('5', query_all_characters(con, query_all_characters(), '1'))
        # print('6', query_all_inventories(con, sql.query_all_inventory_names(), 1))
        # print('7', query_accounts_with_characters(con, sql.query_accounts_with_characters()))
        # print('7', query_characters_with_inventories(con, sql.query_characters_with_inventories()))
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
