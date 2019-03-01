import database
import sql
import error_box

db = 'C:\\sqlite\\db\\test.db'
mem = ':memory:'


# Account class. Stores account_id(primary key of account table), username, and password.
class Account:
    # Used to hold account info in {'username':'password'} format. Populated by load_account_archive()
    # log_in() then compares against it.
    login_dic = {}

    def __init__(self, acc_id, username, password):
        self.id = acc_id
        self.username = username
        self.password = password


def username_taken(username):
    for key in Account.login_dic.keys():
        if key == username:
            return True
        else:
            return False


def account_has_characters(conn, acc_id):
    account_id_tups_list = sql.execute_fetchall_sql(conn, sql.sql_accounts_with_characters())
    for tup in account_id_tups_list:
        if acc_id in tup:
            return True
        else:
            return False


# Creates new account. Adds information to accounts table in database.
def user_creates_account(conn, username, password):
    load_account_archive(conn)
    if username_taken(username):
        error_box.username_taken()
        return False
    else:
        with conn:
            acc_info = {'username': username, 'password': password}
            database.add_account_row(conn, sql.sql_add_account_row(), acc_info)
            return True


# Loads all account username/password information and stores as key:value pairs in Account.log_in_dict.
def load_account_archive(conn):
    Account.login_dic = {}
    with conn:
        list_of_username_password_tups = sql.execute_fetchall_sql(conn, sql.sql_username_password())
        for tup in list_of_username_password_tups:
            Account.login_dic[tup[0]] = tup[1]


# Returns username if authenticated.
def log_in(conn, username, password):
    load_account_archive(conn)  # Loads account info for authentication into Account.login_dic

    if username not in Account.login_dic:
        error_box.wrong_username()
        return None
    elif username in Account.login_dic and Account.login_dic[username] != password:
        error_box.wrong_password()
        return None
    elif username in Account.login_dic and Account.login_dic[username] == password:
        print('Welcome: ' + username)
        acc = load_account_object(conn, username)
        return acc


# query ALL account information from accounts table based on username. Returns Account object based on query.
def load_account_object(conn, username):
    with conn:
        char_info_list = sql.execute_fetchone_sql(conn, sql.sql_account_row(), username)
        char_info_dict = {'acc_id': char_info_list[0], 'username': char_info_list[1], 'password': char_info_list[2]}
        acc = Account(char_info_dict['acc_id'], char_info_dict['username'], char_info_dict['password'])
        return acc


if __name__ == '__main__':
    user_creates_account()
    load_account_archive()
    print(Account.login_dic)
