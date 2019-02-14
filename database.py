import sqlite3
from sqlite3 import Error
from stores import stores
from api import regex
import json
import requests
db = 'C:\\sqlite\\db\\test.db'
mem = ':memory:'


# TODO refactor to not hard code database path. Will not work for others trying to use codebase.
# Creates a connection to test.db
def create_connection(db_path):
    try:
        conn = sqlite3.connect(db_path)
        return conn
    except Error as e:
        print(e)
    return None


# Verifies database setup correctly
def wrong_schema():
    schema = ['accounts', 'characters', 'inventories', 'items']
    con = create_connection(mem)
    with con:
        schema.sort()
        cur_tables = []
        cursor = con.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        for t in tables:
            for i in t:
                cur_tables.append(i)
        cur_tables.sort()
        if cur_tables == schema:
            return False
        else:
            return True


# Verifies store item count via sqlite count(*) method which returns row count for a given table.
# Not currently used.
def wrong_item_count():
    store_item_count = 256
    con = create_connection(mem)
    with con:
        cursor = con.cursor()
        cursor.execute("SELECT count(*) FROM items;")
        cur_item_count = cursor.fetchone()
        cur_item_count = cur_item_count[0]
        if cur_item_count == store_item_count:
            return False
        else:
            return True


# TODO refactor name for reflect how reusable this chunk is.
# TODO consider refactoring into other database functions.


# Modular sqlite execute function which is passed a connection and some sql
def execute_sql(con, sql_statement, *args):
    cur = con.cursor()
    cur.execute(sql_statement, args)


def execute_fetchone_sql(con, sql_statement, *args):
    cur = con.cursor()
    cur.execute(sql_statement, args)
    return cur.fetchone()


def execute_fetchall_sql(con, sql_statement, *args):
    cur = con.cursor()
    cur.execute(sql_statement, args)
    return cur.fetchall()


# SQL statements


# QUERY
def sql_username_password():
    return """SELECT username, password FROM accounts;"""


def sql_account_row():
    return """SELECT id, username, password FROM accounts WHERE username = ?;"""


def sql_character_row():
    return """SELECT id, name, currency FROM characters WHERE name = ?;"""


def sql_inventory_row():
    return """SELECT id, name FROM inventories WHERE name = ?;"""


def sql_all_characters():
    return """SELECT name, currency FROM characters WHERE account_id = ?;"""


def sql_accounts_with_characters():
    return """SELECT DISTINCT account_id FROM characters;"""


def sql_characters_with_inventories():
    return """SELECT DISTINCT character_id FROM inventories;"""


def sql_all_inventories():
    return """SELECT name FROM inventories WHERE character_id = ?;"""

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


# TODO consider refactoring to a single .executemany()
# TODO consider decoupling sql statements to improve encapsulation
# Four sqlite statements which create the database schema.
def create_schema():
    con = create_connection(mem)
    with con:
        accounts = """CREATE TABLE IF NOT EXISTS accounts (
               id integer PRIMARY KEY,
               username varchar NOT NULL,
               password varchar NOT NULL); """

        characters = """CREATE TABLE IF NOT EXISTS characters (
               id integer PRIMARY KEY,
               account_id integer,
               name text,
               currency integer,
               FOREIGN KEY (account_id) REFERENCES accounts (id));"""

        inventories = """CREATE TABLE IF NOT EXISTS inventories (
               id integer PRIMARY KEY,
               character_id integer,
               name text,
               FOREIGN KEY (character_id) REFERENCES characters (id));"""

        items = """CREATE TABLE IF NOT EXISTS items (
               id integer PRIMARY KEY,
               inventory_id integer,
               item text,
               api varchar,
               quantity integer,
               store text,
               FOREIGN KEY (inventory_id) REFERENCES inventories (id));"""

        execute_sql(con, accounts)
        execute_sql(con, characters)
        execute_sql(con, inventories)
        execute_sql(con, items)


# INSERT

# Inserts given values into accounts table at given columns. Returns last row id.
def add_account_row(conn, some_account):
    sql = """INSERT INTO accounts (username, password)
            VALUES(?,?)"""

    execute_sql(conn, sql, some_account[0], some_account[1])
    # cursor = conn.cursor()
    # cursor.execute(sql, some_account)
    return sql


# Inserts given values into accounts table at given columns. Returns last row id.
def add_inventory_row(conn, some_inventory):
    sql = """INSERT INTO inventories (character_id, name)
            VALUES(?,?)"""
    execute_sql(conn, sql, some_inventory[0], some_inventory[1])
    return sql


# Inserts given values into accounts table at given columns. Returns last row id.
def add_character_row(conn, some_character):
    sql = """INSERT INTO characters (account_id, name, currency)
            VALUES(?,?,?)"""
    execute_sql(conn, sql, some_character[0], some_character[1], some_character[2])
    return sql


# Inserts given values into accounts table at given columns. Returns last row id.
def add_item_row(conn, some_item):
    sql = """INSERT INTO items (inventory_id, item, api, quantity)
            VALUES(?,?,?,?)"""
    execute_sql(conn, sql, some_item[0], some_item[1], some_item[2], some_item[3])
    return sql


# Used to populate stores
def add_store_item(con, item_info):
    sql = """INSERT INTO items (item, api, store)
             VALUES(?,?,?)"""
    execute_sql(con, sql, item_info[0], item_info[1], item_info[2])
    return sql


# QUERY

def query_username_password(conn, sql):
    # sql = """SELECT username, password FROM accounts;"""
    some_account = execute_fetchall_sql(conn, sql)
    return some_account


def query_account_row(conn, sql, username):
    # sql = """SELECT id, username, password FROM accounts WHERE username = ?;"""
    some_account = execute_fetchone_sql(conn, sql, username)
    return list(some_account)


def query_character_row(conn, sql, character_name):
    # sql = """SELECT id, name, currency FROM characters WHERE name = ?;"""
    some_account = execute_fetchone_sql(conn, sql, character_name)
    return list(some_account)


def query_inventory_row(conn, sql, inventory_name):
    # sql = """SELECT id, name FROM inventories WHERE name = ?;"""
    some_account = execute_fetchone_sql(conn, sql, inventory_name)
    return list(some_account)


def query_all_characters(conn, sql, account_id):
    # sql = """SELECT name, currency FROM characters WHERE account_id = ?;"""
    some_account = execute_fetchall_sql(conn, sql, account_id)
    for character in some_account:
        print(list(character))


# TODO test
def query_accounts_with_characters(conn, sql):
    temp = []
    # sql = """SELECT DISTINCT account_id FROM characters;"""
    account_id_list = execute_fetchall_sql(conn, sql)
    for tup in account_id_list:
        temp.append(tup[0])
    return temp


# TODO test
def query_characters_with_inventories(conn,  sql):
    temp = []
    # sql = """SELECT DISTINCT character_id FROM inventories;"""
    account_id_list = execute_fetchall_sql(conn, sql)
    for tup in account_id_list:
        temp.append(tup[0])
    return temp


def query_all_inventories(conn, sql, character_id):
    # sql = """SELECT name FROM inventories WHERE character_id = ?;"""
    some_account = execute_fetchall_sql(conn, sql, character_id)
    for character in some_account:
        print(list(character))


# SELECT

# TODO decouple sql and test....maybe?
def count_rows(conn, some_table):
    sql = """SELECT count(*) FROM {};""".format(some_table)
    yup = execute_fetchone_sql(conn, sql)
    return yup[0]


# TODO comment this shit.
# TODO refactor to use new api methods
def stock_stores():
    store_dict = stores()
    conn = create_connection(db)
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
                    num = regex(v, 'equipment/')
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


# if __name__ == '__main__':
#     acc = ('username', 'password')
#     inv = (1, 'inv name')
#     char = (1, 'char name', 420)
#     item = (1, 'item name', 'api url', 1)
#     con = create_connection(db)
#     with con:
#         print(add_account_row(con, acc))
#         add_inventory_row(con, inv)
#         add_character_row(con, char)
#         add_item_row(con, item)
#
#         print(query_username_password(con, sql_username_password()))
#         print(query_account_row(con, sql_account_row(), 'Kazact'))
#         print(query_character_row(con, sql_character_row(), 'char name'))
#         print(query_inventory_row(con, sql_inventory_row(), 'Kazact'))
#         print(query_all_characters(con, sql_all_characters(), '1'))
#         print(query_accounts_with_characters(con, sql_accounts_with_characters()))
#         print(query_characters_with_inventories(con, sql_characters_with_inventories()))
#         print(query_all_inventories(con, sql_all_inventories(), 1))
#         print(count_rows(con, 'items'))
#     # # stock_stores()
