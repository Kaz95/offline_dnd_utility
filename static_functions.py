import database
import sql


# Checks if given entry input is alphanumerical.
# Return True if is alpha or empty string.
# Else return false.
def entry_is_alnum_callback(entry_input):
    if entry_input.isalnum():
        return True
    elif entry_input is '':
        return True
    else:
        return False


# Checks if given entry input is alphabetical.
# Return True if is alpha or empty string.
# Else return false.
def entry_is_alpha_callback(entry_input):
    if entry_input.isalpha():
        return True
    elif entry_input is '':
        return True
    else:
        return False


# Checks if given entry input is digit.
# Return True if is digit or empty string.
# Else return false.
def entry_is_digit_callback(entry_input):
    if entry_input.isdigit():
        return True
    elif entry_input is '':
        return True
    else:
        return False


# Generic function that is passed a tkinter entry box and clears its current contents.
def clear_entry(some_entry):
    some_entry.delete(0, 'end')


# TODO: There is probably a more efficient way to write this.
def convert_currency(currency):
    g = int(currency / 100)
    s = int(round((((currency / 100) - g) * 10), 2))
    c = int(round((((((currency / 100) - g) * 10) - s) * 10), 2))
    converted_dict = {'gp': g, 'sp': s, 'cp': c}
    return converted_dict


# Searches a currency dictionary and returns key with value not equal to zero.
def inspecto_gadget(converted_value):
    for key, value in converted_value.items():
        if value != 0:
            return key


# Tags a treeview items with a given img tag based on currency type.
def img_tag(some_tree, some_item, cur_type):
    if cur_type == 'gp':
        some_tree.item(some_item, tags='gold')
    elif cur_type == 'sp':
        some_tree.item(some_item, tags='silver')
    elif cur_type == 'cp':
        some_tree.item(some_item, tags='copper')


# Query all items from a given store. Use values returned to populate store treeviews.
def populate_tree(some_sql, conn, some_tree, some_store):
    for number in range(database.count_rows(conn, sql.count_table_rows(), 'items')):
        temp_dict = {}
        number += 1
        item_info_tuple = sql.execute_fetchone_sql(conn, some_sql, str(number), some_store)
        try:
            temp_dict['id'] = item_info_tuple[0]
            temp_dict['name'] = item_info_tuple[1]
            temp_dict['value'] = item_info_tuple[2]
            converted_value = convert_currency(temp_dict['value'])
            cur_type = inspecto_gadget(converted_value)
            some_tree.insert('', 'end', temp_dict['id'], text=temp_dict['name'])

            img_tag(some_tree, temp_dict['id'], cur_type)

            some_tree.set(temp_dict['id'], 'price', converted_value[cur_type])

        # TODO: Consider better error handling. This is a silent pass. Not good.
        except TypeError:
            continue
