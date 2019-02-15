import api


# TODO Redesign all this shits

# Player Class. Holds player_id(Primary Key of characters table), character name, currency, and player inventories.
class Player:
    def __init__(self, player_id, name, currency, inventories):
        self.id = player_id
        self.currency = currency    # All currency held in cp. cp is then formatted via convert_currency() before view.
        self.name = name
        self.inventories = inventories  # List of player inventory names in string format.

    # Inventory management
    # TODO figure out wtf is going on. Redesign
    def add_item(self, inventory, some_item):
        equipment_dict = api.get_nested_api_dict(api.get_api_all(api.call_api(api.make_api_url('equipment'))),
                                                 'results')
        item = api.get_api_info(some_item, equipment_dict)  # Search returns ['Item', 'api url']
        self.inventories[inventory][item[0]] = item[1]  # Adds above to inventory dictionary as key:value pair

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
    def sell_item(self, item):
        list_of_dics = api.get_nested_api_dict(api.get_api_all(api.call_api(api.make_api_url('equipment'))), 'results')
        item_api_url = api.get_item_url(item, list_of_dics)
        item_info = api.get_api_all(api.call_api(item_api_url))
        item_cost = api.get_nested_api_dict(item_info, 'cost')
        value = api.convert_price_info(item_cost)
        self.currency += value

    def buy_item(self, item):
        list_of_dics = api.get_nested_api_dict(api.get_api_all(api.call_api(api.make_api_url('equipment'))), 'results')
        item_api_url = api.get_item_url(item, list_of_dics)
        item_info = api.get_api_all(api.call_api(item_api_url))
        item_cost = api.get_nested_api_dict(item_info, 'cost')
        value = api.convert_price_info(item_cost)
        if value > self.currency:
            print('not enough currency')    # TODO remove when GUI

        else:
            print('---item bought---')  # TODO Remove later
            self.currency -= value


if __name__ == '__main__':
    a = Player(1, 'kaz', 5, {})
    a.buy_item('Club')
    print(a.currency)
    a.sell_item('Dagger')
    print(a.currency)
    print(a.convert_currency())
