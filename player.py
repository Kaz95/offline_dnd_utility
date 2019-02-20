import api
import database
import sql
db = 'C:\\sqlite\\db\\test.db'
mem = ':memory:'


# Player Class. Holds player_id(Primary Key of characters table), character name, currency, and player inventories.
class Player:

    # TODO: unit_integration_test: FIXTURE REQUIRED
    # [{'name': 'some name', 'url': 'some url'}, {'name': 'some name', 'url': 'some url'}]
    list_of_dics = api.get_nested_api_dict(api.get_api_all(api.call_api(api.make_api_url('equipment'))), 'results')

    def __init__(self, player_id, name, currency, inventories):
        self.id = player_id
        self.currency = currency    # All currency held in cp. cp is then formatted via convert_currency() before view.
        self.name = name
        self.inventories = inventories  # List of player inventory names in string format.

    # Inventory management
    def add_item(self, conn, item, account_id, cur_inventory_id):
        url = api.get_item_url(item, Player.list_of_dics)
        item_info = {'acc_id': account_id, 'char_id': self.id, 'inv_id': cur_inventory_id, 'item': item, 'api': url,
                     'quant': 1}
        database.add_item_row(conn, sql.sql_add_item_row(), item_info)

    def add_currency(self, amount):
        self.currency += amount

    def subtract_currency(self, amount):
        self.currency -= amount

    # TODO refactor for GUI
    def convert_currency(self):
        amount_in_cp = self.currency
        g = int(amount_in_cp / 100)
        s = int(round((((amount_in_cp / 100) - g) * 10), 2))
        c = int(round((((((amount_in_cp / 100) - g) * 10) - s) * 10), 2))
        converted_dict = {'gp': g, 'sp': s, 'cp': c}
        return converted_dict

    # Gets item price info and adds/subtracts it to/from currency dictionary based on [unit] key.
    # See convert_price_info in api.py for more information on conversion.
    def buy_sell(self, item, action=None):
        url = api.get_item_url(item, Player.list_of_dics)
        item_info = api.get_api_all(api.call_api(url))
        item_cost = api.get_nested_api_dict(item_info, 'cost')
        value = api.convert_price_info(item_cost)
        if action == 'buy':
            if value > self.currency:
                print('not enough currency')  # TODO remove when GUI
            else:
                print('---item bought---')  # TODO remove when GUI
                self.currency -= value
        elif action == 'sell':
            self.currency += value


if __name__ == '__main__':
    a = Player(1, 'kaz', 5000, [8])
    a.buy_sell('Dagger', 'buy')
    print(a.currency)
    a.buy_sell('Dagger', 'sell')
    print(a.currency)
    print(a.convert_currency())
