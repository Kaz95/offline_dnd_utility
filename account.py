# !/usr/bin/python
from search import search
from search import get_price_info
from search import convert_price_info
from database import create_connection
from database import query_account_row
from database import query_username_password
from database import add_account_row


# Account class
class Account:
    log_in_dic = {}

    def __init__(self, acc_id, name, password):
        self.id = acc_id
        self.name = name    # Username
        self.password = password    # Password


# Player Class
class Player:
    def __init__(self, player_id, name, currency, inventories):
        self.id = player_id
        self.currency = currency    # All currency held in cp. cp is then formatted via convert_currency() before view.
        self.name = name  # Character(DM) name.
        self.inventories = inventories  # Character(DM) Inventories(Stores)

    # Inventory management

    def add_item(self, inventory, some_item):
        item = search(some_item)  # Search returns ['Item', 'api url']
        self.inventories[inventory][item[0]] = item[1]  # Adds above to inventory dictionary as key:value pair

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
def user_creates_account():
    print('create name')
    username = input()
    print('create password')
    password = input()
    connection = create_connection()
    with connection:
        account_info = (username, password)
        add_account_row(connection, account_info)


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
        acc = Account(p1_info[0], p1_info[1], p1_info[2])
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