from tkinter import *
from tkinter import ttk
from database import create_connection, count_rows
from stores import stores
import sql

db = 'C:\\sqlite\\db\\test.db'
mem = ':memory:'
selected = {'selected': 'none'}


# Methods
def populate_all_trees():
    populate_tree(shipyard_treeview, 'Shipyard')
    populate_tree(general_store_treeview, 'General Store')
    populate_tree(blacksmith_treeview, 'Blacksmith')
    populate_tree(stables_treeview, 'Stables')


def shipyard_callback(event):
    # print(shipyard_treeview.selection())  # Gets tuple with id as first value
    # # print(treeview.set('I001', 'quantity'))
    # # print(treeview.item('I001'))
    # tup = shipyard_treeview.selection()
    # # Gets value of quantity for item selected.
    # # Quantity can be swapped for another column
    # print(shipyard_treeview.set(tup[0], 'quantity'))
    # print(shipyard_treeview.item(tup[0])['text'])    # Gets name of item selected
    selected['selected'] = shipyard_treeview.selection()


def general_store_callback(event):
    selected['selected'] = general_store_treeview.selection()


def blacksmith_callback(event):
    selected['selected'] = blacksmith_treeview.selection()


def stables_callback(event):
    selected['selected'] = stables_treeview.selection()


def inventory_callback(event):
    selected['selected'] = inventory_treeview.selection()
    print(inventory_treeview.selection())


def buy_item_gui(some_callback):
    dic = stores()
    if some_callback[0] in dic['Ship']:
        inventory_treeview.insert('', 'end', text=shipyard_treeview.item(some_callback[0])['text'])
    elif some_callback[0] in dic['BS']:
        inventory_treeview.insert('', 'end', text=blacksmith_treeview.item(some_callback[0])['text'])
    elif some_callback[0] in dic['GS']:
        inventory_treeview.insert('', 'end', text=general_store_treeview.item(some_callback[0])['text'])
    elif some_callback[0] in dic['Stables']:
        inventory_treeview.insert('', 'end', text=stables_treeview.item(some_callback[0])['text'])


def sell_item_gui(some_callback):
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


def populate_tree(some_tree, some_store):
    conn = create_connection(db)
    with conn:
        for i in range(count_rows(conn, sql.sql_count_rows(), 'items')[0]):
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

characters_label = ttk.Label(text='Characters')
currency_label = ttk.Label(text='Currency')
name_label = ttk.Label(text='Name')
username_label = ttk.Label(text='Username')
password_label = ttk.Label(text='Password')

# Entry

password_entry = ttk.Entry()
username_entry = ttk.Entry()
name_entry = ttk.Entry()
currency_entry = ttk.Entry()

# Combo

chars_combo = ttk.Combobox(values=['1', '2', '3'])

# Treeviews

shipyard_treeview = ttk.Treeview(root)  # ttk.Treeview(parent) Sets a treeview to a given parent window
general_store_treeview = ttk.Treeview(root)
blacksmith_treeview = ttk.Treeview(root)
stables_treeview = ttk.Treeview(root)
inventory_treeview = ttk.Treeview(root)


# Pages


def log_in_page():
    clear()
    title_login_label.grid(column=0, row=0, sticky=W + E)
    username_label.grid(column=0, row=1)
    username_entry.grid(column=0, row=2)
    password_label.grid(column=0, row=3)
    password_entry.grid(column=0, row=4)
    login_page_login_button.grid(column=0, row=5)
    login_page_signup_button.grid(column=0, row=6)


def sign_up_page():
    clear()
    title_signup_label.grid(column=0, row=0, sticky=W + E)
    username_label.grid(column=0, row=1)
    username_entry.grid(column=0, row=2)
    password_label.grid(column=0, row=3)
    password_entry.grid(column=0, row=4)
    signup_page_signup_button.grid(column=0, row=5)
    signup_page_login_button.grid(column=0, row=6)


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


def dashboard():
    clear()

    # Populate trees
    populate_all_trees()

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
    inventory_treeview.grid(row=2, columnspan=4, sticky=W + E, pady=50)

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
    sell.grid(row=3, columnspan=4, sticky=W + E)
    dummy.grid(row=4, columnspan=4, sticky=W + E)
    buy.grid(row=1, columnspan=4, sticky=W + E)
    screen_size()
    center([832, 630])


# Button

login_page_login_button = ttk.Button(text='Log-in', command=character_creation_page)
login_page_signup_button = ttk.Button(text='Sign-up', command=sign_up_page)
signup_page_login_button = ttk.Button(text='Log-in', command=log_in_page)
signup_page_signup_button = ttk.Button(text='Sign-up', command=log_in_page)
create_character_button = ttk.Button(text='Create', command=character_selection_page)
logout_button = ttk.Button(text='Log-out', command=log_in_page)
select_button = ttk.Button(text='Select', command=dashboard)
delete_button = ttk.Button(text='Delete')
sell = ttk.Button(text='Sell', command=lambda: sell_item_gui(selected['selected']))
dummy = ttk.Button(root, text='Test')
buy = ttk.Button(text='Buy', command=lambda: buy_item_gui(selected['selected']))

log_in_page()
center()
root.mainloop()
