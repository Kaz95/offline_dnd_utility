import api
import database
import sql
import error_box

db = 'C:\\sqlite\\db\\test.db'
mem = ':memory:'


# Player Class. Holds player_id(Primary Key of characters table), character name, currency, and player inventories.
class Character:

    # TODO: unit_integration_test: FIXTURE REQUIRED
    # [{'name': 'some name', 'url': 'some url'}, {'name': 'some name', 'url': 'some url'}]
    list_of_item_dicts = api.get_nested_api_dict(api.get_api_all(api.call_api(api.make_api_url('equipment'))), 'results')

    def __init__(self, char_id, name, currency, inventories_list):
        self.id = char_id
        self.currency = currency    # All currency held in cp. cp is then formatted via convert_currency() before view.
        self.name = name
        self.inventories = inventories_list  # List of player inventory names in string format. Technically not used.

    # TODO: This makes more sense as an inventory method. Change it once multiple inventories.
    # TODO: Refactor: Name
    # Adds an item item under character id. Can specify a specific inventory via inv_id
    def add_item(self, conn, item, acc_id, inv_id):
        url = sql.execute_fetchone_sql(conn, sql.sql_store_item_url(), item)
        # url = api.get_item_url(item, Character.list_of_item_dicts)
        item_value = sql.execute_fetchone_sql(conn, sql.sql_store_item_value(), item)

        item_info = {'acc_id': acc_id,
                     'char_id': self.id,
                     'inv_id': inv_id,
                     'item': item,
                     'api': url[0],
                     'value': item_value[0],
                     'quantity': 1}

        database.add_item_row(conn, sql.sql_add_item_row(), item_info)

    # TODO: Test
    # TODO: Refactor: Name
    # Updates currency column in DB based on character ID and currency.
    def update_currency(self, conn):
        sql.execute_sql(conn, sql.update_currency(), self.currency, self.id)

    # Converts character.currency value (in cp) into gp,sp,cp
    def convert_currency(self):
        amount_in_cp = self.currency
        g = int(amount_in_cp / 100)
        s = int(round((((amount_in_cp / 100) - g) * 10), 2))
        c = int(round((((((amount_in_cp / 100) - g) * 10) - s) * 10), 2))
        converted_dict = {'gp': g, 'sp': s, 'cp': c}
        return converted_dict

    # Gets item price info and adds/subtracts it to/from currency based on [unit] key.
    # See convert_price_info() in api.py for more information on conversion.
    # Also updates currency in DB via self.update_currency
    # Returns True if item is affordable. Else returns False.
    def buy_sell(self, item, action=None, conn=None):
        url = api.get_item_url(item, Character.list_of_item_dicts)
        item_info = api.get_api_all(api.call_api(url))
        item_cost = api.get_nested_api_dict(item_info, 'cost')
        item_value = api.convert_price_info(item_cost)
        if action == 'buy':
            if item_value > self.currency:
                print('not enough currency')  # TODO remove later
                return False
            else:
                print('---item bought---')  # TODO remove later
                self.currency -= item_value
                self.update_currency(conn)
                return True
        elif action == 'sell':
            print('---item sold---')  # TODO remove later
            self.currency += item_value
            self.update_currency(conn)


# TODO: Test
# Query all character names. Return True if name in query. Else return False.
def character_name_taken(conn, name):
    character_names_tups = sql.execute_fetchall_sql(conn, sql.sql_all_character_names())
    for tup in character_names_tups:
        if name in tup:
            return True
    return False


# TODO: unit test with mock assert called with.
# Adds character to DB based on current character information.
def character_creation(conn, acc_id, name, currency):
    if character_name_taken(conn, name):
        error_box.character_name_taken()
        return False
    else:
        character_info_dict = {'acc_id': acc_id, 'name': name, 'currency': currency}
        database.add_character_row(conn, sql.sql_add_character_row(), character_info_dict)
        return True


# TODO: Test
# Query character row. Return player object.
def load_character_object(conn, char_name):
    with conn:
        char_info_list = sql.execute_fetchone_sql(conn, sql.sql_character_row(), char_name)
        char_info_dict = {'char_id': char_info_list[0], 'name': char_info_list[1], 'currency': char_info_list[2]}
        character = Character(char_info_dict['char_id'], char_info_dict['name'], char_info_dict['currency'], [])
        return character


# if __name__ == '__main__':
#     a = Character(1, 'kaz', 5000, [8])
    # print(a.display_currency())
