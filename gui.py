from tkinter import *
from tkinter import ttk
from stores import stores
import sql
import account
import setup
import database
import character
import error_box
import threading

# TODO: Hasn't been tested.
# TODO: Refactor GUI to OOP.

# DB paths used for testing.
db = 'C:\\sqlite\\db\\test.db'
mem = ':memory:'

# Dictionary used to store account and character objects, representing the current user information.
user_info = {'acc': None, 'char': None, 'inv': 1}

# Empty Dictionary that is used to store cached inventory treeview items for later use.
# TODO: Verify structure stored in cache and provide comment example.
inv_cache = {}

# Dictionaries used to capture treeview selection events. Value will be a treeview item.
# TODO: Verify if item is stored as tuple or string and provide comment example
gen_selected = {'selected': 'none'}
bs_selected = {'selected': 'none'}
stable_selected = {'selected': 'none'}
ship_selected = {'selected': 'none'}
inv_selected = {'selected': 'none'}
recent_selection = {'selected': 'None'}

# Creates initial connection to test.db. Connection is then passed when necessary and used as context manager.
conn = database.create_connection(db)


# General Functions

# TODO: This is a copy of a function from character.py. Consider removing the other one.
# TODO: There is probably a more efficient way to write this.
def convert_currency(currency):
    g = int(currency / 100)
    s = int(round((((currency / 100) - g) * 10), 2))
    c = int(round((((((currency / 100) - g) * 10) - s) * 10), 2))
    converted_dict = {'gp': g, 'sp': s, 'cp': c}
    return converted_dict


# Gets recently selected treeview item as tuple.
# Tries to get name of item in each treeview. It will only work with one of them presumably.
# Query DB for item value based on name of item.
# Return Item value as integer.
def recent_select_value():
    item = recent_selection['selected']
    item_name = None
    try:
        item_name = general_store_treeview.item(item[0])['text']
    except TclError:
        pass

    try:
        item_name = blacksmith_treeview.item(item[0])['text']
    except TclError:
        pass

    try:
        item_name = stables_treeview.item(item[0])['text']
    except TclError:
        pass

    try:
        item_name = shipyard_treeview.item(item[0])['text']
    except TclError:
        pass

    item_value = sql.execute_fetchone_sql(conn, sql.sql_store_item_value(), item_name)
    # item_value = api.get_item_value(item_name, character.Character.list_of_item_dicts)    # Depricated API call
    return item_value[0]


# def treeview_select_value(some_treeview):
#     item = some_treeview.selection()
#     item_name = some_treeview.item(item[0])['text']
#     item_value = sql.execute_fetchone_sql(conn, sql.sql_store_item_value(), item_name)
#     # item_value = api.get_item_value(item_name, character.Character.list_of_item_dicts)    # Deppricated API call
#     return item_value[0]


# Changes activebackground color of buy button to a given color.
def change_button_background(color):
    buy.config(activebackground=color)


# Changes buy button activebackground color -
# based on if a character object's currency value is greater than a given item value.
def toggle_affordable_color(item_value):
    if item_value >= user_info['char'].currency:
        change_button_background('red')
    elif item_value < user_info['char'].currency:
        change_button_background('green')


# Gets item value of recent treeview selection and toggles button activebackground color based on that value.
def check_value_and_toggle():
    item_value = recent_select_value()
    toggle_affordable_color(item_value)


# Generic function that is passed a tuple with a single value.
# Value represents both the item_id (database) and the item id (tkinter gui).
# TODO: unit test with assertEqual
def new_selection(some_selection):
    recent_selection['selected'] = some_selection


# TODO: unit test with assertEqual.
# Clears dictionaries storing account information objects.
def log_out():
    print('-----Logged Out-----')
    user_info['acc'] = None
    user_info['char'] = None
    user_info['inv'] = None


# Query characters from DB based on current account id.
# Slices name from tuples returned and appends to empty list. Sets combo values to list.
# TODO: unit test assertEqual temp_combo_list.
def populate_combo():
    temp_combo_list = []
    acc_id = user_info['acc'].id
    characters_tuple = sql.execute_fetchall_sql(conn, sql.sql_all_characters(), acc_id)
    for thing in characters_tuple:
        temp_combo_list.append(thing[1])
    chars_combo['values'] = temp_combo_list


# Generic function that is passed a tkinter entry box and clears its current contents.
def clear_entry(some_entry):
    some_entry.delete(0, 'end')


# Callbacks
# Functions that capture most recent selection per widget as well as most recent across all treeview widgets.

def generic_selection_callback(event, some_dict, some_treeview):
    some_dict['selected'] = some_treeview.selection()
    new_selection(some_dict['selected'])


def shipyard_callback(event):
    # print(shipyard_treeview.selection())  # Gets tuple with id as first value
    # # print(treeview.set('I001', 'quantity'))
    # print(shipyard_treeview.item('I001'))
    # tup = shipyard_treeview.selection()
    # # Gets value of quantity for item selected.
    # # Quantity can be swapped for another column
    # print(shipyard_treeview.set(tup[0], 'quantity'))
    # print(shipyard_treeview.item(tup[0])['text'])   # Gets name of item selected
    # print(shipyard_treeview.selection())
    # check_value_and_toggle()
    generic_selection_callback(event, ship_selected, shipyard_treeview)
    check_value_and_toggle()


def general_store_callback(event):
    # check_value_and_toggle()
    generic_selection_callback(event, gen_selected, general_store_treeview)
    check_value_and_toggle()


def blacksmith_callback(event):
    # check_value_and_toggle()
    generic_selection_callback(event, bs_selected, blacksmith_treeview)
    check_value_and_toggle()


def stables_callback(event):
    # check_value_and_toggle()
    generic_selection_callback(event, stable_selected, stables_treeview)
    check_value_and_toggle()


# The inventory callback function also attempts to deselect all previously selections in store widgets.
def inventory_callback(event):
    # TODO: This is bugged. Toggle select causes unwanted behavior. Find a way to check if toggeled on.
    # try:
    #     blacksmith_treeview.selection_toggle(bs_selected['selected'])
    #     general_store_treeview.selection_toggle(gen_selected['selected'])
    #     stables_treeview.selection_toggle(stable_selected['selected'])
    #     shipyard_treeview.selection_toggle(ship_selected['selected'])
    # except TclError:
    #     pass

    generic_selection_callback(event, inv_selected, inventory_treeview)
    print(inventory_treeview.selection())
    print(inventory_treeview.item(inventory_treeview.selection(), 'text'))
    print(recent_selection['selected'])


# Checks if given entry input is alphanumeric.
# Return True if is alnum or empty string.
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


# Sets quantity column of a given (gui)item to 1.
def new_inventory_quantity(some_item):
    inventory_treeview.set(some_item, 'quantity', 1)


# Updates currency treeview based on a (presumably updated) currency dictionary.
def update_currency_treeview(some_dict):
    currency_treeview.item('gold',  text=some_dict['gp'])
    currency_treeview.set('gold', 'silver', some_dict['sp'])
    currency_treeview.set('gold', 'copper', some_dict['cp'])


# Adds 1 to a given (gui)item's quantity column value.
def add_one_inventory_quantity(some_item):
    quantity = inventory_treeview.set(some_item, 'quantity')
    quantity += 1
    inventory_treeview.set(some_item, 'quantity', quantity)


# Subtracts 1 to a given (gui)item's quantity column value.
def minus_one_inventory_quantity(some_item):
    quantity = inventory_treeview.set(some_item, 'quantity')
    quantity -= 1
    inventory_treeview.set(some_item, 'quantity', quantity)


# {'I001': 'Net'}
def inv_tree_dictionary_names(some_tup):
    temp = {}
    for thing in some_tup:
        temp[thing] = inventory_treeview.item(thing, 'text')
    return temp


# {'Net': 'I001'}
def inv_tree_dictionary_ids(some_tup):
    temp = {}
    for thing in some_tup:
        temp[inventory_treeview.item(thing, 'text')] = thing
    return temp


# adds new top level item to inventory treeview.
def new_tree_item(some_treeview, some_callback):
    new_item = inventory_treeview.insert('', 'end', text=some_treeview.item(some_callback[0])['text'])
    new_inventory_quantity(new_item)


# Loops through inventory treeview item names.
# Compares a given callbacks text value to each name.
# If call back equals name, add one to quantity value.
# Else, add new inventory treeview item.
def try_add_one_gui_quantity(some_treeview, some_callback):
    inv_items_tuple = inventory_treeview.get_children()

    names_dictionary = inv_tree_dictionary_names(inv_items_tuple)
    id_dictionary = inv_tree_dictionary_ids(inv_items_tuple)
    item_id = some_treeview.item(some_callback[0])
    item_name = item_id['text']

    for value in names_dictionary.values():
        if value == item_name:
            add_one_inventory_quantity(id_dictionary[item_name])
            return None  # Required to break out of function all together if match is found.
        elif id_dictionary[value] in inv_items_tuple:  # If name in inventory treeview, but not match, continue.
            continue

    new_tree_item(some_treeview, some_callback)


# Adds a new GUI item to inventory treeview if item name not already in.
# If already in, adds one to the quantity column value of a given item.
def buy_item_gui(some_callback):
    stores_dic = stores()

    if len(inventory_treeview.get_children()) != 0:

        if some_callback[0] in stores_dic['Ship']:
            try_add_one_gui_quantity(shipyard_treeview, some_callback)

        elif some_callback[0] in stores_dic['BS']:
            try_add_one_gui_quantity(blacksmith_treeview, some_callback)

        elif some_callback[0] in stores_dic['GS']:
            try_add_one_gui_quantity(general_store_treeview, some_callback)

        elif some_callback[0] in stores_dic['Stables']:
            try_add_one_gui_quantity(stables_treeview, some_callback)

    else:
        if some_callback[0] in stores_dic['Ship']:
            new_tree_item(shipyard_treeview, some_callback)
        elif some_callback[0] in stores_dic['BS']:
            new_tree_item(blacksmith_treeview, some_callback)
        elif some_callback[0] in stores_dic['GS']:
            new_tree_item(general_store_treeview, some_callback)
        elif some_callback[0] in stores_dic['Stables']:
            new_tree_item(stables_treeview, some_callback)


# Subtracts one from a give  gui item's quantity column value if given item has a quantity greater than one.
# Delete gui item if quantity column value less than one
def sell_item_gui(some_callback):
    quantity = inventory_treeview.set(some_callback, 'quantity')
    if quantity > 1:
        minus_one_inventory_quantity(some_callback)
    else:
        inventory_treeview.delete(some_callback)


# def print_button(some_callback):
#     tup = some_callback
#     dic = stores()
#     if some_callback[0] in dic['Ship']:
#         print(shipyard_treeview.item(some_callback[0])['text'])
#     elif some_callback[0] in dic['BS']:
#         print(blacksmith_treeview.item(some_callback[0])['text'])
#     elif some_callback[0] in dic['GS']:
#         print(general_store_treeview.item(some_callback[0])['text'])
#     elif some_callback[0] in dic['Stables']:
#         print(stables_treeview.item(some_callback[0])['text'])
#     else:
#         print(inventory_treeview.item(tup[0]['text']))

# def img_test():
#     img = PhotoImage(file='C:\\Users\\Terrance\\Desktop\\button_screens\\gold.png')
#     gold_pic = blacksmith_treeview.item(1, image=img)
#     gold_pic.image = img
#     print(blacksmith_treeview.item(1,)), ['image']
#     root.update()

# Sets current user character ID to key with all current items in inventory treeview as value.
def cache_inv():
    inv_cache[user_info['char'].id] = inventory_treeview.get_children()


# Deletes a list of inventory treeview items from 'cache' based on a given character ID.
def clear_cache(char_id):
    print(f'-----{char_id} cache deleted-----')
    del inv_cache[char_id]


# Detaches all treeview items present in a list of treeview items.
# Items list is retrieved from inventory cache dictionary.
# Notes, detach does not permanently delete the item. It merely removes it from view.
def detach_inv():
    inventory_treeview.detach(*inv_cache[user_info['char'].id])


# Searches a currency dictionary and returns key with value not equal to zero.
def inspecto_gadget(converted_value):
    for key, value in converted_value.items():
        if value != 0:
            return key


# Query all items from a given store. Use values returned to populate store treeviews.
def populate_tree(some_sql, some_tree, some_store):
    with conn:
        for number in range(database.count_rows(conn, sql.sql_count_rows(), 'items')[0]):
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

                if cur_type == 'gp':
                    some_tree.item(temp_dict['id'], tags='gold')
                elif cur_type == 'sp':
                    some_tree.item(temp_dict['id'], tags='silver')
                elif cur_type == 'cp':
                    some_tree.item(temp_dict['id'], tags='copper')

                some_tree.set(temp_dict['id'], 'price', converted_value[cur_type])

            # TODO: Consider better error handling. This is a silent pass. Not good.
            except TypeError:
                continue


# Populates inventory treeview from a list of DB item tuples.
def populate_inventory_treeview_db(db_char_items):
    for i in db_char_items:
        item_id = inventory_treeview.insert('', 'end', text=i[0])
        inventory_treeview.set(item_id, 'quantity', i[1])


# Reattach items to inventory treeview from inventory cache dictionary.
def populate_inventory_treeview_cache(tree_items_tup):
    for i in tree_items_tup:
        inventory_treeview.reattach(i, '', len(tree_items_tup))


# Checks if current character ID has inventory in cache dictionary.
# Reattaches if it does, else, populates via DB.
def populate_inventory():
    char_items = sql.execute_fetchall_sql(conn, sql.sql_all_character_items(), user_info['char'].id)

    if user_info['char'].id in inv_cache.keys():
        populate_inventory_treeview_cache(inv_cache[user_info['char'].id])
    elif len(char_items) > 0:
        populate_inventory_treeview_db(char_items)


# Populates the four treeview widgets that, makeup the dashboard page, with items.
def populate_all_trees():
    populate_tree(sql.sql_item_from_store(), blacksmith_treeview, 'Blacksmith')
    populate_tree(sql.sql_item_from_store(), shipyard_treeview, 'Shipyard')
    populate_tree(sql.sql_item_from_store(), general_store_treeview, 'General Store')
    populate_tree(sql.sql_item_from_store(), stables_treeview, 'Stables')


# clears (forgets) all widgets currently attached to root window.
def clear():
    for widget in root.grid_slaves():
        widget.grid_forget()


# Returns width and height of screen in pixels.
def screen_size():
    root.update()
    width = root.winfo_width()
    height = root.winfo_height()
    print(width, 'x', height)
    return {'w': width, 'h': height}


# Centers root window. Dashboard and install required a different formula to center properly.
# TODO: This is a quick and dirty solution
def center(dash=None):
    cur_size = screen_size()
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = (ws / 2) - (cur_size['w'] / 2)
    y = (hs / 2) - (cur_size['h'] / 2)
    if dash == [953, 630]:
        y -= 250
        root.geometry('%dx%d+%d+%d' % (dash[0], dash[1], x, y))
        root.update()
    elif dash == [820, 178]:
        root.geometry('%dx%d+%d+%d' % (dash[0], dash[1], x, y))
        root.update()
    else:
        root.geometry('%dx%d+%d+%d' % (cur_size['w'], cur_size['h'], x, y))
        root.update()


# Main window

root = Tk()

# Entry callback functions registration

is_alnum = root.register(entry_is_alnum_callback)
is_digit = root.register(entry_is_digit_callback)
is_alpha = root.register(entry_is_alpha_callback)
failed_is_digit = root.register(error_box.failed_validation_is_digit)
failed_is_alnum = root.register(error_box.failed_validation_is_alnum)
failed_is_alpha = root.register(error_box.failed_validation_is_alpha)

# Title labels

big_label = ttk.Style()
big_label.configure('big.TLabel', font=('Times', 25))
title_login_label = ttk.Label(text='Log-In', width='48', style='big.TLabel', anchor='center')
title_signup_label = ttk.Label(text='Sign-up', width='48', style='big.TLabel', anchor='center')
title_char_creation__label = ttk.Label(text='Character Creation', width='48', style='big.TLabel', anchor='center')
title_char_select_label = ttk.Label(text='Character Selection', width='48', style='big.TLabel', anchor='center')
title_install_label = ttk.Label(text='Installing....', width='48', style='big.TLabel', anchor='center')

# Labels

currency_display_label = ttk.Label(text='Currency Display')
characters_label = ttk.Label(text='Characters')
currency_label = ttk.Label(text='Currency')
name_label = ttk.Label(text='Name')
username_label = ttk.Label(text='Username')
password_label = ttk.Label(text='Password')

# Progressbars

install_bar = ttk.Progressbar(root, orient=HORIZONTAL, length=200, mode='determinate')

# Entries

login_page_password_entry = ttk.Entry(validate='key', validatecommand=(is_alnum, '%P'), invalidcommand=failed_is_alnum)
login_page_username_entry = ttk.Entry(validate='key', validatecommand=(is_alnum, '%P'), invalidcommand=failed_is_alnum)
signup_page_password_entry = ttk.Entry(validate='key', validatecommand=(is_alnum, '%P'), invalidcommand=failed_is_alnum)
signup_page_username_entry = ttk.Entry(validate='key', validatecommand=(is_alnum, '%P'), invalidcommand=failed_is_alnum)
name_entry = ttk.Entry(validate='key', validatecommand=(is_alpha, '%P'), invalidcommand=failed_is_alpha)
currency_entry = ttk.Entry(validate='key', validatecommand=(is_digit, '%P'), invalidcommand=failed_is_digit)

# Combos
chars_combo = ttk.Combobox(postcommand=populate_combo)

# Treeviews

shipyard_treeview = ttk.Treeview(root)  # ttk.Treeview(parent) Sets a treeview to a given parent window
general_store_treeview = ttk.Treeview(root)
blacksmith_treeview = ttk.Treeview(root)
stables_treeview = ttk.Treeview(root)
inventory_treeview = ttk.Treeview(root)
currency_treeview = ttk.Treeview(root)


# Pages
count = 0
max_count = 256


# Starts instillation process in a separate thread from main.
def start():
    def real_start():
        while True:
            con = database.create_connection(db)
            install_bar['value'] = 0
            install_bar['maximum'] = 256
            # update()
            if setup.wrong_schema(con):
                setup.create_schema(con)
                setup.stock_stores(con, install_bar, count, root)
            elif not setup.wrong_schema(con):
                log_in_page()
                break
            # if count >= max_count:
            #     log_in_page()

    threading.Thread(target=real_start).start()

# def update():
#     global count
#     global max_count
#     count += 500
    # install_bar['value'] = count
    # if count < max_count:
    #     root.after(100, update)
    # elif count >= max_count:
    #     log_in_page()


def install_page():

    clear()
    if setup.wrong_schema(conn):
        title_install_label.grid(column=0, row=0, sticky=W + E)
        install_bar.grid(column=0, row=1)
        install.grid(column=0, row=2)
    else:
        log_in_page()


def log_in_page():
    clear()

    title_login_label.grid(column=0, row=0, sticky=W + E)
    username_label.grid(column=0, row=1)
    login_page_username_entry.grid(column=0, row=2)
    password_label.grid(column=0, row=3)
    login_page_password_entry.grid(column=0, row=4)
    login_page_login_button.grid(column=0, row=5)
    login_page_signup_button.grid(column=0, row=6)

    clear_entry(login_page_username_entry)
    clear_entry(login_page_password_entry)
    login_page_username_entry.focus()

    center([820, 178])


def sign_up_page():
    clear()

    title_signup_label.grid(column=0, row=0, sticky=W + E)
    username_label.grid(column=0, row=1)
    signup_page_username_entry.grid(column=0, row=2)
    password_label.grid(column=0, row=3)
    signup_page_password_entry.grid(column=0, row=4)
    signup_page_signup_button.grid(column=0, row=5)
    signup_page_login_button.grid(column=0, row=6)

    clear_entry(signup_page_username_entry)
    clear_entry(signup_page_password_entry)
    signup_page_username_entry.focus()


def character_creation_page():
    clear()

    title_char_creation__label.grid(column=0, row=0, sticky=W + E)
    name_label.grid(column=0, row=1)
    name_entry.grid(column=0, row=2)
    currency_label.grid(column=0, row=3)
    currency_entry.grid(column=0, row=4)
    create_character_button.grid(column=0, row=5)
    logout_button.grid(column=0, row=6)


def character_selection_page():
    clear()

    title_char_select_label.grid(column=0, row=0, sticky=W + E)
    characters_label.grid(column=0, row=1)
    chars_combo.grid(column=0, row=2)
    select_button.grid(column=0, row=3)
    delete_button.grid(column=0, row=4)
    logout_button.grid(column=0, row=5, sticky=W + S)
    character_creation_button.grid(column=0, row=5, sticky=E + S)


# Currency icon images.
gold_img = PhotoImage(file='C:\\Users\\Terrance\\Desktop\\button_screens\\gold.png')
silver_img = PhotoImage(file='C:\\Users\\Terrance\\Desktop\\button_screens\\silver.png')
copper_img = PhotoImage(file='C:\\Users\\Terrance\\Desktop\\button_screens\\copper.png')


# TODO: This is not DRY.
def dashboard_page():

    currency_dict = user_info['char'].convert_currency()
    clear()

    def format_store(some_treeview):
        some_treeview.tag_configure('gold', image=gold_img)
        some_treeview.tag_configure('silver', image=silver_img)
        some_treeview.tag_configure('copper', image=copper_img)
        some_treeview.config(columns='price')
        some_treeview.column('price', width=85, anchor='center')
        some_treeview.column('#0', width=150)
        some_treeview.heading('price', text='Price')
        some_treeview.heading('#0', text='Item')

    # Gen Store formatting
    format_store(general_store_treeview)

    # Blacksmith formatting
    format_store(blacksmith_treeview)

    # Stables formatting
    format_store(stables_treeview)

    # Shipyard formatting
    format_store(shipyard_treeview)

    # Populate trees
    try:
        populate_all_trees()
    except TclError:
        pass

    try:
        currency_treeview.insert('', 'end', 'gold', text=currency_dict['gp'])

    except TclError:
        print('tcl error')
        update_currency_treeview(currency_dict)

    populate_inventory()

    # Binds
    shipyard_treeview.bind('<<TreeviewSelect>>', shipyard_callback)
    blacksmith_treeview.bind('<<TreeviewSelect>>', blacksmith_callback)
    stables_treeview.bind('<<TreeviewSelect>>', stables_callback)
    inventory_treeview.bind('<<TreeviewSelect>>', inventory_callback)
    general_store_treeview.bind('<<TreeviewSelect>>', general_store_callback)

    # General grid formatting
    general_store_treeview.grid(row=0, column=0)
    blacksmith_treeview.grid(row=0, column=1)
    stables_treeview.grid(row=0, column=2)
    shipyard_treeview.grid(row=0, column=3)
    inventory_treeview.grid(row=3, columnspan=4, sticky=W + E)
    currency_treeview.grid(row=2, columnspan=4)

    # Currency formatting

    currency_treeview.config(columns=['silver', 'copper'], height=1)
    currency_treeview.column('#0', width=55, anchor='center')
    currency_treeview.column('silver', width=55, anchor='center')
    currency_treeview.column('copper', width=55, anchor='center')
    currency_treeview.heading('#0', text='Gold')
    currency_treeview.heading('silver', text='Silver')
    currency_treeview.heading('copper', text='Copper')
    currency_treeview.set('gold', 'silver', currency_dict['sp'])
    currency_treeview.set('gold', 'copper', currency_dict['cp'])

    # Inventory formatting
    inventory_treeview.config(columns='quantity')
    inventory_treeview.column('quantity', width=55, anchor='center')
    inventory_treeview.heading('quantity', text='Quantity')
    inventory_treeview.column('#0', width=550)
    inventory_treeview.heading('#0', text='Item')

    # Buttons
    buy.grid(row=1, columnspan=4, sticky=W + E)
    sell.grid(row=4, columnspan=4, sticky=N + W + E)
    logout_button.grid(row=5, column=0, pady=50, sticky=S + W)
    dashboard_page_character_select_button.grid(row=5, column=3, pady=50, sticky=S + E)
    cur_size = screen_size()
    if cur_size['h'] != 630:
        center([953, 630])
    # center()


# Button commands (backend integration)

# Creates account row based on entry boxes and adds to DB. Pushes to login page.
def signup_page_signup_command():
    if account.user_creates_account(conn, signup_page_username_entry.get(), signup_page_password_entry.get()):
        log_in_page()


# Authenticates information passed to entry boxes against DB. Pushes to character creation page
def login_page_login_command():
    # account.log_in(conn, login_page_username_entry.get(), login_page_password_entry.get())
    user_info['acc'] = account.log_in(conn, login_page_username_entry.get(), login_page_password_entry.get())
    if user_info['acc'] is not None:
        if account.account_has_characters(conn, user_info['acc'].id):
            character_selection_page()
        else:
            character_creation_page()


# Creates character row based on entry boxes and adds to DB. Pushes to character selection page.
def create_character_command():
    name = name_entry.get()
    currency = currency_entry.get()
    if character.character_creation(conn, user_info['acc'].id, name, currency):
        character_selection_page()


# Clears dictionary holding account information objects. Pushes to login page.
def logout_command():
    if not user_info['char']:
        log_out()
        log_in_page()
        center()
    else:
        cache_inv()
        detach_inv()
        log_out()
        log_in_page()
        center()


# Deletes a character from the front(gui) and back(DB) end.
def delete_command():
    temp = {}
    char_selected = chars_combo.get()
    acc_id = user_info['acc'].id
    characters_tuple_list = sql.execute_fetchall_sql(conn, sql.sql_all_characters(), acc_id)
    for tup in characters_tuple_list:
        temp[tup[1]] = tup[0]
    char_id = temp[char_selected]
    database.delete_character(conn, char_id)
    clear_cache(char_id)
    clear_entry(chars_combo)
    print('-----character deleted-----')
    root.update()


# Sets current character to a given character object, Character object is based on combobox value.
def select_command():
    user_info['char'] = character.load_character_object(conn, chars_combo.get())
    print(user_info)
    dashboard_page()


# Buys item on front (gui) and back (DB) end. Updates currency based on item value.
def buy_command():

    item_name = None
    affordable = None
    dic = stores()

    print(recent_selection['selected'])
    tup = recent_selection['selected']

    if tup[0] in dic['Ship']:
        item_name = shipyard_treeview.item(tup[0])['text']
    elif tup[0] in dic['BS']:
        item_name = blacksmith_treeview.item(tup[0])['text']
    elif tup[0] in dic['GS']:
        item_name = general_store_treeview.item(tup[0])['text']
    elif tup[0] in dic['Stables']:
        item_name = stables_treeview.item(tup[0])['text']
    if item_name is not None:
        affordable = user_info['char'].buy_sell(item_name, 'buy', conn)

    currency_dict = user_info['char'].convert_currency()
    currency_treeview.item('gold', text=currency_dict['gp'])
    currency_treeview.set('gold', 'silver', currency_dict['sp'])
    currency_treeview.set('gold', 'copper', currency_dict['cp'])

    root.update()

    if affordable:
        buy_item_gui(recent_selection['selected'])
        if not database.item_in_inventory_add(conn, user_info['inv'], item_name):
            user_info['char'].add_item(conn, item_name, user_info['acc'].id, user_info['inv'])

    check_value_and_toggle()


# Sells item and updates currency on front-end.
def sell_command():
    # print(recent_selection['selected'])
    tup = inv_selected['selected']
    item = inventory_treeview.item(tup, 'text')

    user_info['char'].buy_sell(item, 'sell', conn)

    currency_dict = user_info['char'].convert_currency()
    currency_treeview.item('gold', text=currency_dict['gp'])
    currency_treeview.set('gold', 'silver', currency_dict['sp'])
    currency_treeview.set('gold', 'copper', currency_dict['cp'])

    sell_item_gui(inv_selected['selected'])

    root.update()

    if not database.item_in_inventory_minus(conn, user_info['inv'], item):
        database.delete_item(conn, item, user_info['inv'])


def char_select_command():
    cache_inv()
    detach_inv()
    character_selection_page()


# Buttons

login_page_login_button = Button(text='Log-in', bg='gray', command=login_page_login_command)
login_page_signup_button = Button(text='Sign-up', bg='gray', command=sign_up_page)
signup_page_login_button = Button(text='Log-in', bg='gray', command=log_in_page)
signup_page_signup_button = Button(text='Sign-up', bg='gray', command=signup_page_signup_command)
create_character_button = Button(text='Create', bg='gray', command=create_character_command)
logout_button = Button(text='Log-out', bg='gray', command=logout_command)
character_creation_button = Button(text='Character creation', bg='gray', command=character_creation_page)
select_button = Button(text='Select', bg='gray', command=select_command)
dashboard_page_character_select_button = Button(text='Character Selection', bg='gray', command=char_select_command)
delete_button = Button(text='Delete', bg='gray', command=delete_command)
sell = Button(text='Sell', bg='gray', activebackground='green', command=sell_command)
dummy = Button(root, text='Test', bg='gray')
buy = Button(text='Buy', bg='gray', command=buy_command)
install = Button(text='install', bg='gray', command=start)
# buy = ttk.Button(text='Buy', command=lambda: buy_item_gui(selected['selected']))
# buy = Button(text='Buy', bg='gray', command=img_test)
# sell = Button(text='Sell', bg='gray', activebackground='green', command=pog_cmd)
install_page()
center()
root.mainloop()

