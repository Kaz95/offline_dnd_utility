from database import create_connection
from database import add_account_row
# def create_connection(db_file):
#     try:
#         conn = sqlite3.connect(db_file)
#         return conn
#     except Error as e:
#         print(e)
#
#     return None




# Database setup
def bobs():
    connection = create_connection()
    with connection:
        account1 = ('bob1', 'tree53', True)
        add_account_row(connection, account1)
        account2 = ('bob2', 'tree53', True)
        account3 = ('bob3', 'tree53', False)
        add_account_row(connection, account2)
        add_account_row(connection, account3)
        account4 = ('bob4', 'tree53', True)
        add_account_row(connection, account4)
        account5 = ('bob5', 'tree53', False)
        add_account_row(connection, account5)


if __name__ == '__main__':
    bobs()

# Load DM on log in. Create store. Add item. Print Store
# if __name__ == '__main__':
#     dm = load_player(log_in())
#     dm.create_store()
#     dm.add_item('general', 'Club')
#     pprint.pprint(dm.stores)
