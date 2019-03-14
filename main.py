# from account import user_creates_account, log_in, load_account_object
# from player import Player
# from inventory import Inventory
# from database import create_connection
# from database import add_character_row, add_inventory_row
# from database import query_character_row, query_all_characters, query_accounts_with_characters, query_inventory_row
# from database import query_all_inventories
# from database import create_schema, wrong_schema, stock_stores
import sql
import inventory
import account
import character
import database
import setup
db = 'C:\\sqlite\\db\\test.db'
mem = ':memory:'
# TODO: Deprecated. scan for anything of value and delete. RIP.


# Used to flesh out log-in features
def main_menu(conn):
    new = False
    while True:
        if new:
            print('---Log in---')
            username = account.log_in(conn, username, password)
            break
        print('1: Login       2: Sign-up')
        answer = input()
        print('create name')
        username = input()
        print('create password')
        password = input()
        if answer == '2':
            account.user_creates_account(conn, username, password)
            new = True
        elif answer == '1':
            username = account.log_in(conn, username, password)
            break
    return username


# Working model for character creation
# def character_creation(conn):
    # current_account = None
    # connection = database.create_connection(db)
    # with conn:
    #     print('name character')
    #     name = input()
    #     character_info = (cur_account.id, name, 5000)
        # character_info = {'acc_id': cur_account.id, 'name': name, 'currency': 5000}
        # database.add_character_row(conn, sql.add_character_row(), character_info)


# Working model for character creation
def character_creation(conn, name, currency):
        # character_info = (cur_account.id, name, 5000)
        character_info = {'acc_id': cur_account.id, 'name': name, 'currency': currency}
        database.add_character_row(conn, sql.add_character_row(), character_info)


def character_selection(conn):
    # conn = database.create_connection(db)
    with conn:
        print('choose a character')
        print(list(sql.execute_fetchall_sql(conn, sql.query_all_characters(), cur_account.id)))
        char_name = input()
        current_character_info = list(sql.execute_fetchone_sql(conn, sql.query_character_row(), char_name))

        current_character = character.Character(current_character_info[0], current_character_info[1],
                                                current_character_info[2], [])
    return current_character


def create_backpack(conn):
    # conn = database.create_connection(db)
    with conn:
        # backpack_info = (cur_account.id, cur_character.id, cur_character.name)
        backpack_info = {'acc_id': cur_account.id, 'char_id': cur_character.id, 'name': cur_character.name}
        database.add_inventory_row(conn, sql.add_inventory_row(), backpack_info)


def inventory_selection(conn):
    # conn = database.create_connection(db)
    with conn:
        print('choose inventory')
        print(list(sql.execute_fetchall_sql(conn, sql.query_all_inventory_names(), cur_character.id)))
        inv_name = input()
        current_character_info = list(sql.execute_fetchone_sql(conn, sql.query_inventory_row(), inv_name))
        current_inventory = inventory.Inventory(current_character_info[0], current_character_info[1])
    return current_inventory


def fresh_installation(conn):
    setup.create_schema(conn)
    setup.stock_stores(conn)


# def add_item_db(self, item, conn):
#     url = api.get_item_url(item, Player.list_of_dics)   # TODO NOT DRY
#     item_info = (self.inventories[0], item, url, 1)
#     database.add_item_row(conn, item_info)


# # Working model for main
if __name__ == '__main__':
    cur_character = None
    cur_account = None
    cur_inventory = None
    while True:
        conn = database.create_connection(db)
        with conn:
            if setup.wrong_schema(conn):
                fresh_installation(conn)
            # TODO check if store is stocked here via database.wrong_item_count().
            # TODO currently assumes stores are stocked if all tables exist.
            # account object fields populated via main menu. Set to cur acc.
            cur_account = account.load_account_object(main_menu(conn))
            # If current account has characters
            if cur_account.id in database.query_accounts_with_characters(conn, sql.query_accounts_with_characters()):
                cur_character = character_selection(conn)
            else:
                character_creation(conn)
                cur_character = character_selection(conn)
                create_backpack(conn)

            cur_inventory = inventory_selection(conn)
            print(cur_inventory.name)
            cur_character.inventories.append(cur_inventory.id)
            cur_character.buy_sell('Club', 'buy')
            cur_character.add_item_db('Club', conn, cur_account.id, cur_inventory.id)
            print('go again?')
            a = input()
            if a != '':
                break
            # log_out()


# if __name__ == '__main__':
#     cur_character = None
#     conn = database.create_connection(db)
#     with conn:
#         sql.execute_sql(conn, sql.delete_all('items'), 2)



