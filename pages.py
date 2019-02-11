from tkinter import *
from tkinter import ttk
from database import create_connection, count_rows
from stores import stores
# TODO Refactor element names to be more modular. 'Title Label' for example.


def clear(root):
    for i in root.grid_slaves():
        i.grid_forget()


def login_page(root):
    clear(root)
    big_label = ttk.Style()
    big_label.configure('big.TLabel', font=('Times', 25))
    login_label = ttk.Label(text='Log-In', width='48', style='big.TLabel', anchor='center').grid(column=0, row=0,
                                                                                                 sticky=W+E)
    username_label = ttk.Label(text='Username').grid(column=0, row=1)
    username_entry = ttk.Entry().grid(column=0, row=2)
    password_label = ttk.Label(text='Password').grid(column=0, row=3)
    password_entry = ttk.Entry().grid(column=0, row=4)
    login_button = ttk.Button(text='Log-in', command=lambda: character_creation_page(root)).grid(column=0, row=5)
    signup_button = ttk.Button(text='Sign-up', command=lambda: signup_page(root)).grid(column=0, row=6)


def signup_page(root):
    clear(root)
    big_label = ttk.Style()
    big_label.configure('big.TLabel', font=('Times', 25))
    signup_label = ttk.Label(text='Sign-up', width='48', style='big.TLabel', anchor='center').grid(column=0, row=0,
                                                                                                   sticky=W+E)
    username_label = ttk.Label(text='Username').grid(column=0, row=1)
    username_entry = ttk.Entry().grid(column=0, row=2)
    password_label = ttk.Label(text='Password').grid(column=0, row=3)
    password_entry = ttk.Entry().grid(column=0, row=4)
    signup_button = ttk.Button(text='Sign-up', command=lambda: login_page(root)).grid(column=0, row=5)
    login_button = ttk.Button(text='Login-in', command=lambda: login_page(root)).grid(column=0, row=6)


def character_creation_page(root):
    clear(root)
    big_label = ttk.Style()
    big_label.configure('big.TLabel', font=('Times', 25))
    title_label = ttk.Label(text='Character Creation', width='48', style='big.TLabel', anchor='center').grid(column=0,
                                                                                                             row=0,
                                                                                                             sticky=W+E)

    name_label = ttk.Label(text='Name').grid(column=0, row=1)
    name_entry = ttk.Entry().grid(column=0, row=2)
    currency_label = ttk.Label(text='Currency').grid(column=0, row=3)
    currency_entry = ttk.Entry().grid(column=0, row=4)
    create_character_button = ttk.Button(text='Create', command=lambda: character_selection_page(root)).grid(column=0,
                                                                                                             row=5)
    logout_button = ttk.Button(text='Log-out', command=lambda: login_page(root)).grid(column=0, row=6)


def character_selection_page(root):
    clear(root)
    big_label = ttk.Style()
    big_label.configure('big.TLabel', font=('Times', 25))
    title_label = ttk.Label(text='Character Selection', width='48', style='big.TLabel', anchor='center').grid(column=0,
                                                                                                              row=0,
                                                                                                              sticky=W+E)
    characters_label = ttk.Label(text='Characters').grid(column=0, row=1)
    chars_combo = ttk.Combobox(values=['1', '2', '3']).grid(column=0, row=2)
    select_button = ttk.Button(text='Select', command=lambda: dashboard(root)).grid(column=0, row=3)


def populate_tree(some_tree, some_store):
    conn = create_connection()
    with conn:
        for i in range(count_rows(conn, 'items')):
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

# # Example for inserting values
# Shipyard values
# shipyard_treeview.insert('', 'end', i[1], text=i[0])
# shipyard_treeview.insert('', 'end', a[1], text=a[0])
# shipyard_treeview.set(i[1], 'quantity', i[2])
# shipyard_treeview.set(a[1], 'quantity', a[2])


def dashboard(root):
    clear(root)
    selected = {'selected': 'none'}

    # Treeviews
    shipyard_treeview = ttk.Treeview(root)  # ttk.Treeview(parent) Sets a treeview to a given parent window
    general_store_treeview = ttk.Treeview(root)
    blacksmith_treeview = ttk.Treeview(root)
    stables_treeview = ttk.Treeview(root)
    inventory_treeview = ttk.Treeview(root)

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
    sell = ttk.Button(root, text='Sell', command=lambda: sell_item_gui(selected['selected'])).grid(row=3, columnspan=4,
                                                                                                   sticky=W+E)

    buy = ttk.Button(root, text='Buy', command=lambda: buy_item_gui(selected['selected'])).grid(row=1, columnspan=4,
                                                                                                sticky=W+E)
