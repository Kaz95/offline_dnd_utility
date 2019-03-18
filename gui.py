from tkinter import *
from tkinter import ttk
from tkinter import Menu
from tkinter import simpledialog
from stores import stores
import sql
import account
import setup
import database
import character
import error_box
import threading
import static_functions

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


# TODO: unit test with assertEqual.
# Clears dictionaries storing account information objects.
def log_out():
    print('-----Logged Out-----')
    user_info['acc'] = None
    user_info['char'] = None
    user_info['inv'] = None


# Deletes a list of inventory treeview items from 'cache' based on a given character ID.
def clear_cache(char_id):
    print(f'-----{char_id} cache deleted-----')
    del inv_cache[char_id]


# Generic function that is passed a tuple with a single value.
# Value represents both the item_id (database) and the item id (tkinter gui).
# TODO: unit test with assertEqual
def new_selection(some_selection):
    recent_selection['selected'] = some_selection


class MainWindow:
    def __init__(self, root):
        self.conn = database.create_connection(database.db)
        self.root = root
        root.title('DnD Utility')
        big_label = ttk.Style()
        big_label.configure('big.TLabel', font=('Times', 25))

        # Entry callback functions registration

        self.is_alnum = self.root.register(static_functions.entry_is_alnum_callback)
        self.is_digit = self.root.register(static_functions.entry_is_digit_callback)
        self.is_alpha = self.root.register(static_functions.entry_is_alpha_callback)
        self.failed_is_digit = self.root.register(error_box.failed_validation_is_digit)
        self.failed_is_alnum = self.root.register(error_box.failed_validation_is_alnum)
        self.failed_is_alpha = self.root.register(error_box.failed_validation_is_alpha)

        # Treeviews

        self.shipyard_treeview = ttk.Treeview(root)  # ttk.Treeview(parent) Sets a treeview to a given parent window
        self.general_store_treeview = ttk.Treeview(root)
        self.blacksmith_treeview = ttk.Treeview(root)
        self.stables_treeview = ttk.Treeview(root)
        self.inventory_treeview = ttk.Treeview(root)
        self.currency_treeview = ttk.Treeview(root)

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
    def center(self, dash=None):
        cur_size = self.screen_size()
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        x = (ws / 2) - (cur_size['w'] / 2)
        y = (hs / 2) - (cur_size['h'] / 2)
        if dash == [953, 630]:
            y -= 250
            self.root.geometry('%dx%d+%d+%d' % (dash[0], dash[1], x, y))
            self.root.update()
        elif dash == [820, 178]:
            self.root.geometry('%dx%d+%d+%d' % (dash[0], dash[1], x, y))
            self.root.update()
        else:
            self.root.geometry('%dx%d+%d+%d' % (cur_size['w'], cur_size['h'], x, y))
            self.root.update()

    # Sets current user character ID to key with all current items in inventory treeview as value.
    def cache_inv(self):
        inv_cache[user_info['char'].id] = self.inventory_treeview.get_children()

    # Detaches all treeview items present in a list of treeview items.
    # Items list is retrieved from inventory cache dictionary.
    # Notes, detach does not permanently delete the item. It merely removes it from view.
    def detach_inv(self):
        self.inventory_treeview.detach(*inv_cache[user_info['char'].id])


class InstallPage(MainWindow):
    def __init__(self, root):

        self.count = 0
        self.max_count = 256

        MainWindow.__init__(self, root)
        self.clear()
        if setup.wrong_schema(self.conn):
            self.title_install_label = ttk.Label(text='Installing....', width='48', style='big.TLabel', anchor='center')
            self.install_bar = ttk.Progressbar(root, orient=HORIZONTAL, length=200, mode='determinate')
            self.install = Button(text='install', bg='gray', command=self.start)

            self.title_install_label.grid(column=0, row=0, sticky=W + E)
            self.install_bar.grid(column=0, row=1)
            self.install.grid(column=0, row=2)
        else:
            LoginPage(self.root)

        self.center()

    # Starts instillation process in a separate thread from main.
    def start(self):
        self.install.config(state='disabled')

        def real_start():
            while True:
                con = database.create_connection(database.db)
                self.install_bar['value'] = 0
                self.install_bar['maximum'] = 256
                # update_mainloop()
                if setup.wrong_schema(con):
                    setup.create_schema(con)
                    setup.stock_stores(con, self.install_bar, self.count, self.root, self.title_install_label)
                elif not setup.wrong_schema(con):
                    LoginPage(self.root)
                    break
                # if count >= max_count:
                #     log_in_page()

        threading.Thread(target=real_start).start()


class LoginPage(MainWindow):
    def __init__(self, root):
        MainWindow.__init__(self, root)
        self.clear()
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
        with self.conn:
            # account.log_in(conn, login_page_username_entry.get(), login_page_password_entry.get())
            user_info['acc'] = account.log_in(self.conn, self.login_page_username_entry.get(), self.login_page_password_entry.get())
            if user_info['acc'] is not None:
                if account.account_has_characters(self.conn, user_info['acc'].id):
                    CharacterSelectionPage(self.root)
                else:
                    CharacterCreationPage(self.root)


class SignupPage(MainWindow):
    def __init__(self, root):
        MainWindow.__init__(self, root)
        self.clear()
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
        with self.conn:
            if account.user_creates_account(self.conn, self.signup_page_username_entry.get(), self.signup_page_password_entry.get()):
                LoginPage(self.root)


class CharacterCreationPage(MainWindow):
    def __init__(self, root):
        MainWindow.__init__(self, root)
        self.clear()

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
        with self.conn:
            name = self.name_entry.get()
            currency = self.currency_entry.get()
            if character.character_creation(self.conn, user_info['acc'].id, name, currency):
                CharacterSelectionPage(self.root)

    # Clears dictionary holding account information objects. Pushes to login page.
    def logout_command(self):
        if not user_info['char']:
            log_out()
            LoginPage(self.root)
            self.center()
        else:
            self.cache_inv()
            self.detach_inv()
            log_out()
            LoginPage(self.root)
            self.center()


class CharacterSelectionPage(MainWindow):
    def __init__(self, root):
        MainWindow.__init__(self, root)
        self.clear()

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

    # Clears dictionary holding account information objects. Pushes to login page.
    def logout_command(self):
        if not user_info['char']:
            log_out()
            LoginPage(self.root)
            self.center()
        else:
            self.cache_inv()
            self.detach_inv()
            log_out()
            LoginPage(self.root)
            self.center()

    # Query characters from DB based on current account id.
    # Slices name from tuples returned and appends to empty list. Sets combo values to list.
    # TODO: unit test assertEqual temp_combo_list.
    def populate_combo(self):
        with self.conn:
            temp_combo_list = []
            acc_id = user_info['acc'].id
            characters_tuple = sql.execute_fetchall_sql(self.conn, sql.query_all_characters(), acc_id)
            for thing in characters_tuple:
                temp_combo_list.append(thing[1])
            self.chars_combo['values'] = temp_combo_list

    # Deletes a character from the front(gui) and back(DB) end.
    def delete_command(self):
        with self.conn:
            temp = {}
            char_selected = self.chars_combo.get()
            acc_id = user_info['acc'].id
            characters_tuple_list = sql.execute_fetchall_sql(self.conn, sql.query_all_characters(), acc_id)
            for tup in characters_tuple_list:
                temp[tup[1]] = tup[0]
            char_id = temp[char_selected]
            database.delete_character(self.conn, char_id)
            clear_cache(char_id)
            static_functions.clear_entry(self.chars_combo)
            print('-----character deleted-----')
            self.root.update()

    # Sets current character to a given character object, Character object is based on combobox value.
    def select_command(self):
        with self.conn:
            try:
                user_info['char'] = character.load_character_object(self.conn, self.chars_combo.get())
                print(user_info)
                DashboardPage(self.root)
            except TypeError:
                error_box.no_character_selected()


class DashboardPage(MainWindow):
    def __init__(self, root):

        MainWindow.__init__(self, root)
        self.currency_dict = user_info['char'].convert_currency()
        self.clear()

        # TODO: Refactor menu names, they are currently shite.
        # Menus

        store_popup_menu = Menu(tearoff=False)
        store_popup_menu.add_command(label='Add Item', command=self.add_command)

        inventory_popup_menu = Menu(tearoff=False)
        inventory_popup_menu.add_command(label='Remove Item', command=self.remove_command)
        inventory_popup_menu.add_command(label='Change Quantity', command=self.change_quantity_command)

        currency_popup_menu = Menu(tearoff=False)
        currency_type_menu = Menu(tearoff=False)

        currency_type_menu.add_command(label='Gold')
        currency_type_menu.add_command(label='Silver')
        currency_type_menu.add_command(label='Copper')

        currency_popup_menu.add_cascade(label='Update', menu=currency_type_menu)
        currency_popup_menu.add_cascade(label='Add', menu=currency_type_menu)
        currency_popup_menu.add_cascade(label='Subtract', menu=currency_type_menu)

        def store_popup(event):
            store_popup_menu.post(event.x_root, event.y_root)

        def inventory_popup(event):
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

        # Gen Store formatting
        format_store(self.general_store_treeview)

        # Blacksmith formatting
        format_store(self.blacksmith_treeview)

        # Stables formatting
        format_store(self.stables_treeview)

        # Shipyard formatting
        format_store(self.shipyard_treeview)

        # Populate trees
        try:
            self.populate_all_trees()
        except TclError:
            pass

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

        self.shipyard_treeview.bind('<Button-3>', store_popup)
        self.blacksmith_treeview.bind('<Button-3>', store_popup)
        self.stables_treeview.bind('<Button-3>', store_popup)
        self.general_store_treeview.bind('<Button-3>', store_popup)
        self.inventory_treeview.bind('<Button-3>', inventory_popup)
        self.currency_treeview.bind('<Button-3>', currency_popup)

        # General grid formatting
        self.general_store_treeview.grid(row=0, column=0)
        self.blacksmith_treeview.grid(row=0, column=1)
        self.stables_treeview.grid(row=0, column=2)
        self.shipyard_treeview.grid(row=0, column=3)
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
        if cur_size['h'] != 630:
            self.center([953, 630])

    # Populates the four treeview widgets that, makeup the dashboard page, with items.
    def populate_all_trees(self):
        static_functions.populate_tree(sql.query_item_from_store(), self.conn, self.blacksmith_treeview, 'Blacksmith')
        static_functions.populate_tree(sql.query_item_from_store(), self.conn,  self.shipyard_treeview, 'Shipyard')
        static_functions.populate_tree(sql.query_item_from_store(), self.conn,  self.general_store_treeview, 'General Store')
        static_functions.populate_tree(sql.query_item_from_store(), self.conn,  self.stables_treeview, 'Stables')

    # Gets recently selected treeview item as tuple.
    # Tries to get name of item in each treeview. It will only work with one of them presumably.
    # Query DB for item value based on name of item.
    # Return Item value as integer.
    def recent_select_value(self):
        item = recent_selection['selected']
        item_name = None
        try:
            item_name = self.general_store_treeview.item(item[0])['text']
        except TclError:
            pass

        try:
            item_name = self.blacksmith_treeview.item(item[0])['text']
        except TclError:
            pass

        try:
            item_name = self.stables_treeview.item(item[0])['text']
        except TclError:
            pass

        try:
            item_name = self.shipyard_treeview.item(item[0])['text']
        except TclError:
            pass

        item_value = sql.execute_fetchone_sql(self.conn, sql.query_store_item_value(), item_name)
        # item_value = api.get_item_value(item_name, character.Character.list_of_item_dicts)    # Depricated API call
        return item_value[0]

    # Changes activebackground color of buy button to a given color.
    def change_button_background(self, color):
        self.buy.config(activebackground=color)

    # Changes buy button activebackground color -
    # based on if a character object's currency value is greater than a given item value.
    def toggle_affordable_color(self, item_value):
        if item_value >= user_info['char'].currency:
            self.change_button_background('red')
        elif item_value < user_info['char'].currency:
            self.change_button_background('green')

    # Gets item value of recent treeview selection and toggles button activebackground color based on that value.
    def check_value_and_toggle(self):
        item_value = self.recent_select_value()
        self.toggle_affordable_color(item_value)

    def generic_selection_callback(self, event, some_dict, some_treeview):
        some_dict['selected'] = some_treeview.selection()
        new_selection(some_dict['selected'])

    def general_store_callback(self, event):
        # check_value_and_toggle()
        self.generic_selection_callback(event, gen_selected, self.general_store_treeview)
        self.check_value_and_toggle()

    def blacksmith_callback(self, event):
        # check_value_and_toggle()
        self.generic_selection_callback(event, bs_selected, self.blacksmith_treeview)
        self.check_value_and_toggle()

    def stables_callback(self, event):
        # check_value_and_toggle()
        self.generic_selection_callback(event, stable_selected, self.stables_treeview)
        self.check_value_and_toggle()

    def shipyard_callback(self, event):
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
        self.generic_selection_callback(event, ship_selected, self.shipyard_treeview)
        self.check_value_and_toggle()

    # The inventory callback function also attempts to deselect all previously selections in store widgets.
    def inventory_callback(self, event):
        # TODO: This is bugged. Toggle select causes unwanted behavior. Find a way to check if toggeled on.
        # try:
        #     blacksmith_treeview.selection_toggle(bs_selected['selected'])
        #     general_store_treeview.selection_toggle(gen_selected['selected'])
        #     stables_treeview.selection_toggle(stable_selected['selected'])
        #     shipyard_treeview.selection_toggle(ship_selected['selected'])
        # except TclError:
        #     pass

        self.generic_selection_callback(event, inv_selected, self.inventory_treeview)
        print(self.inventory_treeview.selection())
        print(self.inventory_treeview.item(self.inventory_treeview.selection(), 'text'))
        print(recent_selection['selected'])

    # Clears dictionary holding account information objects. Pushes to login page.
    def logout_command(self):
        if not user_info['char']:
            log_out()
            LoginPage(self.root)
            self.center()
        else:
            self.cache_inv()
            self.detach_inv()
            log_out()
            LoginPage(self.root)
            self.center()

    def char_select_command(self):
        self.cache_inv()
        self.detach_inv()
        CharacterSelectionPage(self.root)

    # Populates inventory treeview from a list of DB item tuples.
    def populate_inventory_treeview_db(self, db_char_items):
        for i in db_char_items:
            converted_value = static_functions.convert_currency(i[2])
            cur_type = static_functions.inspecto_gadget(converted_value)
            item_id = self.inventory_treeview.insert('', 'end', text=i[0])
            static_functions.img_tag(self.inventory_treeview, item_id, cur_type)
            self.inventory_treeview.set(item_id, 'quantity', i[1])
            self.inventory_treeview.set(item_id, 'unit_value', converted_value[cur_type])

    # Reattach items to inventory treeview from inventory cache dictionary.
    def populate_inventory_treeview_cache(self, tree_items_tup):
        for i in tree_items_tup:
            self.inventory_treeview.move(i, '', len(tree_items_tup))

    # Checks if current character ID has inventory in cache dictionary.
    # Reattaches if it does, else, populates via DB.
    def populate_inventory(self):
        char_items = sql.execute_fetchall_sql(self.conn, sql.query_all_character_items(), user_info['char'].id)

        # if user_info['char'].id in inv_cache.keys():
        #     self.populate_inventory_treeview_cache(inv_cache[user_info['char'].id])
        if len(char_items) > 0:
            self.populate_inventory_treeview_db(char_items)

    # Sets quantity column of a given (gui)item to 1.
    def new_inventory_quantity(self, some_item):
        self.inventory_treeview.set(some_item, 'quantity', 1)

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

    def change_quantity_command(self):
        tup = recent_selection['selected']
        item_name = self.inventory_treeview.item(tup[0])['text']
        answer = simpledialog.askinteger('Input',
                                         f'How many {item_name} do you have?',
                                         parent=self.root,
                                         minvalue=1,
                                         maxvalue=1000)

        self.inventory_treeview.set(tup, 'quantity', answer)
        sql.execute_sql(self.conn, sql.update_quantity(), answer, item_name, user_info['inv'])

    def add_command(self):
        item_name = None
        dic = stores()

        print(recent_selection['selected'])
        tup = recent_selection['selected']

        if tup[0] in dic['Ship']:
            item_name = self.shipyard_treeview.item(tup[0])['text']
        elif tup[0] in dic['BS']:
            item_name = self.blacksmith_treeview.item(tup[0])['text']
        elif tup[0] in dic['GS']:
            item_name = self.general_store_treeview.item(tup[0])['text']
        elif tup[0] in dic['Stables']:
            item_name = self.stables_treeview.item(tup[0])['text']

        self.buy_item_gui(recent_selection['selected'])
        if not database.in_inventory(self.conn, user_info['inv'], item_name, '+'):
            user_info['char'].add_item_db(self.conn, item_name, user_info['acc'].id, user_info['inv'])

    # TODO: Buy and sell commands require better error handling
    # Buys item on front (gui) and back (DB) end. Updates currency based on item value.
    def buy_command(self):

        item_name = None
        affordable = None
        dic = stores()

        print(recent_selection['selected'])
        tup = recent_selection['selected']

        if tup[0] in dic['Ship']:
            item_name = self.shipyard_treeview.item(tup[0])['text']
        elif tup[0] in dic['BS']:
            item_name = self.blacksmith_treeview.item(tup[0])['text']
        elif tup[0] in dic['GS']:
            item_name = self.general_store_treeview.item(tup[0])['text']
        elif tup[0] in dic['Stables']:
            item_name = self.stables_treeview.item(tup[0])['text']
        if item_name is not None:
            affordable = user_info['char'].buy_sell(item_name, 'buy', self.conn)

        currency_dict = user_info['char'].convert_currency()
        self.currency_treeview.item('gold', text=currency_dict['gp'])
        self.currency_treeview.set('gold', 'silver', currency_dict['sp'])
        self.currency_treeview.set('gold', 'copper', currency_dict['cp'])

        self.root.update()

        if affordable:
            self.buy_item_gui(recent_selection['selected'])
            if not database.in_inventory(self.conn, user_info['inv'], item_name, '+'):
                user_info['char'].add_item_db(self.conn, item_name, user_info['acc'].id, user_info['inv'])

        self.check_value_and_toggle()

    def remove_command(self):
        tup = inv_selected['selected']
        item = self.inventory_treeview.item(tup, 'text')
        self.sell_item_gui(inv_selected['selected'])
        # self.root.update()
        if not database.in_inventory(self.conn, user_info['inv'], item, '-'):
            database.delete_item(self.conn, item, user_info['inv'])

    # Sells item and updates currency on front-end.
    def sell_command(self):
        # print(recent_selection['selected'])
        tup = inv_selected['selected']
        item = self.inventory_treeview.item(tup, 'text')

        user_info['char'].buy_sell(item, 'sell', self.conn)

        currency_dict = user_info['char'].convert_currency()
        self.currency_treeview.item('gold', text=currency_dict['gp'])
        self.currency_treeview.set('gold', 'silver', currency_dict['sp'])
        self.currency_treeview.set('gold', 'copper', currency_dict['cp'])

        self.sell_item_gui(inv_selected['selected'])

        self.root.update()

        if not database.in_inventory(self.conn, user_info['inv'], item, '-'):
            database.delete_item(self.conn, item, user_info['inv'])


main = Tk()

# Currency icon images.
gold_img = PhotoImage(file='C:\\Users\\Terrance\\Desktop\\button_screens\\gold.png')
silver_img = PhotoImage(file='C:\\Users\\Terrance\\Desktop\\button_screens\\silver.png')
copper_img = PhotoImage(file='C:\\Users\\Terrance\\Desktop\\button_screens\\copper.png')

dnd_utility = InstallPage(main)
main.mainloop()


