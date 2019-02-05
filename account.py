# !/usr/bin/python
from search import search
from search import get_price_info
from search import convert_price_info
from database import create_connection
from database import query_account_row
from database import query_username_password
from database import add_account_row
import pprint
import json
import requests


# Account class
class Account:
    log_in_dic = {}

    def __init__(self, acc_id, name, password, admin):
        self.id = acc_id
        self.name = name    # Username
        self.password = password    # Password
        self.admin = admin  # is admin. uses boolean True/False

    # TODO Check if still needed. Add logout method.
    # Adds account name:password as key:value pair.
    def add_account(self):
        Account.log_in_dic[self.name] = self.password


# Player Class
class Player:
    def __init__(self, player_id, name, currency, inventories, is_dm):
        self.id = player_id
        self.currency = currency    # All currency held in cp. cp is then formatted via convert_currency() before view.
        self.name = name  # Character(DM) name.
        self.inventories = inventories  # Character(DM) Inventories(Stores)
        self.is_dm = is_dm  # is dm. Uses True/False boolean.

    # Inventory management

    def add_item(self, store, some_item):
        item = search(some_item)  # Search returns ['Item', 'api url']
        self.inventories[store][item[0]] = item[1]  # Adds above to inventory dictionary as key:value pair



    # # Inventory management
    # def add_item_dict(self, item):
    #     url = "http://www.dnd5eapi.co/api/equipment/"  # Storing API url as var
    #     response = requests.get(url)  # stores response from .get ping as response
    #     response.raise_for_status()  # Checks response for errors
    #     equipment = json.loads(response.text)  # json.load turns json data to a python dictionary
    #     list_of_dict = equipment['results']  # Dictionary containing Name/url: Values
    #     print('What are you looking for?')
    #     # Asks for item to search for
    #     for dic in list_of_dict:  # For dic in list of dicts
    #         if dic['name'] == item:  # If dic[name] == item searched for
    #             self.inventories[dic['name']] = dict({})  # Adds item name as key of above dictionary
    #             # Adds quantity as key for nested item dictionary. Value of 1.
    #             self.inventories[dic['name']]['quantity'] = 1
    #             # Adds api url as key for nested item dictionary. Value is api url related to item name.
    #             self.inventories[dic['name']]['api url'] = dic['url']
    #             pprint.pprint(self.inventories)

    # def remove_bag_item(self, item):
    #     del self.inventories[item]

    # Converts base currency unit cp to gp:sp:cp format and returns in a dictionary.
    def convert_currency(self):
        amount_in_cp = self.currency
        g = int(amount_in_cp / 100)
        s = int(round((((amount_in_cp / 100) - g) * 10), 2))
        c = int(round((((((amount_in_cp / 100) - g) * 10) - s) * 10), 2))
        converted_dict = {'gp': g, 'sp': s, 'cp': c}
        return converted_dict

    # Gets item price info and adds/subtracts it to/from currency dictionary based on [unit] key.
    # See convert_price_info in search.py for more information on conversion.
    def sell_item(self, item):
        value = convert_price_info(get_price_info(item))
        self.currency += value

    def buy_item(self, item):
        value = convert_price_info(get_price_info(item))
        if value > self.currency:
            print('not enough currency')

        else:
            print('---item bought---')  # TODO Remove later
            self.currency -= value


class Inventory:
    def __init__(self, inventory_id, name):
        self.id = inventory_id
        self.name = name


# Creates new admin account. Adds information to accounts table in database.
def user_creates_admin_account():
    print('create name')
    dm_name = input()
    print('create password')
    password = input()
    connection = create_connection()
    with connection:
        account_info = (dm_name, password, True)
        add_account_row(connection, account_info)

# Creates new user account. Adds information to accounts table in database.
def user_creates_user_account():
    # print('Name player')
    # player_name = input()
    # print('create password')
    # password = input()
    # Currency Dictionary starts at 0 on all values.       # TODO Update to DM account creation standards
    player = Character('bob', 'tree53', False, {}, 13260, False)     # TODO change back to user input and 0 currency
    return player                                          # TODO Local dict and DB dump


# Loads all account username/password information and stores as key:value pairs in lof_in_dict.
def load_account_archive():
    connection = create_connection()
    with connection:
        a = query_username_password(connection)
        for i in a:
            Account.log_in_dic[i[0]] = i[1]


# Requests username/password from user. Returns username if authenticated
def log_in():
    load_account_archive()  # Loads account info for authentication.
    print('enter username')
    username = input()
    print('enter password')
    password = input()
    if username in Account.log_in_dic and Account.log_in_dic[username] == password:
        print('Welcome: ' + username)
        return username


# query ALL account information from accounts table based on username. Returns Account object based on query.
def load_account_object(username):
    connection = create_connection()
    with connection:
        p1_info = query_account_row(connection, username)
        acc = Account(p1_info[0], p1_info[1], p1_info[2], p1_info[3])
        return acc



# # Creates new account.
# def user_creates_account():
#     print('create name')
#     name = input()
#     print('create password')
#     password = input()
#     print('DM or player?')
#     role = input()
#     account = Account(name, password, role)
#     return account

# Adds DM account object as row in accounts table of test.db as well as account_dict.
# if __name__ == '__main__':
#     p1 = user_creates_dm_account()
#     p1.add_account()
#     connection = create_connection()
#     with connection:
#         account = (p1.name, p1.password, p1.role)
#         print(add_account_row(connection, account))


if __name__ == '__main__':
    p1 = Player('bob', 5000, [], False)
    p1.add_item_dict('Club')