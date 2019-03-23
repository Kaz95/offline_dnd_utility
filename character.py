import api
import database
import sql
import error_box

db = 'C:\\sqlite\\db\\test.db'
mem = ':memory:'


# Player Class. Holds player_id(Primary Key of characters table), character name, currency, and player inventories.
class Character:

    # TODO: unit_integration_test: FIXTURE REQUIRED
    # Main equipment dictionary returned from DnD 5e API
    # [{'name': 'some name', 'url': 'some url'}, {'name': 'some name', 'url': 'some url'}]
    list_of_item_dicts = api.get_nested_api_dict(api.get_api_all(api.call_api(api.construct_api_url('equipment'))), 'results')

    def __init__(self, char_id, name, currency, inventories_list):
        self.id = char_id
        self.currency = currency    # All currency held in cp. cp is then formatted via convert_currency() before view.
        self.name = name
        self.inventories = inventories_list  # List of player inventory names in string format. Not currently used.

    # TODO: Not tested
    # TODO: This makes more sense as an inventory method. Change it once multiple inventories.
    # Adds an item under character id. Can specify a specific inventory via inv_id
    def add_item_db(self, conn, item, acc_id, inv_id):
        url = sql.execute_fetchone_sql(conn, sql.query_store_item_url(), item)
        # url = api.get_item_url(item, Character.list_of_item_dicts)
        item_value = sql.execute_fetchone_sql(conn, sql.query_store_item_value(), item)

        item_info = {'acc_id': acc_id,
                     'char_id': self.id,
                     'inv_id': inv_id,
                     'item': item,
                     'api': url[0],
                     'value': item_value[0],
                     'quantity': 1}

        database.add_item_row(conn, sql.add_item_row(), item_info)

    # TODO: Test
    # Updates currency column in DB based on character ID and currency.
    def update_currency_db(self, conn):
        sql.execute_sql(conn, sql.update_currency(), self.currency, self.id)

    # TODO: action= and conn= aren't exactly optional and should not be treated as such.
    # Gets item price info and adds/subtracts it to/from currency based on [unit] key.
    # See convert_price_info() in api.py for more information on conversion.
    # Also updates currency in DB via self.update_currency_db
    # Returns True if item is affordable. Else returns False.
    def buy_sell(self, item, action=None, conn=None):
        url = api.get_item_url(item, Character.list_of_item_dicts)
        item_info = api.get_api_all(api.call_api(url))
        item_cost = api.get_nested_api_dict(item_info, 'cost')
        item_value = api.convert_price_info(item_cost)
        if action == 'buy':
            if item_value > self.currency:
                return False
            else:
                print('---item bought---')  # TODO remove later
                self.currency -= item_value
                self.update_currency_db(conn)
                return True
        elif action == 'sell':
            print('---item sold---')  # TODO remove later
            self.currency += item_value
            self.update_currency_db(conn)


# TODO: Test
# TODO: I think 'if in' works on nested structures.
# Query all character names. Return True if name in query. Else return False.
def character_name_taken(conn, name):
    character_names_tups = sql.execute_fetchall_sql(conn, sql.query_all_character_names())
    for tup in character_names_tups:
        if name in tup:
            return True
    return False


# TODO: unit test with mock assert called with.
# Adds character to DB based on current character information.
# If character name taken, display error box.
def character_creation(conn, acc_id, name, currency):
    if character_name_taken(conn, name):
        error_box.character_name_taken()
        return False
    else:
        character_info_dict = {'acc_id': acc_id, 'name': name, 'currency': currency}
        database.add_character_row(conn, sql.add_character_row(), character_info_dict)
        return True


# TODO: Test
# Query character row. Returns character object.
def load_character_object(conn, char_name):
    char_info_list = sql.execute_fetchone_sql(conn, sql.query_character_row(), char_name)
    char_info_dict = {'char_id': char_info_list[0], 'name': char_info_list[1], 'currency': char_info_list[2]}
    character = Character(char_info_dict['char_id'], char_info_dict['name'], char_info_dict['currency'], [])
    return character


# if __name__ == '__main__':
#     a = Character(1, 'kaz', 5000, [8])
    # print(a.display_currency())
