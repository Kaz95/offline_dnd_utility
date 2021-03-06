from tkinter import *
from tkinter import ttk, Menu, simpledialog
from stores import stores
import sql
import account
import setup
import database
import character
import error_box
import threading
import queue
import static_functions
import os
import sys


# Dictionary used to store account and character objects, representing the current user information.
user_info = {'acc': None, 'char': None, 'inv': 1}

# Dictionaries used to capture treeview selection events. Value will be a treeview item.
# TODO: Verify if item is stored as tuple or string and provide comment example
gen_selected = {'selected': 'none'}
bs_selected = {'selected': 'none'}
stable_selected = {'selected': 'none'}
ship_selected = {'selected': 'none'}
inv_selected = {'selected': 'none'}
recent_selection = {'selected': 'None'}


# TODO: unit test with assertEqual.
# Clears dictionaries storing account information objects.
def log_out():
    print('-----Logged Out-----')
    user_info['acc'] = None
    user_info['char'] = None
    # user_info['inv'] = None


# Generic function that is passed a tuple with a single value.
# Value represents both the item_id (database) and the item id (tkinter gui).
# TODO: unit test with assertEqual
def new_selection(some_selection):
    recent_selection['selected'] = some_selection


class MainWindow:
    def __init__(self, root):
        self.main_thread = threading.main_thread()
        # These two super class variables are used for handling clean program exit.
        self.closed = True
        self.queue = queue.Queue()

        # self.conn = database.create_connection(database.db)
        self.root = root

        # This overrides tkinter's handling of exiting the program.
        self.root.protocol("WM_DELETE_WINDOW", self.close_both_threads)

        root.title('DnD Utility')
        big_label = ttk.Style()
        big_label.configure('big.TLabel', font=('Times', 25))
        self.clear()

        # Entry callback functions registration

        self.is_alnum = self.root.register(static_functions.entry_is_alnum_callback)
        self.is_digit = self.root.register(static_functions.entry_is_digit_callback)
        self.is_alpha = self.root.register(static_functions.entry_is_alpha_callback)
        self.failed_is_digit = self.root.register(error_box.failed_validation_is_digit)
        self.failed_is_alnum = self.root.register(error_box.failed_validation_is_alnum)
        self.failed_is_alpha = self.root.register(error_box.failed_validation_is_alpha)

    # Command to handle closing of both threads on tkinter window exit.
    def close_both_threads(self):
        if threading.active_count() == 2:
            answer = error_box.cancel_install()
            if answer:
                closed = True
                self.queue.put(closed)
        else:
            self.root.quit()

    # clears (forgets) all widgets currently attached to root window.
    def clear(self):
        for widget in self.root.grid_slaves():
            widget.grid_forget()

    # Returns width and height of screen in pixels.
    def screen_size(self):
        self.root.update()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        print(width, 'x', height)
        return {'w': width, 'h': height}

    # Centers root window. Dashboard and install required a different formula to center properly.
    # TODO: This is a quick and dirty solution
    # TODO: Magic numbers are bad mkay.
    def center(self, dash=None):
        cur_size = self.screen_size()
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        x = (ws / 2) - (cur_size['w'] / 2)
        y = (hs / 2) - (cur_size['h'] / 2)
        if dash == [1019, 647]:
            y -= 250
            self.root.geometry('%dx%d+%d+%d' % (dash[0], dash[1], x, y))
        elif dash == [820, 178]:
            self.root.geometry('%dx%d+%d+%d' % (dash[0], dash[1], x, y))
        else:
            self.root.geometry('%dx%d+%d+%d' % (cur_size['w'], cur_size['h'], x, y))

        self.root.update()

    # Clears dictionary holding account information objects. Pushes to login page.
    def logout_command(self):
        log_out()
        LoginPage(self.root)
        self.center()


class InstallPage(MainWindow):
    def __init__(self, root):
        # Removes the DB file. There's is no way to reach this page without creating a DB file first.
        os.remove(database.db)

        self.conn = database.create_connection(database.db)
        self.count = 0
        # TODO: I don't think I use max_count. I could, but I don't think I am. Maybe make private class var?
        # TODO: Check count via 'count' dictionary in api. Hard code as maximum for install bar.
        self.max_count = 256

        MainWindow.__init__(self, root)

        if setup.wrong_schema(self.conn):
            self.title_install_label = ttk.Label(text='Installing....', width='48', style='big.TLabel', anchor='center')
            self.install_bar = ttk.Progressbar(root, orient=HORIZONTAL, length=200, mode='determinate')
            self.install_button = Button(text='Install', bg='gray', command=self.start)

            self.title_install_label.grid(column=0, row=0, sticky=W + E)
            self.install_bar.grid(column=0, row=1)
            self.install_button.grid(column=0, row=2)

        else:
            LoginPage(self.root)

        self.center()

    # Starts instillation process in a separate thread from main.
    def start(self):
        self.install_button.config(state='disabled')

        def real_start():
            # Loops is required to push login page after successful installation.
            while True:
                con = database.create_connection(database.db)
                self.install_bar['value'] = 0
                self.install_bar['maximum'] = 256
                # update_mainloop()
                wrg_schema = setup.wrong_schema(con)
                if not wrg_schema:
                    LoginPage(self.root)
                    break
                elif wrg_schema:
                    setup.create_schema(con)
                    setup.stock_stores(con, self.install_bar, self.root, self.title_install_label, self.queue)

        threading.Thread(target=real_start).start()


class LoginPage(MainWindow):
    def __init__(self, root):
        # Connection used to check if the database is setup correctly. Is discarded no matter the outcome.
        self.temp_conn = database.create_connection(database.db)
        self.thread_id = threading.get_ident()

        MainWindow.__init__(self, root)
        if setup.wrong_schema(self.temp_conn) or database.wrong_item_count(self.temp_conn):
            self.temp_conn.close()
            InstallPage(self.root)
        else:
            self.temp_conn.close()
            self.conn = database.create_connection(database.db)

            self.username_label = ttk.Label(text='Username')
            self.password_label = ttk.Label(text='Password')
            self.title_login_label = ttk.Label(text='Log-In', width='48', style='big.TLabel', anchor='center')

            self.login_page_username_entry = ttk.Entry(validate='key', validatecommand=(self.is_alnum, '%P'),
                                                       invalidcommand=self.failed_is_alnum)

            self.login_page_password_entry = ttk.Entry(validate='key', validatecommand=(self.is_alnum, '%P'),
                                                       invalidcommand=self.failed_is_alnum)

            self.login_page_login_button = Button(text='Log-in', bg='gray', command=self.login_page_login_command)
            # self.login_page_login_button = Button(text='Log-in', bg='gray')
            self.login_page_signup_button = Button(text='Sign-up', bg='gray', command=lambda: SignupPage(self.root))
            # self.login_page_signup_button = Button(text='Sign-up', bg='gray')

            self.title_login_label.grid(column=0, row=0, sticky=W + E)
            self.username_label.grid(column=0, row=1)
            self.login_page_username_entry.grid(column=0, row=2)
            self.password_label.grid(column=0, row=3)
            self.login_page_password_entry.grid(column=0, row=4)
            self.login_page_login_button.grid(column=0, row=5)
            self.login_page_signup_button.grid(column=0, row=6)

            static_functions.clear_entry(self.login_page_username_entry)
            static_functions.clear_entry(self.login_page_password_entry)
            self.login_page_username_entry.focus()

            self.center([820, 178])

    # Authenticates information passed to entry boxes against DB. Pushes to character creation page
    def login_page_login_command(self):
        print(threading.get_ident())
        print(self.thread_id)
        if self.thread_id != threading.get_ident():
            error_box.wrong_username()
            LoginPage(self.root)
            return
        # account.log_in(conn, login_page_username_entry.get(), login_page_password_entry.get())
        user_info['acc'] = account.log_in(self.conn, self.login_page_username_entry.get(), self.login_page_password_entry.get())
        if user_info['acc'] is not None:
            if account.account_has_characters(self.conn, user_info['acc'].id):
                CharacterSelectionPage(self.root)
            else:
                CharacterCreationPage(self.root)


class SignupPage(MainWindow):
    def __init__(self, root):
        self.conn = database.create_connection(database.db)

        MainWindow.__init__(self, root)

        self.title_signup_label = ttk.Label(text='Sign-up', width='48', style='big.TLabel', anchor='center')
        self.username_label = ttk.Label(text='Username')
        self.password_label = ttk.Label(text='Password')

        self.signup_page_username_entry = ttk.Entry(validate='key', validatecommand=(self.is_alnum, '%P'),
                                                    invalidcommand=self.failed_is_alnum)

        self.signup_page_password_entry = ttk.Entry(validate='key', validatecommand=(self.is_alnum, '%P'),
                                                    invalidcommand=self.failed_is_alnum)

        self.signup_page_signup_button = Button(text='Sign-up', bg='gray', command=self.signup_page_signup_command)
        self.signup_page_login_button = Button(text='Log-in', bg='gray', command=lambda: LoginPage(self.root))

        self.title_signup_label.grid(column=0, row=0, sticky=W + E)
        self.username_label.grid(column=0, row=1)
        self.signup_page_username_entry.grid(column=0, row=2)
        self.password_label.grid(column=0, row=3)
        self.signup_page_password_entry.grid(column=0, row=4)
        self.signup_page_signup_button.grid(column=0, row=5)
        self.signup_page_login_button.grid(column=0, row=6)

        static_functions.clear_entry(self.signup_page_username_entry)
        static_functions.clear_entry(self.signup_page_password_entry)
        self.signup_page_username_entry.focus()

    # Creates account row based on entry boxes and adds to DB. Pushes to login page.
    def signup_page_signup_command(self):
        if account.user_creates_account(self.conn, self.signup_page_username_entry.get(), self.signup_page_password_entry.get()):
            LoginPage(self.root)


class CharacterCreationPage(MainWindow):
    def __init__(self, root):
        self.conn = database.create_connection(database.db)

        MainWindow.__init__(self, root)

        self.title_char_creation__label = ttk.Label(text='Character Creation', width='48', style='big.TLabel',
                                                    anchor='center')

        self.currency_label = ttk.Label(text='Currency')
        self.name_label = ttk.Label(text='Name')

        self.name_entry = ttk.Entry(validate='key', validatecommand=(self.is_alpha, '%P'), invalidcommand=self.failed_is_alpha)
        self.currency_entry = ttk.Entry(validate='key', validatecommand=(self.is_digit, '%P'), invalidcommand=self.failed_is_digit)

        self.create_character_button = Button(text='Create', bg='gray', command=self.create_character_command)
        self.logout_button = Button(text='Log-out', bg='gray', command=self.logout_command)

        self.title_char_creation__label.grid(column=0, row=0, sticky=W + E)
        self.name_label.grid(column=0, row=1)
        self.name_entry.grid(column=0, row=2)
        self.currency_label.grid(column=0, row=3)
        self.currency_entry.grid(column=0, row=4)
        self.create_character_button.grid(column=0, row=5)
        self.logout_button.grid(column=0, row=6)

        self.name_entry.focus()

    # Creates character row based on entry boxes and adds to DB. Pushes to character selection page.
    def create_character_command(self):
        name = self.name_entry.get()
        currency = self.currency_entry.get()
        if character.character_creation(self.conn, user_info['acc'].id, name, currency):
            CharacterSelectionPage(self.root)


class CharacterSelectionPage(MainWindow):
    def __init__(self, root):
        self.conn = database.create_connection(database.db)

        MainWindow.__init__(self, root)

        self.title_char_select_label = ttk.Label(text='Character Selection', width='48', style='big.TLabel', anchor='center')
        self.characters_label = ttk.Label(text='Characters')
        self.chars_combo = ttk.Combobox(postcommand=self.populate_combo)
        self.select_button = Button(text='Select', bg='gray', command=self.select_command)
        self.delete_button = Button(text='Delete', bg='gray', command=self.delete_command)
        self.logout_button = Button(text='Log-out', bg='gray', command=self.logout_command)
        self.character_creation_button = Button(text='Character creation', bg='gray', command=lambda: CharacterCreationPage(self.root))

        self.title_char_select_label.grid(column=0, row=0, sticky=W + E)
        self.characters_label.grid(column=0, row=1)
        self.chars_combo.grid(column=0, row=2)
        self.select_button.grid(column=0, row=3)
        self.delete_button.grid(column=0, row=4)
        self.logout_button.grid(column=0, row=5, sticky=W + S)
        self.character_creation_button.grid(column=0, row=5, sticky=E + S)

        self.chars_combo.focus()

    # Query characters from DB based on current account id.
    # Slices name from tuples returned and appends to empty list. Sets combo values to list.
    # TODO: Might be able to apply list comprehension
    # TODO: unit test assertEqual temp_combo_list.
    def populate_combo(self):
        temp_combo_list = []
        acc_id = user_info['acc'].id
        characters_tuple = sql.execute_fetchall_sql(self.conn, sql.query_all_characters(), acc_id)
        for thing in characters_tuple:
            temp_combo_list.append(thing[1])
        self.chars_combo['values'] = temp_combo_list

    # TODO: Might be able to apply list comprehension
    # Deletes a character from the front(gui) and back(DB) end.
    def delete_command(self):
        temp = {}
        char_selected = self.chars_combo.get()
        acc_id = user_info['acc'].id
        characters_tuple_list = sql.execute_fetchall_sql(self.conn, sql.query_all_characters(), acc_id)
        for tup in characters_tuple_list:
            temp[tup[1]] = tup[0]
        char_id = temp[char_selected]
        database.delete_character(self.conn, char_id)
        static_functions.clear_entry(self.chars_combo)
        print('-----character deleted-----')
        self.root.update()

    # Sets current character to a given character object, Character object is based on combobox value.
    # If no value is selected, displays error box.
    def select_command(self):
        try:
            user_info['char'] = character.load_character_object(self.conn, self.chars_combo.get())
            DashboardPage(self.root)
        except TypeError:
            error_box.no_character_selected()


class DashboardPage(MainWindow):
    def __init__(self, root):
        self.conn = database.create_connection(database.db)

        MainWindow.__init__(self, root)
        self.currency_dict = static_functions.convert_currency(user_info['char'].currency)

        self.gen_frame = LabelFrame(root, text='General Store')
        self.bs_frame = LabelFrame(root, text='Blacksmith')
        self.ship_frame = LabelFrame(root, text='Shipyard')
        self.stable_frame = LabelFrame(root, text='Stables')

        # Treeviews

        self.shipyard_treeview = ttk.Treeview(self.ship_frame)  # ttk.Treeview(parent) Sets a treeview to a given parent window
        self.general_store_treeview = ttk.Treeview(self.gen_frame)
        self.blacksmith_treeview = ttk.Treeview(self.bs_frame)
        self.stables_treeview = ttk.Treeview(self.stable_frame)
        self.inventory_treeview = ttk.Treeview(root)
        self.currency_treeview = ttk.Treeview(root)

        # List of store treeviews
        self.store_treeviews = [self.shipyard_treeview, self.stables_treeview, self.blacksmith_treeview, self.general_store_treeview]

        recent_selection['selected'] = 'None'
        inv_selected['selected'] = 'none'

        # Scrollbars
        self.gen_vsb = ttk.Scrollbar(self.gen_frame, orient="vertical", command=self.general_store_treeview.yview)
        self.bs_vsb = ttk.Scrollbar(self.bs_frame, orient="vertical", command=self.blacksmith_treeview.yview)
        self.stable_vsb = ttk.Scrollbar(self.stable_frame, orient="vertical", command=self.stables_treeview.yview)

        self.general_store_treeview.configure(yscrollcommand=self.gen_vsb.set)
        self.blacksmith_treeview.configure(yscrollcommand=self.bs_vsb.set)
        self.stables_treeview.configure(yscrollcommand=self.stable_vsb.set)

        # TODO: Refactor menu names, they are currently shite.
        # Menus

        store_popup_menu = Menu(tearoff=False)
        store_popup_menu.add_command(label='Add Item', command=self.add_command)

        inventory_popup_menu = Menu(tearoff=False)
        inventory_popup_menu.add_command(label='Subtract One', command=self.subtract_one_command)
        inventory_popup_menu.add_command(label='Remove Item', command=self.remove_command)
        inventory_popup_menu.add_command(label='Update Quantity', command=self.update_quantity_command)

        currency_popup_menu = Menu(tearoff=False)
        update_submenu = Menu(tearoff=False)
        add_submenu = Menu(tearoff=False)
        subtract_submenu = Menu(tearoff=False)

        update_submenu.add_command(label='Gold', command=lambda: self.update_currency_command('gold'))
        update_submenu.add_command(label='Silver', command=lambda: self.update_currency_command('silver'))
        update_submenu.add_command(label='Copper', command=lambda: self.update_currency_command('copper'))

        add_submenu.add_command(label='Gold', command=lambda: self.add_currency_command('gold'))
        add_submenu.add_command(label='Silver', command=lambda: self.add_currency_command('silver'))
        add_submenu.add_command(label='Copper', command=lambda: self.add_currency_command('copper'))

        subtract_submenu.add_command(label='Gold', command=lambda: self.subtract_currency_command('gold'))
        subtract_submenu.add_command(label='Silver', command=lambda: self.subtract_currency_command('silver'))
        subtract_submenu.add_command(label='Copper', command=lambda: self.subtract_currency_command('copper'))

        currency_popup_menu.add_cascade(label='Update', menu=update_submenu)
        currency_popup_menu.add_cascade(label='Add', menu=add_submenu)
        currency_popup_menu.add_cascade(label='Subtract', menu=subtract_submenu)

        def select_item(event, some_tree):
            iid = some_tree.identify_row(event.y)
            if iid is not None:
                print(iid)
                some_tree.selection_set(iid)
                return True

        def general_store_popup(event):
            if select_item(event, self.general_store_treeview):
                store_popup_menu.post(event.x_root, event.y_root)

        def blacksmith_popup(event):
            if select_item(event, self.blacksmith_treeview):
                store_popup_menu.post(event.x_root, event.y_root)

        def stables_popup(event):
            if select_item(event, self.stables_treeview):
                store_popup_menu.post(event.x_root, event.y_root)

        def shipyard_popup(event):
            if select_item(event, self.shipyard_treeview):
                store_popup_menu.post(event.x_root, event.y_root)

        def inventory_popup(event):
            if select_item(event, self.inventory_treeview):
                inventory_popup_menu.post(event.x_root, event.y_root)

        def currency_popup(event):
            currency_popup_menu.post(event.x_root, event.y_root)

        def format_store(some_treeview):
            some_treeview.tag_configure('gold', image=gold_img)
            some_treeview.tag_configure('silver', image=silver_img)
            some_treeview.tag_configure('copper', image=copper_img)
            some_treeview.config(columns='price')
            some_treeview.column('price', width=85, anchor='center')
            some_treeview.column('#0', width=150)
            some_treeview.heading('price', text='Price')
            some_treeview.heading('#0', text='Item')

        for treeview in self.store_treeviews:
            format_store(treeview)

        # TODO: Verify purpose of error handling.
        try:
            self.populate_all_trees()
        except TclError:
            pass

        # Creates the initial currency item. If item exists, updates treeview instead.
        # TODO: Verify that error handling is both necessary and used correctly.
        try:
            self.currency_treeview.insert('', 'end', 'gold', text=self.currency_dict['gp'])

        except TclError:
            print('tcl error')
            self.update_currency_treeview(self.currency_dict)

        # Binds
        self.shipyard_treeview.bind('<<TreeviewSelect>>', self.shipyard_callback)
        self.blacksmith_treeview.bind('<<TreeviewSelect>>', self.blacksmith_callback)
        self.stables_treeview.bind('<<TreeviewSelect>>', self.stables_callback)
        self.inventory_treeview.bind('<<TreeviewSelect>>', self.inventory_callback)
        self.general_store_treeview.bind('<<TreeviewSelect>>', self.general_store_callback)

        # for treeview in self.store_treeviews:
        #     treeview.bind('<Button-3>', general_store_popup)

        self.general_store_treeview.bind('<Button-3>', general_store_popup)
        self.blacksmith_treeview.bind('<Button-3>', blacksmith_popup)
        self.stables_treeview.bind('<Button-3>', stables_popup)
        self.shipyard_treeview.bind('<Button-3>', shipyard_popup)

        self.inventory_treeview.bind('<Button-3>', inventory_popup)
        self.currency_treeview.bind('<Button-3>', currency_popup)

        # General grid formatting
        self.general_store_treeview.grid(row=0, column=0)
        self.blacksmith_treeview.grid(row=0, column=0)
        self.stables_treeview.grid(row=0, column=0)
        self.shipyard_treeview.grid(row=0, column=0)

        self.gen_vsb.grid(row=0, column=1, sticky='ns')
        self.bs_vsb.grid(row=0, column=1, sticky='ns')
        self.stable_vsb.grid(row=0, column=1, sticky='ns')

        self.gen_frame.grid(row=0, column=0)
        self.bs_frame.grid(row=0, column=1)
        self.stable_frame.grid(row=0, column=2)
        self.ship_frame.grid(row=0, column=3)

        # self.general_store_treeview.grid(row=0, column=0)
        # self.blacksmith_treeview.grid(row=0, column=1)
        # self.stables_treeview.grid(row=0, column=2)
        # self.shipyard_treeview.grid(row=0, column=3)
        self.inventory_treeview.grid(row=3, columnspan=4, sticky=W + E)
        self.currency_treeview.grid(row=2, columnspan=4)

        # Currency formatting

        self.currency_treeview.config(columns=['silver', 'copper'], height=1)
        self.currency_treeview.column('#0', width=55, anchor='center')
        self.currency_treeview.column('silver', width=55, anchor='center')
        self.currency_treeview.column('copper', width=65, anchor='center')
        self.currency_treeview.heading('#0', text='Gold', image=gold_img)
        self.currency_treeview.heading('silver', text='Silver', image=silver_img)
        self.currency_treeview.heading('copper', text='Copper', image=copper_img)
        self.currency_treeview.set('gold', 'silver', self.currency_dict['sp'])
        self.currency_treeview.set('gold', 'copper', self.currency_dict['cp'])

        # Inventory formatting
        self.inventory_treeview.tag_configure('gold', image=gold_img)
        self.inventory_treeview.tag_configure('silver', image=silver_img)
        self.inventory_treeview.tag_configure('copper', image=copper_img)
        self.inventory_treeview.config(columns=('quantity', 'unit_value'))
        self.inventory_treeview.column('quantity', width=2, anchor='center')
        self.inventory_treeview.heading('quantity', text='Quantity')
        self.inventory_treeview.column('unit_value', width=55, anchor='center')
        self.inventory_treeview.heading('unit_value', text='Unit Value')
        self.inventory_treeview.column('#0', width=700)
        self.inventory_treeview.heading('#0', text='Item')

        # Buttons
        self.buy = Button(text='Buy', bg='gray', command=self.buy_command)
        self.buy.grid(row=1, columnspan=4, sticky=W + E)
        self.sell = Button(text='Sell', bg='gray', activebackground='green', command=self.sell_command)
        self.sell.grid(row=4, columnspan=4, sticky=N + W + E)
        self.logout_button = Button(text='Log-out', bg='gray', command=self.logout_command)
        self.logout_button.grid(row=5, column=0, pady=50, sticky=S + W)
        self.dashboard_page_character_select_button = Button(text='Character Selection', bg='gray',
                                                             command=self.char_select_command)

        self.dashboard_page_character_select_button.grid(row=5, column=3, pady=50, sticky=S + E)

        self.populate_inventory()

        cur_size = self.screen_size()
        # TODO: Magic numbers are bad mkay.
        if cur_size['h'] != 647:
            self.center([1019, 647])

    # Populates the four treeview widgets that, makeup the dashboard page, with items.
    def populate_all_trees(self):
        static_functions.populate_tree(sql.query_item_from_store(), self.conn, self.blacksmith_treeview, 'Blacksmith')
        static_functions.populate_tree(sql.query_item_from_store(), self.conn,  self.shipyard_treeview, 'Shipyard')
        static_functions.populate_tree(sql.query_item_from_store(), self.conn,  self.general_store_treeview, 'General Store')
        static_functions.populate_tree(sql.query_item_from_store(), self.conn,  self.stables_treeview, 'Stables')

    # TODO: DRY
    # Gets recently selected treeview item as tuple.
    # Tries to get name of item in each treeview. It will only work with one of them presumably.
    # Query DB for item value based on name of item.
    # Return Item value as integer.
    def recent_select_value(self):
        item = recent_selection['selected']
        print(item)
        item_name = None
        for treeview in self.store_treeviews:
            try:
                item_name = treeview.item(item[0])['text']
            except TclError:
                pass
        item_value = sql.execute_fetchone_sql(self.conn, sql.query_store_item_value(), item_name)
        return item_value[0]

    # Changes activebackground color of buy button to a given color.
    def change_button_background(self, color):
        self.buy.config(activebackground=color)

    # Changes buy button activebackground color
    # based on if a character object's currency value is greater than a given item value.
    def toggle_affordable_color(self, item_value):
        if item_value >= user_info['char'].currency:
            self.change_button_background('red')
        elif item_value < user_info['char'].currency:
            self.change_button_background('green')

    # Gets item value of recent treeview selection and toggles button activebackground color based on that value.
    def check_value_and_toggle(self):
        try:
            item_value = self.recent_select_value()
            self.toggle_affordable_color(item_value)
        # TODO: Remove later
        except TypeError:
            print('ima type error')

    # Sets recent selection and toggles previous selection.
    def generic_selection_callback(self, event, some_dict, some_treeview):
        some_dict['selected'] = some_treeview.selection()
        if recent_selection['selected'] == 'None' or len(some_treeview.selection()) > 0:
            new_selection(some_dict['selected'])

        for tree in self.store_treeviews:
            if len(tree.selection()) > 0 and tree.selection() != recent_selection['selected']:
                tree.selection_toggle(tree.selection())

        if len(self.inventory_treeview.selection()) > 0 and self.inventory_treeview.selection() != recent_selection['selected']:
            self.inventory_treeview.selection_toggle(self.inventory_treeview.selection())

    def general_store_callback(self, event):
        self.generic_selection_callback(event, gen_selected, self.general_store_treeview)
        self.check_value_and_toggle()

    def blacksmith_callback(self, event):
        self.generic_selection_callback(event, bs_selected, self.blacksmith_treeview)
        self.check_value_and_toggle()

    def stables_callback(self, event):
        self.generic_selection_callback(event, stable_selected, self.stables_treeview)
        self.check_value_and_toggle()

    def shipyard_callback(self, event):
        self.generic_selection_callback(event, ship_selected, self.shipyard_treeview)
        self.check_value_and_toggle()

    # The inventory callback function also attempts to deselect all previously selections in store widgets.
    def inventory_callback(self, event):
        self.generic_selection_callback(event, inv_selected, self.inventory_treeview)

    def char_select_command(self):
        CharacterSelectionPage(self.root)

    # Populates inventory treeview from a list of DB item tuples.
    def populate_inventory_treeview_db(self, db_char_items):
        for item in db_char_items:
            converted_value = static_functions.convert_currency(item[2])
            cur_type = static_functions.inspecto_gadget(converted_value)
            item_id = self.inventory_treeview.insert('', 'end', text=item[0])
            static_functions.img_tag(self.inventory_treeview, item_id, cur_type)
            self.inventory_treeview.set(item_id, 'quantity', item[1])
            self.inventory_treeview.set(item_id, 'unit_value', converted_value[cur_type])

    # Repopulates inventory treeview via DB query
    def populate_inventory(self):
        char_items = sql.execute_fetchall_sql(self.conn, sql.query_all_character_items(), user_info['char'].id)

        if len(char_items) > 0:
            self.populate_inventory_treeview_db(char_items)

    # Sets quantity column of a given (gui)item to 1.
    def new_inventory_quantity(self, some_item):
        self.inventory_treeview.set(some_item, 'quantity', 1)

    # Sets a given item's unit value column to a given value.
    def new_inventory_unit_value(self, some_item, value):
        self.inventory_treeview.set(some_item, 'unit_value', value)

    # Updates currency treeview based on a (presumably updated) currency dictionary.
    def update_currency_treeview(self, some_dict):
        self.currency_treeview.item('gold', text=some_dict['gp'])
        self.currency_treeview.set('gold', 'silver', some_dict['sp'])
        self.currency_treeview.set('gold', 'copper', some_dict['cp'])

    # Adds 1 to a given (gui)item's quantity column value.
    def add_one_inventory_quantity(self, some_item):
        quantity = self.inventory_treeview.set(some_item, 'quantity')
        quantity += 1
        self.inventory_treeview.set(some_item, 'quantity', quantity)

    # Subtracts 1 to a given (gui)item's quantity column value.
    def minus_one_inventory_quantity(self, some_item):
        quantity = self.inventory_treeview.set(some_item, 'quantity')
        quantity -= 1
        self.inventory_treeview.set(some_item, 'quantity', quantity)

    # {'I001': 'Net'}
    def inv_tree_dictionary_names(self, some_tup):
        temp = {}
        for thing in some_tup:
            temp[thing] = self.inventory_treeview.item(thing, 'text')
        return temp

    # {'Net': 'I001'}
    def inv_tree_dictionary_ids(self, some_tup):
        temp = {}
        for thing in some_tup:
            temp[self.inventory_treeview.item(thing, 'text')] = thing
        return temp

    # adds new top level item to inventory treeview.
    def new_tree_item(self, some_treeview, some_callback):
        item_name = some_treeview.item(some_callback[0])['text']
        item_value = sql.execute_fetchone_sql(self.conn, sql.query_store_item_value(), item_name)
        converted_value = static_functions.convert_currency(item_value[0])
        cur_type = static_functions.inspecto_gadget(converted_value)
        new_item = self.inventory_treeview.insert('', 'end', text=some_treeview.item(some_callback[0])['text'])
        static_functions.img_tag(self.inventory_treeview, new_item, cur_type)
        self.new_inventory_quantity(new_item)
        self.new_inventory_unit_value(new_item, converted_value[cur_type])

    # Loops through inventory treeview item names.
    # Compares a given callbacks text value to each name.
    # If call back equals name, add one to quantity value.
    # Else, add new inventory treeview item.
    def try_add_one_gui_quantity(self, some_treeview, some_callback):
        inv_items_tuple = self.inventory_treeview.get_children()

        names_dictionary = self.inv_tree_dictionary_names(inv_items_tuple)
        id_dictionary = self.inv_tree_dictionary_ids(inv_items_tuple)
        item_id = some_treeview.item(some_callback[0])
        item_name = item_id['text']

        for value in names_dictionary.values():
            if value == item_name:
                self.add_one_inventory_quantity(id_dictionary[item_name])
                return None  # Required to break out of function all together if match is found.
            elif id_dictionary[value] in inv_items_tuple:  # If name in inventory treeview, but not match, continue.
                continue

        self.new_tree_item(some_treeview, some_callback)

    # TODO: DRY
    # Adds a new GUI item to inventory treeview if item name not already in.
    # If already in, adds one to the quantity column value of a given item.
    def buy_item_gui(self, some_callback):
        stores_dic = stores()

        if len(self.inventory_treeview.get_children()) != 0:
            if some_callback[0] in stores_dic['Ship']:
                self.try_add_one_gui_quantity(self.shipyard_treeview, some_callback)

            elif some_callback[0] in stores_dic['BS']:
                self.try_add_one_gui_quantity(self.blacksmith_treeview, some_callback)

            elif some_callback[0] in stores_dic['GS']:
                self.try_add_one_gui_quantity(self.general_store_treeview, some_callback)

            elif some_callback[0] in stores_dic['Stables']:
                self.try_add_one_gui_quantity(self.stables_treeview, some_callback)

        else:
            if some_callback[0] in stores_dic['Ship']:
                self.new_tree_item(self.shipyard_treeview, some_callback)
            elif some_callback[0] in stores_dic['BS']:
                self.new_tree_item(self.blacksmith_treeview, some_callback)
            elif some_callback[0] in stores_dic['GS']:
                self.new_tree_item(self.general_store_treeview, some_callback)
            elif some_callback[0] in stores_dic['Stables']:
                self.new_tree_item(self.stables_treeview, some_callback)

    # Subtracts one from a give  gui item's quantity column value if given item has a quantity greater than one.
    # Delete gui item if quantity column value less than one
    def sell_item_gui(self, some_callback):
        quantity = self.inventory_treeview.set(some_callback, 'quantity')
        if quantity > 1:
            self.minus_one_inventory_quantity(some_callback)
        else:
            self.inventory_treeview.delete(some_callback)

    # Updates quantity of recently selected inventory item based on value returned from simple dialogue.
    # Displays error box if no items elected.
    def update_quantity_command(self):
        try:
            tup = recent_selection['selected']
            item_name = self.inventory_treeview.item(tup[0])['text']
            answer = simpledialog.askinteger('Input',
                                             f'How many {item_name} do you have?',
                                             parent=self.root,
                                             minvalue=1,
                                             maxvalue=1000)

            self.inventory_treeview.set(tup, 'quantity', answer)
            sql.execute_sql(self.conn, sql.update_quantity(), answer, item_name, user_info['inv'])

        except TclError:
            error_box.no_inventory_item_selected()

    # Updates a given currency type's value in treeview based on value returned from simpledialogue.
    def update_currency_command(self, cur_type):
        if cur_type == 'gold':
            answer = simpledialog.askinteger('Input',
                                             f'How much {cur_type} do you have?',
                                             minvalue=0,
                                             maxvalue=100000)

            cur_gold_value = self.currency_treeview.item('gold', 'text')
            diff = answer - cur_gold_value
            diff = diff * 100
            user_info['char'].currency += diff
            user_info['char'].update_currency_db(self.conn)
            self.currency_treeview.item('gold', text=answer)

        elif cur_type == 'silver':
            answer = simpledialog.askinteger('Input',
                                             f'How much {cur_type} do you have?',
                                             minvalue=0,
                                             maxvalue=9)

            cur_silver_value = self.currency_treeview.set('gold', 'silver')
            diff = answer - cur_silver_value
            diff = diff * 10
            user_info['char'].currency += diff
            user_info['char'].update_currency_db(self.conn)
            self.currency_treeview.set('gold', 'silver', answer)

        elif cur_type == 'copper':
            answer = simpledialog.askinteger('Input',
                                             f'How much {cur_type} do you have?',
                                             minvalue=0,
                                             maxvalue=9)

            cur_copper_value = self.currency_treeview.set('gold', 'copper')
            diff = answer - cur_copper_value
            user_info['char'].currency += diff
            user_info['char'].update_currency_db(self.conn)
            self.currency_treeview.set('gold', 'copper', answer)

    # Adds value returned from simple dialogue to a given currency type. Converts to base currency type for calculations
    # Then updates currency treeview
    def add_currency_command(self, cur_type):
        answer = simpledialog.askinteger('Input', f'How much {cur_type} do you want to add?', minvalue=1, maxvalue=100000)

        if cur_type == 'gold':
            answer = answer * 100
        elif cur_type == 'silver':
            answer = answer * 10

        user_info['char'].currency += answer
        user_info['char'].update_currency_db(self.conn)
        new_cur_dict = static_functions.convert_currency(user_info['char'].currency)
        self.update_currency_treeview(new_cur_dict)

    # Subtracts value returned from simple dialogue to a given currency type. Converts to base currency type for calculations
    # Then updates currency treeview
    def subtract_currency_command(self, cur_type):
        answer = simpledialog.askinteger('Input', f'How much {cur_type} do you want to add?', minvalue=1,
                                         maxvalue=100000)

        if cur_type == 'gold':
            answer = answer * 100
        elif cur_type == 'silver':
            answer = answer * 10
        if answer > user_info['char'].currency:
            error_box.cant_remove_that_much()
        else:
            user_info['char'].currency -= answer
            user_info['char'].update_currency_db(self.conn)
            new_cur_dict = static_functions.convert_currency(user_info['char'].currency)
            self.update_currency_treeview(new_cur_dict)

    # Attempts to retrieve the text value of given item_id in each store treeview.
    # Presumably only found inside one, so no error handling needed.
    def get_tree_item_name(self, item_id):
        item_name = None
        dic = stores()

        if item_id in dic['Ship']:
            item_name = self.shipyard_treeview.item(item_id)['text']
        elif item_id in dic['BS']:
            item_name = self.blacksmith_treeview.item(item_id)['text']
        elif item_id in dic['GS']:
            item_name = self.general_store_treeview.item(item_id)['text']
        elif item_id in dic['Stables']:
            item_name = self.stables_treeview.item(item_id)['text']

        return item_name

    # Same as buy command minus the currency.
    def add_command(self):
        try:
            print(recent_selection['selected'])
            item_name = self.get_tree_item_name(recent_selection['selected'][0])
            self.buy_item_gui(recent_selection['selected'])

            if not database.in_inventory(self.conn, user_info['inv'], item_name, '+'):
                user_info['char'].add_item_db(self.conn, item_name, user_info['acc'].id, user_info['inv'])

        except TypeError:
            error_box.no_store_item_selected()

    # TODO: Buy and sell commands require better error handling
    # Buys item on front (gui) and back (DB) end. Updates currency based on item value.
    def buy_command(self):
        # item_name = None
        affordable = None
        print(recent_selection['selected'])
        item_name = self.get_tree_item_name(recent_selection['selected'][0])

        if item_name is not None:
            affordable = user_info['char'].buy_sell(item_name, 'buy', self.conn)

        currency_dict = static_functions.convert_currency(user_info['char'].currency)
        self.update_currency_treeview(currency_dict)
        self.root.update()

        if affordable:
            self.buy_item_gui(recent_selection['selected'])

            if not database.in_inventory(self.conn, user_info['inv'], item_name, '+'):
                user_info['char'].add_item_db(self.conn, item_name, user_info['acc'].id, user_info['inv'])

        self.check_value_and_toggle()

    # Same as sell command minus the currency
    def remove_command(self):
        try:
            tup = inv_selected['selected']
            item = self.inventory_treeview.item(tup, 'text')
            self.inventory_treeview.delete(tup)
            database.delete_item(self.conn, item, user_info['inv'])

        except TclError:
            error_box.no_inventory_item_selected()

    # Same as sell command minus the currency
    def subtract_one_command(self):
        try:
            tup = inv_selected['selected']
            item = self.inventory_treeview.item(tup, 'text')
            self.sell_item_gui(inv_selected['selected'])

            if not database.in_inventory(self.conn, user_info['inv'], item, '-'):
                database.delete_item(self.conn, item, user_info['inv'])

        except TclError:
            error_box.no_inventory_item_selected()

    # Sells item and updates currency on front-end.
    def sell_command(self):
        tup = inv_selected['selected']
        item = self.inventory_treeview.item(tup, 'text')
        user_info['char'].buy_sell(item, 'sell', self.conn)
        currency_dict = static_functions.convert_currency(user_info['char'].currency)
        self.update_currency_treeview(currency_dict)
        self.sell_item_gui(inv_selected['selected'])
        self.root.update()

        if not database.in_inventory(self.conn, user_info['inv'], item, '-'):
            database.delete_item(self.conn, item, user_info['inv'])


main = Tk()
# Create directories required for DB file creation
os.makedirs("C:\\sqlite", exist_ok=True)
os.makedirs("C:\\sqlite\\db", exist_ok=True)


# TODO: This works with a non-onefile exe. No idea why. Figure it out ASAP.
# __location__ = os.path.realpath(
#     os.path.join(os.getcwd(), os.path.dirname(__file__)))
#
# gold_img = PhotoImage(file=os.path.join(__location__, 'gold.png'))
# silver_img = PhotoImage(file=os.path.join(__location__, 'silver.png'))
# copper_img = PhotoImage(file=os.path.join(__location__, 'copper.png'))

# TODO: This works with a one file exe. No idea why. Figure it out ASAP
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# Currency type icon images
gold_img = PhotoImage(file=resource_path('gold.png'))
silver_img = PhotoImage(file=resource_path('silver.png'))
copper_img = PhotoImage(file=resource_path('copper.png'))

# silver_img = PhotoImage(file='C:\\Users\\Terrance\\Desktop\\button_screens\\silver.png')
# copper_img = PhotoImage(file='C:\\Users\\Terrance\\Desktop\\button_screens\\copper.png')

dnd_utility = LoginPage(main)
main.mainloop()


