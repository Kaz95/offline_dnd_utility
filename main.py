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
import player
import database
import setup

db = 'C:\\sqlite\\db\\test.db'
mem = ':memory:'


# Used to flesh out log-in features
def main_menu(conn):
    new = False
    while True:
        if new:
            print('---Log in---')
            username = account.log_in(conn)
            break
        print('1: Login       2: Sign-up')
        answer = input()
        if answer == '2':
            account.user_creates_account(conn)
            new = True
        elif answer == '1':
            username = account.log_in(conn)
            break
    return username


# Working model for character creation
def character_creation(conn):
    # current_account = None
    # connection = database.create_connection(db)
    with conn:
        print('name character')
        name = input()
        character_info = (cur_account.id, name, 5000)
        database.add_character_row(conn, character_info)


def character_selection(conn):
    # conn = database.create_connection(db)
    with conn:
        print('choose a character')
        print(database.query_fetchall_list(conn, sql.sql_all_characters(), cur_account.id))
        char_name = input()
        current_character_info = database.query_fetchone_list(conn, sql.sql_character_row(), char_name)

        current_character = player.Player(current_character_info[0], current_character_info[1],
                                          current_character_info[2], [])
    return current_character


def create_backpack(conn):
    # conn = database.create_connection(db)
    with conn:
        backpack_info = (cur_character.id, cur_character.name)
        database.add_inventory_row(conn, backpack_info)


def inventory_selection(conn):
    # conn = database.create_connection(db)
    with conn:
        print('choose inventory')
        print(database.query_fetchall_list(conn, sql.sql_all_inventory_names(), cur_character.id))
        inv_name = input()
        current_character_info = database.query_fetchone_list(conn, sql.sql_inventory_row(), inv_name)
        current_inventory = inventory.Inventory(current_character_info[0], current_character_info[1])
    return current_inventory


def fresh_installation():
    setup.create_schema()
    setup.stock_stores()


def log_out():
    main_menu()


# # Working model for main
if __name__ == '__main__':
    cur_character = None
    cur_account = None
    cur_inventory = None
    while True:
        conn = database.create_connection(db)
        with conn:
            if setup.wrong_schema(conn):
                fresh_installation()
            # TODO check if store is stocked here via database.wrong_item_count().
            # TODO currently assumes stores are stocked if all tables exist.
            # account object fields populated via main menu. Set to cur acc.
            cur_account = account.load_account_object(main_menu(conn))
            # If current account has characters
            if cur_account.id in database.query_accounts_with_characters(conn, sql.sql_accounts_with_characters()):
                cur_character = character_selection(conn)
            else:
                character_creation(conn)
                cur_character = character_selection(conn)
                create_backpack(conn)

            cur_inventory = inventory_selection(conn)
            print(cur_inventory.name)
            cur_character.inventories.append(cur_inventory.id)
            cur_character.buy_item('Club', conn)
            print('go again?')
            a = input()
            if a != '':
                break
            # log_out()


# TODO figure out why character c doesnt have 2 clubs
# if __name__ == '__main__':
#     cur_character = None
    # conn = database.create_connection(db)
    # with conn:
    #     cur_account = None
    #     cur_inventory = None
    #     cur_character = player.Player(4, 'k', 5000, [4])
    #     cur_character.buy_item('Club', conn)
    #     cur_character.buy_item('Club', conn)
    #     cur_character.buy_item('Club', conn)



