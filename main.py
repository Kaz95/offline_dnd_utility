from account import user_creates_account, log_in, load_account_object
from player import Player
from inventory import Inventory
from database import create_connection
from database import add_character_row, add_inventory_row
from database import query_character_row, query_all_characters, query_accounts_with_characters, query_inventory_row
from database import query_all_inventories
from database import create_schema, wrong_schema, stock_stores
import setup

db = 'C:\\sqlite\\db\\test.db'
mem = ':memory:'


# Used to flesh out log-in features
def main_menu():
    new = False
    while True:
        if new:
            print('---Log in---')
            username = log_in()
            break
        print('1: Login       2: Sign-up')
        answer = input()
        if answer == '2':
            user_creates_account()
            new = True
        elif answer == '1':
            username = log_in()
            break
    return username


# Working model for character creation
def character_creation():
    # current_account = None
    connection = create_connection(db)
    with connection:
        print('name character')
        name = input()
        character_info = (current_account.id, name, 5000)
        add_character_row(connection, character_info)


def character_selection():
    conn = create_connection(db)
    with conn:
        print('choose a character')
        query_all_characters(conn, current_account.id)
        char_name = input()
        current_character_info = query_character_row(conn, char_name)
        current_character = Player(current_character_info[0], current_character_info[1], current_character_info[2],
                                   [])
    return current_character


def create_backpack():
    conn = create_connection(db)
    with conn:
        backpack_info = (character.id, character.name)
        add_inventory_row(conn, backpack_info)


def inventory_selection():
    conn = create_connection(db)
    with conn:
        print('choose inventory')
        query_all_inventories(conn, character.id)
        inv_name = input()
        current_character_info = query_inventory_row(conn, inv_name)
        current_inventory = Inventory(current_character_info[0], current_character_info[1])
    return current_inventory


def fresh_installation():
    setup.create_schema()
    setup.stock_stores()


# Working model for main
if __name__ == '__main__':
    if wrong_schema():
        fresh_installation()
    # TODO check if store is stocked here via database.wrong_item_count().
    # TODO currently assumes stores are stocked if all tables exist.
    current_account = load_account_object(main_menu())  # account object fields populated via main menu. Set to cur acc.
    # If current account has characters
    if current_account.id in query_accounts_with_characters(create_connection(db)):
        character = character_selection()
    else:
        print('no characters')
        print('make a character')
        character_creation()
        character = character_selection()
        create_backpack()

