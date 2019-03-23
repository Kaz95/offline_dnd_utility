import database
import sql
import error_box

db = 'C:\\sqlite\\db\\test.db'
mem = ':memory:'

# TODO: Test everything. Nothing here is currently tested....


# Account class. Stores account_id(primary key of account table), username, and password.
class Account:
    # Used to hold account info in {'username':'password'} format. Populated by load_account_archive()
    # log_in() then compares against it.
    account_archive_dictionary = {}

    def __init__(self, acc_id, username, password):
        self.id = acc_id
        self.username = username
        self.password = password


# TODO: If in makes more sense.
# Checks if username is taken. Return True/False respectively.
def username_taken(username):
    for key in Account.account_archive_dictionary.keys():
        if key == username:
            return True
        else:
            return False


# TODO: I think I can do an if in statement here as well. Even if im searching nested structures.
# Query a list of account IDs with character. Check if current account(ID) exists in that list. Returns True/False.
def account_has_characters(conn, acc_id):
    account_id_tups_list = sql.execute_fetchall_sql(conn, sql.query_accounts_with_characters())
    for tup in account_id_tups_list:
        if acc_id in tup:
            return True

    return False


# Attempt to create a new account. First checks if username exists in DB.
# Then adds new account info to DB if username does not exist.
# Displays an error box if username is taken.
def user_creates_account(conn, username, password):
    load_account_archive(conn)
    if username_taken(username):
        error_box.username_taken()
        return False
    else:
        acc_info = {'username': username, 'password': password}
        database.add_account_row(conn, sql.add_account_row(), acc_info)
        return True


# Loads all account username/password information and stores as key:value pairs in Account.log_in_dict.
def load_account_archive(conn):
    Account.account_archive_dictionary = {}
    list_of_username_password_tups = sql.execute_fetchall_sql(conn, sql.query_username_password())
    for tup in list_of_username_password_tups:
        Account.account_archive_dictionary[tup[0]] = tup[1]


# Returns account object if authenticated against account archive dictionary
# Displays an error box if not authenticated. Returns None.
def log_in(conn, username, password):
    load_account_archive(conn)  # Loads account info for authentication into Account.login_dic

    if username not in Account.account_archive_dictionary:
        error_box.wrong_username()
        return None
    elif username in Account.account_archive_dictionary and Account.account_archive_dictionary[username] != password:
        error_box.wrong_password()
        return None
    elif username in Account.account_archive_dictionary and Account.account_archive_dictionary[username] == password:
        print('Welcome: ' + username)
        acc = load_account_object(conn, username)
        return acc


# Query account information from accounts table based on username. Returns Account object based on query.
def load_account_object(conn, username):
    char_info_list = sql.execute_fetchone_sql(conn, sql.query_account_row(), username)
    char_info_dict = {'acc_id': char_info_list[0], 'username': char_info_list[1], 'password': char_info_list[2]}
    acc = Account(char_info_dict['acc_id'], char_info_dict['username'], char_info_dict['password'])
    return acc


# if __name__ == '__main__':
#     user_creates_account()
#     load_account_archive()
#     print(Account.login_dic)
