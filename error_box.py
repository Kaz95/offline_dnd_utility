import tkinter
from tkinter import messagebox


def failed_validation_is_digit():
    messagebox.showerror('Input Error', 'Input must contain only numbers.')


def failed_validation_is_alpha():
    messagebox.showerror('Input Error', 'Input must contain only letters.')


def failed_validation_is_alnum():
    messagebox.showerror('Input Error', 'Input must be alphanumeric.')


def wrong_username():
    messagebox.showerror('Log-in Failed', 'No account associated with that username')


def wrong_password():
    messagebox.showerror(('Log-in Failed', 'Incorrect password'))


def username_taken():
    messagebox.showerror('Sign-up Failed', 'There is already an account with that username')


def character_name_taken():
    messagebox.showerror('Character Creation Failed', 'There is already a character with that name.')


