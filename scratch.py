from tkinter import *
from tkinter import ttk
from stores import stores
import sql
import account
import setup
import database
import player
# TODO: Update GUI.py once clean
# TODO: Comment all of the things. Every block if it makes sense to do so.

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

# Setup in mem DB for testing purposes
conn = database.create_connection(db)
setup.create_schema(conn)
if not setup.wrong_schema(conn):
    setup.stock_stores(conn)


# Methods
def new_selection(some_selection):
    recent_selection['selected'] = some_selection


def log_out():
    print('-----Logged Out-----')
    user_info['acc'] = None
    user_info['char'] = None
    user_info['inv'] = None


# Working model for character creation
def character_creation(name, currency):
        # character_info = (cur_account.id, name, 5000)
        character_info = {'acc_id': user_info['acc'].id, 'name': name, 'currency': currency}
        database.add_character_row(conn, sql.sql_add_character_row(), character_info)


def populate_combo():
    temp = []
    acc_id = user_info['acc'].id
    characters = sql.execute_fetchall_sql(conn, sql.sql_all_characters(), acc_id)
    for c in characters:
        temp.append(c[1])
    chars_combo['values'] = temp


# def populate_combo1():
#     chars_combo['values'] = ['1', '2', '3']


def clear_entry(some_entry):
    some_entry.delete(0, 'end')


def populate_all_trees():
    populate_tree(shipyard_treeview, 'Shipyard')
    populate_tree(general_store_treeview, 'General Store')
    populate_tree(blacksmith_treeview, 'Blacksmith')
    populate_tree(stables_treeview, 'Stables')


def shipyard_callback(event):
    # print(shipyard_treeview.selection())  # Gets tuple with id as first value
    # # print(treeview.set('I001', 'quantity'))
    # print(shipyard_treeview.item('I001'))
    # tup = shipyard_treeview.selection()
    # # Gets value of quantity for item selected.
    # # Quantity can be swapped for another column
    # print(shipyard_treeview.set(tup[0], 'quantity'))
    # print(shipyard_treeview.item(tup[0])['text'])    # Gets name of item selected
    ship_selected['selected'] = shipyard_treeview.selection()
    new_selection(ship_selected['selected'])


def general_store_callback(event):
    gen_selected['selected'] = general_store_treeview.selection()
    new_selection(gen_selected['selected'])


def blacksmith_callback(event):
    bs_selected['selected'] = blacksmith_treeview.selection()
    new_selection(bs_selected['selected'])


def stables_callback(event):
    stable_selected['selected'] = stables_treeview.selection()
    new_selection(stable_selected['selected'])


def inventory_callback(event):
    try:
        blacksmith_treeview.selection_toggle(bs_selected['selected'])
        general_store_treeview.selection_toggle(gen_selected['selected'])
        stables_treeview.selection_toggle(stable_selected['selected'])
        shipyard_treeview.selection_toggle(ship_selected['selected'])
    except TclError:
        pass

    inv_selected['selected'] = inventory_treeview.selection()
    print(inventory_treeview.selection())
    print(inventory_treeview.item(inventory_treeview.selection(), 'text'))
    new_selection(inv_selected['selected'])
    print(recent_selection['selected'])


def new_inventory_quantity(some_item):
    inventory_treeview.set(some_item, 'quantity', 1)


def add_one_inventory_quantity(some_item):
    quantity = inventory_treeview.set(some_item, 'quantity')
    # quantity = int(quantity)
    quantity += 1
    inventory_treeview.set(some_item, 'quantity', quantity)


def minus_one_inventory_quantity(some_item):
    quantity = inventory_treeview.set(some_item, 'quantity')
    # quantity = int(quantity)
    quantity -= 1
    inventory_treeview.set(some_item, 'quantity', quantity)


def inv_tree_dictionary(some_tup):
    temp = {}
    for i in some_tup:
        temp[i] = inventory_treeview.item(i, 'text')
    return temp


def inv_tree_dictionary2(some_tup):
    temp = {}
    for i in some_tup:
        temp[inventory_treeview.item(i, 'text')] = i
    return temp


def buy_item_gui(some_callback):
    dic = stores()
    inv_items = inventory_treeview.get_children()
    if len(inv_items) != 0:
        inv_tree_dict1 = inv_tree_dictionary(inv_items)
        inv_tree_dict2 = inv_tree_dictionary2(inv_items)
        if some_callback[0] in dic['Ship']:
            item_id = shipyard_treeview.item(some_callback[0])
            item_name = item_id['text']
            for v in inv_tree_dict1.values():
                if v == item_name:
                    add_one_inventory_quantity(inv_tree_dict2[item_name])
                    return None
                elif inv_tree_dict2[v] in inv_items:
                    continue

            new_item = inventory_treeview.insert('', 'end', text=shipyard_treeview.item(some_callback[0])['text'])
            new_inventory_quantity(new_item)
        elif some_callback[0] in dic['BS']:
            item_id = blacksmith_treeview.item(some_callback[0])
            item_name = item_id['text']
            for v in inv_tree_dict1.values():
                if v == item_name:
                    add_one_inventory_quantity(inv_tree_dict2[item_name])
                    return None
                elif inv_tree_dict2[v] in inv_items:
                    continue

            new_item = inventory_treeview.insert('', 'end', text=blacksmith_treeview.item(some_callback[0])['text'])
            new_inventory_quantity(new_item)
        elif some_callback[0] in dic['GS']:
            item_id = general_store_treeview.item(some_callback[0])
            item_name = item_id['text']
            for v in inv_tree_dict1.values():
                if v == item_name:
                    add_one_inventory_quantity(inv_tree_dict2[item_name])
                    return None
                elif inv_tree_dict2[v] in inv_items:
                    continue

            new_item = inventory_treeview.insert('', 'end', text=general_store_treeview.item(some_callback[0])['text'])
            new_inventory_quantity(new_item)
        elif some_callback[0] in dic['Stables']:
            item_id = stables_treeview.item(some_callback[0])
            item_name = item_id['text']
            for v in inv_tree_dict1.values():
                if v == item_name:
                    add_one_inventory_quantity(inv_tree_dict2[item_name])
                    return None
                elif inv_tree_dict2[v] in inv_items:
                    continue

            new_item = inventory_treeview.insert('', 'end', text=stables_treeview.item(some_callback[0])['text'])
            new_inventory_quantity(new_item)
    else:
        if some_callback[0] in dic['Ship']:
            new_item = inventory_treeview.insert('', 'end', text=shipyard_treeview.item(some_callback[0])['text'])
            new_inventory_quantity(new_item)
        elif some_callback[0] in dic['BS']:
            new_item = inventory_treeview.insert('', 'end', text=blacksmith_treeview.item(some_callback[0])['text'])
            new_inventory_quantity(new_item)
        elif some_callback[0] in dic['GS']:
            new_item = inventory_treeview.insert('', 'end', text=general_store_treeview.item(some_callback[0])['text'])
            new_inventory_quantity(new_item)
        elif some_callback[0] in dic['Stables']:
            new_item = inventory_treeview.insert('', 'end', text=stables_treeview.item(some_callback[0])['text'])
            new_inventory_quantity(new_item)


def sell_item_gui(some_callback):
    quantity = inventory_treeview.set(some_callback, 'quantity')
    if quantity > 1:
        minus_one_inventory_quantity(some_callback)
    else:
        inventory_treeview.delete(some_callback)


def print_button(some_callback):
    tup = some_callback
    dic = stores()
    if some_callback[0] in dic['Ship']:
        print(shipyard_treeview.item(some_callback[0])['text'])
    elif some_callback[0] in dic['BS']:
        print(blacksmith_treeview.item(some_callback[0])['text'])
    elif some_callback[0] in dic['GS']:
        print(general_store_treeview.item(some_callback[0])['text'])
    elif some_callback[0] in dic['Stables']:
        print(stables_treeview.item(some_callback[0])['text'])
    else:
        print(inventory_treeview.item(tup[0]['text']))


# TODO: Needs comments
def populate_tree(some_tree, some_store):
    # conn = create_connection(db)
    with conn:
        for i in range(database.count_rows(conn, sql.sql_count_rows(), 'items')[0]):
            d = {}
            i += 1
            k = """SELECT id, item FROM items WHERE id = ? AND store = ?;"""
            cur = conn.cursor()
            cur.execute(k, [str(i), some_store])
            o = cur.fetchone()
            try:
                d['id'] = o[0]
                d['name'] = o[1]
                some_tree.insert('', 'end', d['id'], text=d['name'])
            except TypeError:
                continue


def clear():
    for i in root.grid_slaves():
        i.grid_forget()


def screen_size():
    root.update()
    width = root.winfo_width()
    height = root.winfo_height()
    print(width, 'x', height)
    return {'w': width, 'h': height}


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

# Title label

big_label = ttk.Style()
big_label.configure('big.TLabel', font=('Times', 25))
title_login_label = ttk.Label(text='Log-In', width='48', style='big.TLabel', anchor='center')
title_signup_label = ttk.Label(text='Sign-up', width='48', style='big.TLabel', anchor='center')
title_char_creation__label = ttk.Label(text='Character Creation', width='48', style='big.TLabel', anchor='center')
title_char_select_label = ttk.Label(text='Character Selection', width='48', style='big.TLabel', anchor='center')


# Label

currency_display_label = ttk.Label(text='Currency Display')
characters_label = ttk.Label(text='Characters')
currency_label = ttk.Label(text='Currency')
name_label = ttk.Label(text='Name')
username_label = ttk.Label(text='Username')
password_label = ttk.Label(text='Password')

# Entry

login_page_password_entry = ttk.Entry()
login_page_username_entry = ttk.Entry()
signup_page_password_entry = ttk.Entry()
signup_page_username_entry = ttk.Entry()
name_entry = ttk.Entry()
currency_entry = ttk.Entry()


# Combo
chars_combo = ttk.Combobox(postcommand=populate_combo)
# chars_combo = ttk.Combobox(values=['1', '2', '3'])


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
    character_selection_button.grid(column=0, row=5, sticky=E+S)


def dashboard():
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

    # Labels
    # currency_display_label.grid(row=2, columnspan=4, sticky=N)


# Button functions (backend integration)

def signup_page_signup_command():
    account.user_creates_account(conn, signup_page_username_entry.get(), signup_page_password_entry.get())
    log_in_page()


def login_page_login_command():
    account.log_in(conn, login_page_username_entry.get(), login_page_password_entry.get())
    user_info['acc'] = account.load_account_object(conn, login_page_username_entry.get())
    character_creation_page()


def create_character_command():
    name = name_entry.get()
    currency = currency_entry.get()
    character_creation(name, currency)
    character_selection_page()


def logout_command():
    log_out()
    log_in_page()


def delete_command():
    temp = {}
    char_selected = chars_combo.get()
    acc_id = user_info['acc'].id
    characters = sql.execute_fetchall_sql(conn, sql.sql_all_characters(), acc_id)
    for c in characters:
        temp[c[1]] = c[0]
    char_id = temp[char_selected]
    database.delete_character(conn, char_id)
    clear_entry(chars_combo)
    print('-----character deleted-----')
    root.update()


def select_command():
    user_info['char'] = player.load_player_object(conn, chars_combo.get())
    print(user_info)
    dashboard()


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
    # item_name = inventory_treeview.item(tup, 'text')
    # user_dict = {'acc_id': user_info['acc'],
    #              'char_id': user_info['char'],
    #              'inv_id': user_info['inv'],
    #              'item': item_name,
    #              'api': None,
    #              'quant': None}
    if not database.item_in_inventory_add(conn, user_info['inv'], item):
        user_info['char'].add_item(conn, item, user_info['acc'].id, user_info['inv'])


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


# Button

login_page_login_button = ttk.Button(text='Log-in', command=login_page_login_command)
login_page_signup_button = ttk.Button(text='Sign-up', command=sign_up_page)
signup_page_login_button = ttk.Button(text='Log-in', command=log_in_page)
signup_page_signup_button = ttk.Button(text='Sign-up', command=signup_page_signup_command)
create_character_button = ttk.Button(text='Create', command=create_character_command)
logout_button = ttk.Button(text='Log-out', command=logout_command)
character_selection_button = ttk.Button(text='Character selection', command=character_selection_page)
select_button = ttk.Button(text='Select', command=select_command)
delete_button = ttk.Button(text='Delete', command=delete_command)
sell = ttk.Button(text='Sell', command=sell_command)
dummy = ttk.Button(root, text='Test')
# buy = ttk.Button(text='Buy', command=lambda: buy_item_gui(selected['selected']))
buy = ttk.Button(text='Buy', command=buy_command)
log_in_page()
center()
root.mainloop()
