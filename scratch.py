from tkinter import *
from tkinter import ttk
from stores import stores
import sql
import account
import setup
import database
import character
# TODO: Hasn't been tested, refactored, or commented.

# TODO: Comment all of the things. Every block if it makes sense to do so.

# TODO: Update GUI.py once clean

db = 'C:\\sqlite\\db\\test.db'
mem = ':memory:'

user_info = {'acc': None, 'char': None, 'inv': 1}

# selected = {'selected': 'none'}
gen_selected = {'selected': 'none'}
bs_selected = {'selected': 'none'}
stable_selected = {'selected': 'none'}
ship_selected = {'selected': 'none'}
inv_selected = {'selected': 'none'}
recent_selection = {'selected': 'None'}

# Setup in mem DB for testing purposes.
conn = database.create_connection(db)
setup.create_schema(conn)
if not setup.wrong_schema(conn):
    setup.stock_stores(conn)


# General Functions

# Generic function that is passed a tuple with a single value.
# Value represents both the item_id (database) and the item id (tkinter gui).
def new_selection(some_selection):
    recent_selection['selected'] = some_selection


# Clears dictionaries storing account information objects.
def log_out():
    print('-----Logged Out-----')
    user_info['acc'] = None
    user_info['char'] = None
    user_info['inv'] = None


# Adds character to DB based on current character information.
def character_creation(name, currency):
        character_info_dict = {'acc_id': user_info['acc'].id, 'name': name, 'currency': currency}
        database.add_character_row(conn, sql.sql_add_character_row(), character_info_dict)


# Query characters from DB based on current account id.
# Slices name from tuples returned and appends to empty list. Sets combo values to list.
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

def generic_callback(event, some_dict, some_treeview):
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
    # print(shipyard_treeview.item(tup[0])['text'])    # Gets name of item selected
    # print(shipyard_treeview.selection())
    generic_callback(event, ship_selected, shipyard_treeview)


def general_store_callback(event):
    generic_callback(event, gen_selected, general_store_treeview)


def blacksmith_callback(event):
    generic_callback(event, bs_selected, blacksmith_treeview)


def stables_callback(event):
    generic_callback(event, stable_selected, stables_treeview)


# The inventory callback function also attempts to deselect all previously selections in store widgets.
def inventory_callback(event):
    try:
        blacksmith_treeview.selection_toggle(bs_selected['selected'])
        general_store_treeview.selection_toggle(gen_selected['selected'])
        stables_treeview.selection_toggle(stable_selected['selected'])
        shipyard_treeview.selection_toggle(ship_selected['selected'])
    except TclError:
        pass

    generic_callback(event, inv_selected, inventory_treeview)
    print(inventory_treeview.selection())
    print(inventory_treeview.item(inventory_treeview.selection(), 'text'))
    print(recent_selection['selected'])


# Sets quantity column of a given (gui)item to 1.
def new_inventory_quantity(some_item):
    inventory_treeview.set(some_item, 'quantity', 1)


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
            return None     # Required to break out of function all together if match is found.
        elif id_dictionary[value] in inv_items_tuple:   # If name in inventory treeview, but not match, continue.
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
                some_tree.insert('', 'end', temp_dict['id'], text=temp_dict['name'])

            # TODO: Consider better error handling. This is a silent pass. Not good.
            except TypeError:
                continue


# Populates the five treeview widgets that, makeup the dashboard page, with items.
def populate_all_trees():
    populate_tree(sql.sql_item_from_store(), shipyard_treeview, 'Shipyard')
    populate_tree(sql.sql_item_from_store(), general_store_treeview, 'General Store')
    populate_tree(sql.sql_item_from_store(), blacksmith_treeview, 'Blacksmith')
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


# Centers root window. Dashboard required a different formula to center properly.
# TODO: This is a quick and dirty solution
def center(dash=None):
    cur_size = screen_size()
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = (ws / 2) - (cur_size['w'] / 2)
    y = (hs / 2) - (cur_size['h'] / 2)
    if dash is not None:
        y -= 250
        root.geometry('%dx%d+%d+%d' % (dash[0], dash[1], x, y))
        root.update()
    else:
        root.geometry('%dx%d+%d+%d' % (cur_size['w'], cur_size['h'], x, y))
        root.update()


# Main window

root = Tk()

# Title labels

big_label = ttk.Style()
big_label.configure('big.TLabel', font=('Times', 25))
title_login_label = ttk.Label(text='Log-In', width='48', style='big.TLabel', anchor='center')
title_signup_label = ttk.Label(text='Sign-up', width='48', style='big.TLabel', anchor='center')
title_char_creation__label = ttk.Label(text='Character Creation', width='48', style='big.TLabel', anchor='center')
title_char_select_label = ttk.Label(text='Character Selection', width='48', style='big.TLabel', anchor='center')


# Labels

currency_display_label = ttk.Label(text='Currency Display')
characters_label = ttk.Label(text='Characters')
currency_label = ttk.Label(text='Currency')
name_label = ttk.Label(text='Name')
username_label = ttk.Label(text='Username')
password_label = ttk.Label(text='Password')

# Entrys

login_page_password_entry = ttk.Entry()
login_page_username_entry = ttk.Entry()
signup_page_password_entry = ttk.Entry()
signup_page_username_entry = ttk.Entry()
name_entry = ttk.Entry()
currency_entry = ttk.Entry()


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

def log_in_page():
    clear()

    title_login_label.grid(column=0, row=0, sticky=W+E)
    username_label.grid(column=0, row=1)
    login_page_username_entry.grid(column=0, row=2)
    password_label.grid(column=0, row=3)
    login_page_password_entry.grid(column=0, row=4)
    login_page_login_button.grid(column=0, row=5)
    login_page_signup_button.grid(column=0, row=6)

    clear_entry(login_page_username_entry)
    clear_entry(login_page_password_entry)
    login_page_username_entry.focus()


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

    title_char_creation__label.grid(column=0, row=0, sticky=W+E)
    name_label.grid(column=0, row=1)
    name_entry.grid(column=0, row=2)
    currency_label.grid(column=0, row=3)
    currency_entry.grid(column=0, row=4)
    create_character_button.grid(column=0, row=5)
    logout_button.grid(column=0, row=6)


def character_selection_page():
    clear()

    title_char_select_label.grid(column=0, row=0, sticky=W+E)
    characters_label.grid(column=0, row=1)
    chars_combo.grid(column=0, row=2)
    select_button.grid(column=0, row=3)
    delete_button.grid(column=0, row=4)
    logout_button.grid(column=0, row=5, sticky=W+S)
    character_creation_button.grid(column=0, row=5, sticky=E+S)


def dashboard_page():
    currency_dict = user_info['char'].convert_currency()
    clear()

    # Populate trees
    populate_all_trees()
    currency_treeview.insert('', 'end', 'gold', text=currency_dict['gp'])

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
    inventory_treeview.grid(row=3, columnspan=4, sticky=W+E)
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

    # Gen Store formatting
    general_store_treeview.config(columns='quantity')
    general_store_treeview.column('quantity', width=55, anchor='center')
    general_store_treeview.column('#0', width=150)
    general_store_treeview.heading('quantity', text='Quantity')
    general_store_treeview.heading('#0', text='Item')

    # Blacksmith formatting
    blacksmith_treeview.config(columns='quantity')
    blacksmith_treeview.column('quantity', width=55, anchor='center')
    blacksmith_treeview.column('#0', width=150)
    blacksmith_treeview.heading('quantity', text='Quantity')
    blacksmith_treeview.heading('#0', text='Item')

    # Stables formatting
    stables_treeview.config(columns='quantity')
    stables_treeview.column('quantity', width=55, anchor='center')
    stables_treeview.column('#0', width=150)
    stables_treeview.heading('quantity', text='Quantity')
    stables_treeview.heading('#0', text='Item')

    # Shipyard formatting
    shipyard_treeview.config(columns='quantity')
    shipyard_treeview.column('quantity', width=55, anchor='center')
    shipyard_treeview.heading('quantity', text='Quantity')
    shipyard_treeview.column('#0', width=150)
    shipyard_treeview.heading('#0', text='Item')

    # Inventory formatting
    inventory_treeview.config(columns='quantity')
    inventory_treeview.column('quantity', width=55, anchor='center')
    inventory_treeview.heading('quantity', text='Quantity')
    inventory_treeview.column('#0', width=550)
    inventory_treeview.heading('#0', text='Item')

    # Buttons
    sell.grid(row=4, columnspan=4, sticky=N+W+E)
    dummy.grid(row=5, columnspan=4, sticky=W+E)
    buy.grid(row=1, columnspan=4, sticky=W+E)
    screen_size()
    center([832, 630])


# Button commands (backend integration)

# Creates account row based on entry boxes and adds to DB. Pushes to login page.
def signup_page_signup_command():
    account.user_creates_account(conn, signup_page_username_entry.get(), signup_page_password_entry.get())
    log_in_page()


# TODO: Needs to have logic to push to char create or char select depending.
# Authenticates information passed to entry boxes against DB. Pushes to character creation page
def login_page_login_command():
    account.log_in(conn, login_page_username_entry.get(), login_page_password_entry.get())
    user_info['acc'] = account.load_account_object(conn, login_page_username_entry.get())
    character_creation_page()


# Creates character row based on entry boxes and adds to DB. Pushes to character selection page.
def create_character_command():
    name = name_entry.get()
    currency = currency_entry.get()
    character_creation(name, currency)
    character_selection_page()


# Clears dictionary holding account information objects. Pushes to login page.
def logout_command():
    log_out()
    log_in_page()


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
    clear_entry(chars_combo)
    print('-----character deleted-----')
    root.update()


# Sets current character to a given character object, Character object is based on combobox value.
def select_command():
    user_info['char'] = character.load_character_object(conn, chars_combo.get())
    print(user_info)
    dashboard_page()


# TODO: Integrate currency back-end.
# Buys item on front (gui) and back (DB) end. Updates currency based on item value.
def buy_command():
    item = None
    print(recent_selection['selected'])

    buy_item_gui(recent_selection['selected'])

    tup = recent_selection['selected']
    dic = stores()

    if tup[0] in dic['Ship']:
        item = shipyard_treeview.item(tup[0])['text']
    elif tup[0] in dic['BS']:
        item = blacksmith_treeview.item(tup[0])['text']
    elif tup[0] in dic['GS']:
        item = general_store_treeview.item(tup[0])['text']
    elif tup[0] in dic['Stables']:
        item = stables_treeview.item(tup[0])['text']
    if item is not None:
        user_info['char'].buy_sell(item, 'buy')

    currency_dict = user_info['char'].convert_currency()
    currency_treeview.item('gold', text=currency_dict['gp'])
    currency_treeview.set('gold', 'silver', currency_dict['sp'])
    currency_treeview.set('gold', 'copper', currency_dict['cp'])
    root.update()

    if not database.item_in_inventory_add(conn, user_info['inv'], item):
        user_info['char'].add_item(conn, item, user_info['acc'].id, user_info['inv'])


# TODO: Integrate back-end.
# Sells item and updates currency on front-end.
def sell_command():
    # print(recent_selection['selected'])
    tup = inv_selected['selected']
    item = inventory_treeview.item(tup, 'text')
    user_info['char'].buy_sell(item, 'sell')
    currency_dict = user_info['char'].convert_currency()
    currency_treeview.item('gold', text=currency_dict['gp'])
    currency_treeview.set('gold', 'silver', currency_dict['sp'])
    currency_treeview.set('gold', 'copper', currency_dict['cp'])
    sell_item_gui(inv_selected['selected'])
    root.update()


# Buttons

login_page_login_button = ttk.Button(text='Log-in', command=login_page_login_command)
login_page_signup_button = ttk.Button(text='Sign-up', command=sign_up_page)
signup_page_login_button = ttk.Button(text='Log-in', command=log_in_page)
signup_page_signup_button = ttk.Button(text='Sign-up', command=signup_page_signup_command)
create_character_button = ttk.Button(text='Create', command=create_character_command)
logout_button = ttk.Button(text='Log-out', command=logout_command)
character_creation_button = ttk.Button(text='Character creation', command=character_creation_page)
select_button = ttk.Button(text='Select', command=select_command)
delete_button = ttk.Button(text='Delete', command=delete_command)
sell = ttk.Button(text='Sell', command=sell_command)
dummy = ttk.Button(root, text='Test')
# buy = ttk.Button(text='Buy', command=lambda: buy_item_gui(selected['selected']))
buy = ttk.Button(text='Buy', command=buy_command)
log_in_page()
center()
root.mainloop()
