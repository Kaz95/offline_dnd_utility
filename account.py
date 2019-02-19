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


# Creates new admin account. Adds information to accounts table in database.
def user_creates_account(conn, username, password):
    # connection = database.create_connection(db)
    with conn:
        account_info = {'user': username, 'pass': password}
        database.add_account_row(conn, sql.sql_add_account_row(), account_info)


# Loads all account username/password information and stores as key:value pairs in Account.log_in_dict.
def load_account_archive(conn):
    # conn = database.create_connection(db)
    with conn:
        a = sql.execute_fetchall_sql(conn, sql.sql_username_password())
        for i in a:
            Account.log_in_dic[i[0]] = i[1]


# TODO: unit_integration_test
# Requests username/password from user. Returns username if authenticated
def log_in(conn, username, password):
    load_account_archive(conn)  # Loads account info for authentication.
    if username in Account.log_in_dic and Account.log_in_dic[username] == password:
        print('Welcome: ' + username)
        return username
    else:
        log_in(conn, username, password)


# TODO: unit_integration_test
# query ALL account information from accounts table based on username. Returns Account object based on query.
def load_account_object(conn, username):
    # conn = database.create_connection(db)
    with conn:
        p1_info = list(sql.execute_fetchone_sql(conn, sql.sql_account_row(), username))
        acc = Account(p1_info[0], p1_info[1], p1_info[2])
        return acc


if __name__ == '__main__':
    user_creates_account()
    load_account_archive()
    print(Account.log_in_dic)
