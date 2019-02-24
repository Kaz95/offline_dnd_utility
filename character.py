import api
import database
import sql
db = 'C:\\sqlite\\db\\test.db'
mem = ':memory:'
# TODO: Comment all of the things. Every block if it makes sense to do so.


# TODO: Consider refactor to player
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

    # Inventory management
    def add_item(self, conn, item, acc_id, inv_id):
        url = api.get_item_url(item, Character.list_of_item_dicts)

        item_info = {'acc_id': acc_id,
                     'char_id': self.id,
                     'inv_id': inv_id,
                     'item': item,
                     'api': url,
                     'quantity': 1}

        database.add_item_row(conn, sql.sql_add_item_row(), item_info)

    def add_currency(self, amount):
        self.currency += amount

    def subtract_currency(self, amount):
        self.currency -= amount

    def convert_currency(self):
        amount_in_cp = self.currency
        g = int(amount_in_cp / 100)
        s = int(round((((amount_in_cp / 100) - g) * 10), 2))
        c = int(round((((((amount_in_cp / 100) - g) * 10) - s) * 10), 2))
        converted_dict = {'gp': g, 'sp': s, 'cp': c}
        return converted_dict

    # Gets item price info and adds/subtracts it to/from currency based on [unit] key.
    # See convert_price_info() in api.py for more information on conversion.
    def buy_sell(self, item, action=None):
        url = api.get_item_url(item, Character.list_of_item_dicts)
        item_info = api.get_api_all(api.call_api(url))
        item_cost = api.get_nested_api_dict(item_info, 'cost')
        item_value = api.convert_price_info(item_cost)
        if action == 'buy':
            if item_value > self.currency:
                print('not enough currency')  # TODO remove later
            else:
                print('---item bought---')  # TODO remove later
                self.currency -= item_value
        elif action == 'sell':
            self.currency += item_value


# Query character row. Return player object.
def load_character_object(conn, char_name):
    with conn:
        char_info_list = sql.execute_fetchone_sql(conn, sql.sql_character_row(), char_name)
        char_info_dict = {'char_id': char_info_list[0], 'name': char_info_list[1], 'currency': char_info_list[2]}
        character = Character(char_info_dict['char_id'], char_info_dict['name'], char_info_dict['currency'], [])
        return character


if __name__ == '__main__':
    a = Character(1, 'kaz', 5000, [8])
    # print(a.display_currency())
