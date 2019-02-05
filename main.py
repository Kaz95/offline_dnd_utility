
from account import user_creates_account
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
from database import add_item_row, add_store_item, create_schema, wrong_schema
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
            user_creates_account()
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
        print('name character')
        name = input()
        character_info = (current_account.id, name, 5000)
        add_character_row(connection, character_info)


def character_selection():
    conn = create_connection()
    with conn:
        print('choose a character')
        query_all_characters(conn, current_account.id)
        char_name = input()
        current_character_info = query_character_row(conn, char_name)
        current_character = Player(current_character_info[0], current_character_info[1], current_character_info[2],
                                   [])
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
            add_store_item(conn, temp)


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


def fresh_installation():
    create_schema()
    stock_stores()


# Working model for main
if __name__ == '__main__':
    if wrong_schema():
        fresh_installation()
    # TODO check if store is stocked here via database.wrong_item_count().
    # TODO currently assumes stores are stocked if all tables exist.
    current_account = load_account_object(main_menu())  # account object fields populated via main menu. Set to cur acc.
    # If current account has characters
    if current_account.id in query_accounts_with_characters(create_connection()):
        character = character_selection()
    else:
        print('no characters')
        print('make a character')
        character_creation()
        character = character_selection()
        create_backpack()

