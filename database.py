import sqlite3
from sqlite3 import Error
from stores import stores
from search import regex
import json
import requests
from tkinter import *


# Creates a connection to test.db
def create_connection():
    try:
        conn = sqlite3.connect('C:\\sqlite\\db\\test.db')
        return conn
    except Error as e:
        print(e)

    return None


# Verifies database setup correctly
def wrong_schema():
    schema = ['accounts', 'characters', 'inventories', 'items']
    con = create_connection()
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
    con = create_connection()
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
def create_table(con, sql_statement):
    cur = con.cursor()
    cur.execute(sql_statement)


# TODO consider refactoring to a single .executemany()
# Four sqlite statements which create the database schema.
def create_schema():
    con = create_connection()
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

        create_table(con, accounts)
        create_table(con, characters)
        create_table(con, inventories)
        create_table(con, items)


# TODO Refactor ALL THIS SHIT to use what is currently create_table().
# Inserts given values into accounts table at given columns. Returns last row id.
def add_account_row(conn, some_account):
    k = """INSERT INTO accounts (username, password)
            VALUES(?,?)"""
    cursor = conn.cursor()
    cursor.execute(k, some_account)
    # return cursor.lastrowid


# Inserts given values into accounts table at given columns. Returns last row id.
def add_inventory_row(conn, some_inventory):
    k = """INSERT INTO inventories (character_id, name)
            VALUES(?,?)"""
    cursor = conn.cursor()
    cursor.execute(k, some_inventory)


# Inserts given values into accounts table at given columns. Returns last row id.
def add_character_row(conn, some_character):
    k = """INSERT INTO characters (account_id, name, currency)
            VALUES(?,?,?)"""
    cursor = conn.cursor()
    cursor.execute(k, some_character)


# Inserts given values into accounts table at given columns. Returns last row id.
def add_item_row(conn, some_character):
    k = """INSERT INTO items (inventory_id, item, api, quantity)
            VALUES(?,?,?,?)"""
    cursor = conn.cursor()
    cursor.execute(k, some_character)


# Used to populate stores
def add_store_item(con, item_info):
    sql = '''INSERT INTO items(item, api, store)
             VALUES(?,?,?)'''
    cur = con.cursor()
    cur.execute(sql, item_info)


def query_username_password(conn):
    k = """SELECT username, password FROM accounts;"""
    cursor = conn.cursor()
    cursor.execute(k)
    some_account = cursor.fetchall()
    return some_account


def query_account_row(conn, username):
    k = """SELECT id, username, password FROM accounts WHERE username = ?;"""
    cursor = conn.cursor()
    cursor.execute(k, [username])
    some_account = cursor.fetchone()
    return list(some_account)


def query_character_row(conn, character_name):
    k = """SELECT id, name, currency FROM characters WHERE name = ?;"""
    cursor = conn.cursor()
    cursor.execute(k, [character_name])
    some_account = cursor.fetchone()
    return list(some_account)


def query_inventory_row(conn, inventory_name):
    k = """SELECT id, name FROM inventories WHERE name = ?;"""
    cursor = conn.cursor()
    cursor.execute(k, [inventory_name])
    some_account = cursor.fetchone()
    return list(some_account)


def query_all_characters(conn, account_id):
    k = """SELECT name, currency FROM characters WHERE account_id = ?;"""
    cursor = conn.cursor()
    cursor.execute(k, [account_id])
    some_account = cursor.fetchall()
    for character in some_account:
        print(list(character))


def query_accounts_with_characters(conn):
    temp = []
    k = """SELECT DISTINCT account_id FROM characters;"""
    cursor = conn.cursor()
    cursor.execute(k)
    account_id_list = cursor.fetchall()
    for tup in account_id_list:
        temp.append(tup[0])
    return temp


def query_characters_with_inventories(conn):
    temp = []
    k = """SELECT DISTINCT character_id FROM inventories;"""
    cursor = conn.cursor()
    cursor.execute(k)
    account_id_list = cursor.fetchall()
    for tup in account_id_list:
        temp.append(tup[0])
    return temp


def query_all_inventories(conn, character_id):
    k = """SELECT name FROM inventories WHERE character_id = ?;"""
    cursor = conn.cursor()
    cursor.execute(k, [character_id])
    some_account = cursor.fetchall()
    for character in some_account:
        print(list(character))


# TODO Figure out what this is.
def count_rows(conn, some_table):
    ka = """SELECT count(*) FROM {};""".format(some_table)
    cur = conn.cursor()
    cur.execute(ka)
    yup = cur.fetchone()
    return yup[0]


# TODO comment this shit.
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
