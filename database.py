import sqlite3
from sqlite3 import Error


# Creates a connection to test.db
def create_connection():
    try:
        conn = sqlite3.connect('C:\\sqlite\\db\\test.db')
        return conn
    except Error as e:
        print(e)

    return None


# Verifies user ahs database setup correctly
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


def create_table(con, sql_statement):
    cur = con.cursor()
    cur.execute(sql_statement)


def create_schema():
    con = create_connection()
    with con:
        k = """CREATE TABLE IF NOT EXISTS accounts (
               id integer PRIMARY KEY,
               username varchar NOT NULL,
               password varchar NOT NULL); """
               
        a = """CREATE TABLE IF NOT EXISTS characters (
               id integer PRIMARY KEY,
               account_id integer,
               name text,
               currency integer,
               FOREIGN KEY (account_id) REFERENCES accounts (id));"""
               
        b = """CREATE TABLE IF NOT EXISTS inventories (
               id integer PRIMARY KEY,
               character_id integer,
               name text,
               FOREIGN KEY (character_id) REFERENCES characters (id));"""
               
        c = """CREATE TABLE IF NOT EXISTS items (
               id integer PRIMARY KEY,
               inventory_id integer,
               item text,
               api varchar,
               quantity integer,
               store text,
               FOREIGN KEY (inventory_id) REFERENCES inventories (id));"""

        create_table(con, k)
        create_table(con, a)
        create_table(con, b)
        create_table(con, c)


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


def count_rows(conn, where):
    conn = create_connection()
    with conn:
        k = """SELECT count(*) FROM inventories WHERE character_id = ?;"""
        cur = conn.cursor()
        cur.execute(k)
        yup = cur.fetchone()
        print(yup)
