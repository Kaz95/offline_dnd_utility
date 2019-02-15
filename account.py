import database
import sql
db = 'C:\\sqlite\\db\\test.db'
mem = ':memory:'


# Account class. Stores account_id(primary key of account table), username, and password.
class Account:
    # Used to hold account info in {'username':'password'} format. Populated by load_account_archive()
    # log_in() then compares against it.
    log_in_dic = {}

    # TODO refactor self.name to self.username
    def __init__(self, acc_id, name, password):
        self.id = acc_id
        self.name = name
        self.password = password


# TODO refactor for GUI
# Creates new admin account. Adds information to accounts table in database.
def user_creates_account():
    print('create name')
    username = input()
    print('create password')
    password = input()
    connection = database.create_connection(db)
    with connection:
        account_info = (username, password)
        database.add_account_row(connection, account_info)


# TODO integration test
# Loads all account username/password information and stores as key:value pairs in Account.log_in_dict.
def load_account_archive():
    conn = database.create_connection(db)
    with conn:
        a = database.query_fetchall(conn, sql.sql_username_password())
        for i in a:
            Account.log_in_dic[i[0]] = i[1]


# TODO refactor for GUI
# Requests username/password from user. Returns username if authenticated
def log_in():
    load_account_archive()  # Loads account info for authentication.
    print('enter username')
    username = input()
    print('enter password')
    password = input()
    if username in Account.log_in_dic and Account.log_in_dic[username] == password:
        print('Welcome: ' + username)
        return username
    else:
        log_in()


# TODO integration test
# query ALL account information from accounts table based on username. Returns Account object based on query.
def load_account_object(username):
    conn = database.create_connection(db)
    with conn:
        p1_info = database.query_fetchone_list(conn, sql.sql_account_row(), username)
        acc = Account(p1_info[0], p1_info[1], p1_info[2])
        return acc


if __name__ == '__main__':
    user_creates_account()
    load_account_archive()
    print(Account.log_in_dic)
