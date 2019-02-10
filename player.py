from search import search, convert_price_info, get_price_info


# Player Class. Holds player_id(Primary Key of characters table), character name, currency, and player inventories.
class Player:
    def __init__(self, player_id, name, currency, inventories):
        self.id = player_id
        self.currency = currency    # All currency held in cp. cp is then formatted via convert_currency() before view.
        self.name = name
        self.inventories = inventories  # List of player inventory names in string format.

    # Inventory management

    def add_item(self, inventory, some_item):
        item = search(some_item)  # Search returns ['Item', 'api url']
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
    # See convert_price_info in search.py for more information on conversion.
    def sell_item(self, item):
        value = convert_price_info(get_price_info(item))
        self.currency += value

    def buy_item(self, item):
        value = convert_price_info(get_price_info(item))
        if value > self.currency:
            print('not enough currency')    # TODO remove when GUI

        else:
            print('---item bought---')  # TODO Remove later
            self.currency -= value
