from tkinter import *
from tkinter import ttk


def login_page():
    big_label = ttk.Style()
    big_label.configure('big.TLabel', font=('Times', 25))
    login_label = ttk.Label(text='Log-In', width='48', style='big.TLabel', anchor='center').grid(column=0, row=0, sticky=W+E)
    username_label = ttk.Label(text='Username').grid(column=0, row=1)
    username_entry = ttk.Entry().grid(column=0, row=2)
    password_label = ttk.Label(text='Password').grid(column=0, row=3)
    password_entry = ttk.Entry().grid(column=0, row=4)
    signup_button = ttk.Button(text='Log-in').grid(column=0, row=5)
    login_button = ttk.Button(text='Sign-up', command=signup_page).grid(column=0, row=6)


def signup_page():
    big_label = ttk.Style()
    big_label.configure('big.TLabel', font=('Times', 25))
    signup_label = ttk.Label(text='Sign-up', width='48', style='big.TLabel', anchor='center').grid(column=0, row=0,
                                                                                                   sticky=W+E)
    username_label = ttk.Label(text='Username').grid(column=0, row=1)
    username_entry = ttk.Entry().grid(column=0, row=2)
    password_label = ttk.Label(text='Password').grid(column=0, row=3)
    password_entry = ttk.Entry().grid(column=0, row=4)
    signup_button = ttk.Button(text='Sign-up', command=login_page).grid(column=0, row=5)
    login_button = ttk.Button(text='Login-in', command=login_page).grid(column=0, row=6)
