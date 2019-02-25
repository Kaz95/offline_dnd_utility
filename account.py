import database
import sql
db = 'C:\\sqlite\\db\\test.db'
mem = ':memory:'
# TODO: Comment all of the things. Every block if it makes sense to do so.


# Account class. Stores account_id(primary key of account table), username, and password.
class Account:
    # Used to hold account info in {'username':'password'} format. Populated by load_account_archive()
    # log_in() then compares against it.
    login_dic = {}

    def __init__(self, acc_id, username, password):
        self.id = acc_id
        self.username = username
        self.password = password


# Creates new account. Adds information to accounts table in database.
def user_creates_account(conn, username, password):
    with conn:
        acc_info = {'username': username, 'password': password}
        database.add_account_row(conn, sql.sql_add_account_row(), acc_info)


# Loads all account username/password information and stores as key:value pairs in Account.log_in_dict.
def load_account_archive(conn):
    with conn:
        list_of_username_password_tups = sql.execute_fetchall_sql(conn, sql.sql_username_password())
        for tup in list_of_username_password_tups:
            Account.login_dic[tup[0]] = tup[1]


# Returns username if authenticated.
def log_in(conn, username, password):
    load_account_archive(conn)  # Loads account info for authentication into Account.login_dic
    if username in Account.login_dic and Account.login_dic[username] == password:
        print('Welcome: ' + username)
        return username


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
