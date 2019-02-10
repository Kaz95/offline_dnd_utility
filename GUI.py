from database import create_connection, count_rows
from tkinter import *
from tkinter import ttk


# TODO refactor to work for multiple treeviews(stores). Currently set to shipyard.
def populate_tree():
    conn = create_connection()
    with conn:
        for i in range(count_rows(conn, 'items')):
            d = {}
            i += 1
            k = """SELECT id, item FROM items WHERE id = ? AND store = 'Shipyard';"""
            cur = conn.cursor()
            cur.execute(k, [str(i)])
            o = cur.fetchone()
            try:
                d['id'] = o[0]
                d['name'] = o[1]
                treeview.insert('', 'end', d['id'], text=d['name'])
            except TypeError:
                continue

def callback(event):
    print(treeview.selection())  # Gets tuple with id as first value
    # print(treeview.set('I001', 'quantity'))
    # print(treeview.item('I001'))
    tup = treeview.selection()
    # Gets value of quantity for item selected.
    # Quantity can be swapped for another column
    print(treeview.set(tup[0], 'quantity'))
    print(treeview.item(tup[0])['text'])    # Gets name of item selected


root = Tk()     # Tk() Creates main window
treeview = ttk.Treeview(root)   # ttk.Treeview(parent) Sets a treeview to a given parent window
treeview.pack()    # Is the command that actually adds to a window. Until then things are bound, but not viewable.
treeview.config(columns='quantity')
treeview.column('quantity', width=50, anchor='center')
treeview.heading('quantity', text='Quantity')
treeview.column('#0', width=150)
treeview.heading('#0', text='Item')
populate_tree()
treeview.bind('<<TreeviewSelect>>', callback)
root.mainloop()





