from account import user_creates_user_account
from account import user_creates_admin_account
from account import log_in
from account import load_account_object
from account import Player
from account import Inventory
from database import create_connection
from database import add_character_row
from database import query_character_row
from database import query_all_characters
from database import query_accounts_with_characters
from database import add_inventory_row
from database import query_characters_with_inventories
from database import query_all_inventories
from database import query_inventory_row
from database import add_item_row, add_store_item,create_schema
from search import search
from stores import stores
import requests
from search import regex
import json


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
            print('Admin or user?')
            ctype = 'Admin'    # TODO Change back to input once Player option is live.
            if ctype == 'Admin':
                user_creates_admin_account()
            elif ctype == 'user':
                user_creates_user_account()
            new = True
        elif answer == '1':
            username = log_in()
            break
    return username


# Working model for character creation
def character_creation():
    # current_account = None
    connection = create_connection()
    with connection:
        if current_account.admin == 1:
            print('1: DM       2: Player')
            rank = '2'  # TODO Change back to input at some point
            if rank == '1':
                print('name character')
                name = input()
                character_info = (current_account.id, name, None, True)
                add_character_row(connection, character_info)
            elif rank == '2':
                print('name character')
                name = input()
                character_info = (current_account.id, name, 5000, False)
                add_character_row(connection, character_info)
        elif current_account.admin == 0:
            print('name character')
            name = input()
            character_info = (current_account.id, name, 5000, False)
            add_character_row(connection, character_info)


def character_selection():
    conn = create_connection()
    with conn:
        current_character = None
        print('choose a character')
        query_all_characters(conn, current_account.id)
        char_name = input()
        current_character_info = query_character_row(conn, char_name)
        print(current_character_info)
        if current_character_info[3] == 1:
            current_character = Player(current_character_info[0], current_character_info[1], None, [], True)
        elif current_character_info[3] == 0:
            current_character = Player(current_character_info[0], current_character_info[1], current_character_info[2],
                                       [], False)
    return current_character


def stock_stores():
    store_dict = stores()
    conn = create_connection()
    with conn:
        url = "http://www.dnd5eapi.co/api/equipment/"
        response = requests.get(url)
        response.raise_for_status()
        json_shit = json.loads(response.text)
        json_shit = json_shit['results']
        for dic in json_shit:
            temp = []
            for k, v in dic.items():
                temp.append(v)
                if v[0:37] == 'http://www.dnd5eapi.co/api/equipment/':
                    num = regex(v)
                    if num in store_dict['GS']:
                        temp.append('General Store')
                    elif num in store_dict['BS']:
                        temp.append('Blacksmith')
                    elif num in store_dict['Ship']:
                        temp.append('Shipyard')
                    elif num in store_dict['Stables']:
                        temp.append('Stables')
                    else:
                        temp.append('No Store')
            temp = tuple(temp)
            print(temp)
            add_store_item(conn, temp)

# def create_store():
#     conn = create_connection()
#     with conn:
#         print('make a store')
#         store_name = input()
#         store_info = (character.id, store_name)
#         add_inventory_row(conn, store_info)


def create_backpack():
    conn = create_connection()
    with conn:
        backpack_info = (character.id, character.name)
        add_inventory_row(conn, backpack_info)


def inventory_selection():
    conn = create_connection()
    with conn:
        print('choose inventory')
        query_all_inventories(conn, character.id)
        inv_name = input()
        current_character_info = query_inventory_row(conn, inv_name)
        current_inventory = Inventory(current_character_info[0], current_character_info[1])
    return current_inventory


def add_store_items():
    conn = create_connection()
    with conn:
        while True:
            print('stock store')
            print('------------')
            print('Search:')
            item = input()
            result = search(item)
            item_info = (inventory.id, result[0], result[1], None)
            add_item_row(conn, item_info)
            print(result[0] + ' added.')
            print('---------------')
            print('again?')
            answer = input()
            if answer != '':
                break


# Working model for main
if __name__ == '__main__':
    create_schema()
    current_account = load_account_object(main_menu())  # account object fields populated via main menu. Set to cur acc.
    # If current account has characters
    if current_account.id in query_accounts_with_characters(create_connection()):
        character = character_selection()
    else:
        print('no characters')
        print('make a character')
        character_creation()
        character = character_selection()
    stock_stores()

    if character.is_dm:
        if character.id in query_characters_with_inventories(create_connection()):
            inventory = inventory_selection()
        else:
            print('no inventory')
            print('make an inventory')
            # create_store()    # TODO turn back on once DM is live again.
            inventory = inventory_selection()
    else:
        create_backpack()
    # if character.isDM:
        # add_store_items()

    # TODO Make sure add/remove item from store and buy/sell methods work.
    # TODO Code review
