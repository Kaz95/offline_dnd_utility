import database
import sql
import stores
import api
import character
import time
import sys

# TODO: May be required for mock. Not sure atm.
import sqlite3


# TODO consider refactoring to a single .executemany()
# TODO: Test
# Four sqlite statements which create the database schema.
def create_schema(conn):
    sql.execute_sql(conn, sql.create_accounts_table())
    sql.execute_sql(conn, sql.create_characters_table())
    sql.execute_sql(conn, sql.create_inventories_table())
    sql.execute_sql(conn, sql.create_items_table())


# Verifies database setup correctly
# You want a False return
def wrong_schema(conn):
    schema = ['accounts', 'characters', 'inventories', 'items']
    schema.sort()
    cur_tables = []
    tables_tup_list = sql.execute_fetchall_sql(conn, sql.check_table_schema())
    for tup in tables_tup_list:
        for index in tup:
            cur_tables.append(index)
    cur_tables.sort()
    if cur_tables == schema:
        return False
    else:
        return True


# Updates value of progress bar.
def update_mainloop(some_bar, count, some_label, window, canceled):
    percent = round((count/256) * 100)

    some_label.config(text=f'Installing....{percent}%')
    some_bar['value'] = count
    time.sleep(.05)
    if not canceled:
        some_bar.update_idletasks()
    else:
        window.quit()
        sys.exit()


# Stocks stores on initial installation. Also keeps track of progress and updates the progress bar on sister thread.
def stock_stores(conn, some_bar, window, some_label, some_queue):
    canceled = False
    count = 0
    time_to_install = time.time()
    store_dict = stores.stores()    # {'some_store':[1,2,3,4,5]} Used to tell which items in which stores - ints are ids
    url = api.construct_api_url('equipment')
    s = api.create_session()
    response = api.call_api(url, s)
    response_dict = api.get_api_all(response)
    usable_dict = api.get_nested_api_dict(response_dict, 'results')  # [{'name': 'some_name', 'url': 'some_url'}]
    for dic in usable_dict:
        temp = {}
        for key, value in dic.items():
            if not temp:    # If temp dictionary is empty
                temp['item'] = value    # add value with key 'item'
            else:
                temp['api'] = value     # add value with key 'api'

            item_value = api.get_item_value(temp['item'], character.Character.list_of_item_dicts, s)
            temp['currency'] = item_value

            if value[0:37] == url:  # if one of those values beings with a url like string
                num = api.regex(value, 'equipment/')    # slices number off url and captures as variable

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
        database.add_store_item(conn, sql.add_store_item(), temp)
        count += 1
        print(count)
        # TODO: Pass new canceled var that was just obtained from queue.
        if not some_queue.empty():
            canceled = some_queue.get()
        update_mainloop(some_bar, count, some_label, window, canceled)

    print('done in: ', time.time() - time_to_install)
    print('Done with everything.')

