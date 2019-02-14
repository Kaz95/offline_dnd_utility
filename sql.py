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
               character_id integer,
               name text,
               FOREIGN KEY (character_id) REFERENCES characters (id));"""


def sql_items_table():
    return """CREATE TABLE IF NOT EXISTS items (
               id integer PRIMARY KEY,
               inventory_id integer,
               item text,
               api varchar,
               quantity integer,
               store text,
               FOREIGN KEY (inventory_id) REFERENCES inventories (id));"""


def sql_check_table_schema():
    return "SELECT name FROM sqlite_master WHERE type='table';"

# INSERT


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
