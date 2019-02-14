import testing.database
import testing.sql
import testing.stores
import testing.api


db = 'C:\\sqlite\\db\\test.db'
mem = ':memory:'


# TODO consider refactoring to a single .executemany()
# Four sqlite statements which create the database schema.
def create_schema():
    con = testing.database.create_connection(db)
    with con:
        # accounts = """CREATE TABLE IF NOT EXISTS accounts (
        #        id integer PRIMARY KEY,
        #        username varchar NOT NULL,
        #        password varchar NOT NULL);"""
        #
        # characters = """CREATE TABLE IF NOT EXISTS characters (
        #        id integer PRIMARY KEY,
        #        account_id integer,
        #        name text,
        #        currency integer,
        #        FOREIGN KEY (account_id) REFERENCES accounts (id));"""
        #
        # inventories = """CREATE TABLE IF NOT EXISTS inventories (
        #        id integer PRIMARY KEY,
        #        character_id integer,
        #        name text,
        #        FOREIGN KEY (character_id) REFERENCES characters (id));"""
        #
        # items = """CREATE TABLE IF NOT EXISTS items (
        #        id integer PRIMARY KEY,
        #        inventory_id integer,
        #        item text,
        #        api varchar,
        #        quantity integer,
        #        store text,
        #        FOREIGN KEY (inventory_id) REFERENCES inventories (id));"""

        testing.sql.execute_sql(con, testing.sql.sql_accounts_table())
        testing.sql.execute_sql(con, testing.sql.sql_characters_table())
        testing.sql.execute_sql(con, testing.sql.sql_inventories_table())
        testing.sql.execute_sql(con, testing.sql.sql_items_table())


# Verifies database setup correctly
def wrong_schema():
    schema = ['accounts', 'characters', 'inventories', 'items']
    con = testing.database.create_connection(db)
    with con:
        schema.sort()
        cur_tables = []
        tables = testing.sql.execute_fetchall_sql(con, testing.sql.sql_check_table_schema())
        for t in tables:
            for i in t:
                cur_tables.append(i)
        cur_tables.sort()
        if cur_tables == schema:
            return False
        else:
            return True


# TODO comment this shit.
# TODO refactor to use new api methods
def stock_stores():
    store_dict = testing.stores.stores()
    conn = testing.database.create_connection(db)
    with conn:
        url = testing.api.make_api_url('equipment')
        response = testing.api.call_api(url)
        response_dict = testing.api.get_api_all(response)
        usable_dict = testing.api.get_nested_api_dict(response_dict, 'results')
        for dic in usable_dict:
            temp = []
            for k, v in dic.items():
                temp.append(v)
                if v[0:37] == url:
                    num = testing.api.regex(v, 'equipment/')
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
            testing.database.add_store_item(conn, temp)


if __name__ == '__main__':
    create_schema()
    if wrong_schema():
        print('Wrong schema')
    stock_stores()
