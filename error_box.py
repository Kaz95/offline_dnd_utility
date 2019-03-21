import tkinter
from tkinter import messagebox
# TODO: Not sure if I can or even need to test this.
# TODO: Will most likely be heavily altered during OOP refactor. Don't worry till then.


def failed_validation_is_digit():
    messagebox.showerror('Input Error', 'Input must contain only numbers.')


def failed_validation_is_alpha():
    messagebox.showerror('Input Error', 'Input must contain only letters.')


def failed_validation_is_alnum():
    messagebox.showerror('Input Error', 'Input must be alphanumeric.')


def wrong_username():
    messagebox.showerror('Log-in Failed', 'No account associated with that username')


def wrong_password():
    messagebox.showerror('Log-in Failed', 'Incorrect password')


def username_taken():
    messagebox.showerror('Sign-up Failed', 'There is already an account with that username')


def character_name_taken():
    messagebox.showerror('Character Creation Failed', 'There is already a character with that name.')


def no_character_selected():
    messagebox.showerror('No Character Selected', 'Whoops! You forgot to select a character.')


def no_store_item_selected():
    messagebox.showerror('No Item Selected', 'Whoops! You forgot to select a store item.')


def no_inventory_item_selected():
    messagebox.showerror('No Item Selected', 'Whoops! You forgot to select an inventory item.')


def cant_remove_that_much():
    messagebox.showerror('Removal Failed', 'You can\'t remove more currency than you have')
