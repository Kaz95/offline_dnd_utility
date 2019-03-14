import database
import sql
import stores
import api
import character
import time
import threading


# TODO: May be required for mock. Not sure atm.
import sqlite3

db = 'C:\\sqlite\\db\\test.db'
mem = ':memory:'


# TODO consider refactoring to a single .executemany()
# TODO: Test
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
        tables_tup_list = sql.execute_fetchall_sql(conn, sql.sql_check_table_schema())
        for tup in tables_tup_list:
            for index in tup:
                cur_tables.append(index)
        cur_tables.sort()
        if cur_tables == schema:
            return False
        else:
            return True


# Updates value of progress bar.
# TODO: Refactor: Name
def update(some_bar, count):
    some_bar['value'] = count
    # print(some_bar['value'])
    time.sleep(.05)
    some_bar.update_idletasks()


# TODO: Refactor: Variable Names
# Stocks stores on initial installation. Also keeps track of progress and updates the progress bar on sister thread.
def stock_stores(conn, some_bar, count, window):
    t = time.time()
    global max_count
    store_dict = stores.stores()    # {'some_store':[1,2,3,4,5]} Used to tell which items in which stores - ints are ids
    with conn:
        url = api.make_api_url('equipment')
        response = api.call_api(url)
        response_dict = api.get_api_all(response)
        usable_dict = api.get_nested_api_dict(response_dict, 'results')  # [{'name': 'some_name', 'url': 'some_url'}]
        max_count = api.get_nested_api_dict(response_dict, 'count')
        print(count)
        for dic in usable_dict:
            temp = {}
            for k, v in dic.items():
                if not temp:    # If temp dictionary is empty
                    temp['item'] = v    # add value with key 'item'
                else:
                    temp['api'] = v     # add value with key 'api'

                item_value = api.get_item_value(temp['item'], character.Character.list_of_item_dicts)
                temp['currency'] = item_value

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
            count += 1
            print(count)
            window.after(10, update(some_bar, count))
        # print(count)
        print('done in: ', time.time() - t)
        print('Done with everything.')


# def fake_api():
#     global fake_items
#     global done
#     for i in range(256):
#         fake_item = {'item': 'item', 'api': 'api', 'currency': i + 1, 'store': 'store'}
#         fake_items.append(fake_item)
#         time.sleep(.2)
#         print(fake_items)
    # done = True


# def add_but_check():
#     global fake_items
#     global done
#     print('============')
#     conn = database.create_connection(db)
#     while True:
#         print(fake_items)
#         if len(fake_items) != 0:
#             print('============')
            # database.add_store_item(conn, sql.sql_add_store_item(), fake_items[0])
            # fake_items.pop(0)
            # print(fake_items)
        # if done:
        #     break


# if __name__ == '__main__':
#     fake_items = []
#     done = False
#     conn = database.create_connection(db)
#     create_schema(conn)
    # t = time.time()
    # t1 = threading.Thread(target=fake_api)
    # t2 = threading.Thread(target=add_but_check)
    # t1.start()
    # t2.start()
    # t1.join()
    # t2.join()

    # print('done in: ', time.time() - t)
    # print('Done with everything.')
