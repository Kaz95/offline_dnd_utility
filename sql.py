# required for a mock
import sqlite3
# TODO: Consider removing sql from beginning of each function. It's redundant.
# TODO: Consider creating common naming scheme among all statements.
# TODO: Consider what could be more DRY.

# TODO: Refactor sql statements to adhere to new code style guide.
# TODO: This will require manually refactoring.....a lot of tests and manual regression testing...Be prepared.


# Modular sqlite execute functions which are passed a connection and some sql
def execute_sql(con, sql_statement, *args):
    cur = con.cursor()
    cur.execute(sql_statement, args)
    con.commit()


def execute_fetchone_sql(con, sql_statement, *args):
    cur = con.cursor()
    cur.execute(sql_statement, args)
    return cur.fetchone()


def execute_fetchall_sql(con, sql_statement, *args):
    cur = con.cursor()
    cur.execute(sql_statement, args)
    return cur.fetchall()


# SQL statements


# CREATE TABLE
def sql_accounts_table():
    return """CREATE TABLE IF NOT EXISTS accounts (
               id integer PRIMARY KEY,
               username varchar NOT NULL,
               password varchar NOT NULL);"""


def sql_characters_table():
    return """CREATE TABLE IF NOT EXISTS characters (
               id integer PRIMARY KEY,
               account_id integer,
               name text,
               currency integer,
               FOREIGN KEY (account_id) REFERENCES accounts (id));"""


def sql_inventories_table():
    return """CREATE TABLE IF NOT EXISTS inventories (
               id integer PRIMARY KEY,
               account_id integer,
               character_id integer,
               name text,
               FOREIGN KEY (account_id) REFERENCES accounts (id),
               FOREIGN KEY (character_id) REFERENCES characters(id));"""


def sql_items_table():
    return """CREATE TABLE IF NOT EXISTS items (
               id integer PRIMARY KEY,
               account_id,
               character_id,
               inventory_id integer,
               item text,
               api varchar,
               unit_value,
               quantity integer,
               store text,
               FOREIGN KEY (account_id) REFERENCES accounts (id),
               FOREIGN KEY (character_id) REFERENCES characters (id),
               FOREIGN KEY (inventory_id) REFERENCES inventories (id));"""


# Query all table names. Used to check if tables have been created during install.
# TODO: Test
def sql_check_table_schema():
    return "SELECT name FROM sqlite_master WHERE type='table';"


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
    return """SELECT id, name, currency FROM characters WHERE account_id = ?;"""


def sql_accounts_with_characters():
    return """SELECT DISTINCT account_id FROM characters;"""


def sql_characters_with_inventories():
    return """SELECT DISTINCT character_id FROM inventories;"""


# TODO: Test
def sql_characters_inventory_ids():
    return """SELECT id FROM inventories WHERE character_id = ?;"""


def sql_all_inventory_names():
    return """SELECT name FROM inventories WHERE character_id = ?;"""


def sql_query_accounts_with_characters():
    return """SELECT DISTINCT account_id FROM characters;"""


def sql_query_items_in_inventory():
    return """SELECT item, quantity FROM items WHERE inventory_id = ?"""


def sql_item_quantity():
    return """SELECT quantity FROM items where item = ? AND inventory_id = ?"""


# TODO: Test
def sql_item_from_store():
    return """SELECT id, item, unit_value FROM items WHERE id = ? AND store = ?;"""


# TODO: Test
def sql_character_currency():
    return """SELECT currency FROM characters WHERE id = ?"""


# TODO: Test
def sql_all_character_names():
    return """SELECT name FROM characters;"""


# TODO: Test
def sql_all_character_items():
    return """SELECT item, quantity FROM items WHERE character_id = ?;"""


# TODO: Test
def sql_store_item_value():
    return """SELECT unit_value FROM items WHERE item = ? AND quantity IS NULL;"""


# TODO: Test
def sql_store_item_url():
    return """SELECT api FROM items WHERE item = ? AND quantity IS NULL;"""


# Delete
# TODO: This could be refactored to always use character_id as WHERE. Only table changes in current use.
def sql_delete_all(table, where):
    return """DELETE FROM {} WHERE {} = ?""".format(table, where)


def sql_delete_item():
    return """DELETE FROM items WHERE item = ? AND inventory_id = ?"""


# INSERT

def sql_add_item_row():
    return """INSERT INTO items (account_id, character_id, inventory_id, item, api, unit_value, quantity)
            VALUES(?,?,?,?,?,?,?)"""


def sql_add_account_row():
    return """INSERT INTO accounts (username, password)
            VALUES(?,?)"""


def sql_add_inventory_row():
    return """INSERT INTO inventories (account_id, character_id, name)
            VALUES(?,?,?)"""


def sql_add_character_row():
    return """INSERT INTO characters (account_id, name, currency)
            VALUES(?,?,?)"""


def sql_add_store_item():
    return """INSERT INTO items (item, api, unit_value, store)
             VALUES(?,?,?,?)"""


def sql_count_rows():
    return """SELECT count(*) FROM {};"""


# Update

def update_quantity():
    return """UPDATE items SET quantity = ? WHERE item = ? AND inventory_id = ?"""


# TODO: Test
def update_currency():
    return """UPDATE characters SET currency = ? WHERE id = ?"""

