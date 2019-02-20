import database
import sql
import stores
import api
import sqlite3


db = 'C:\\sqlite\\db\\test.db'
mem = ':memory:'


# TODO consider refactoring to a single .executemany()
# Four sqlite statements which create the database schema.
def create_schema(conn):
    with conn:
        sql.execute_sql(conn, sql.sql_accounts_table())
        sql.execute_sql(conn, sql.sql_characters_table())
        sql.execute_sql(conn, sql.sql_inventories_table())
        sql.execute_sql(conn, sql.sql_items_table())


# Verifies database setup correctly
# You want a False return
def wrong_schema(conn):
    schema = ['accounts', 'characters', 'inventories', 'items']
    with conn:
        schema.sort()
        cur_tables = []
        tables = sql.execute_fetchall_sql(conn, sql.sql_check_table_schema())
        for t in tables:
            for i in t:
                cur_tables.append(i)
        cur_tables.sort()
        if cur_tables == schema:
            return False
        else:
            return True


def stock_stores(conn):
    store_dict = stores.stores()    # {'some_store':[1,2,3,4,5]} Used to tell which items in which stores - ints are ids
    with conn:
        url = api.make_api_url('equipment')
        response = api.call_api(url)
        response_dict = api.get_api_all(response)
        usable_dict = api.get_nested_api_dict(response_dict, 'results')  # [{'name': 'some_name', 'url': 'some_url'}]
        for dic in usable_dict:
            temp = {}
            for k, v in dic.items():
                if not temp:    # If temp dictionary is empty
                    temp['item'] = v    # add value with key 'item'
                else:
                    temp['api'] = v     # add value with key 'api'
                if v[0:37] == url:  # if one of those values beings with a url like string
                    num = api.regex(v, 'equipment/')    # slices number off url and captures as variable

                    # This logic compares the captured number to the numbers in the dict imported earlier
                    # Then it adds a 'store':'some_store' key:value to the temp dictionary
                    if num in store_dict['GS']:
                        temp['store'] = 'General Store'
                    elif num in store_dict['BS']:
                        temp['store'] = 'Blacksmith'
                    elif num in store_dict['Ship']:
                        temp['store'] = 'Shipyard'
                    elif num in store_dict['Stables']:
                        temp['store'] = 'Stables'
                    else:
                        temp['store'] = 'No Store'

            # adds an item to a store table based on information stored in dictionary
            database.add_store_item(conn, sql.sql_add_store_item(), temp)


if __name__ == '__main__':
    con = database.create_connection(db)
    create_schema(con)
    if wrong_schema(con):
        print('Wrong schema')
    stock_stores(con)
