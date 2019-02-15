# Inventory class. Used to keep track of current inventory selected.
# This allows items to capture the inventory_id value.
import database
import api


class Inventory:
    def __init__(self, inventory_id, name):
        self.id = inventory_id
        self.name = name

    def add_item(self, item, id, conn):
        list_of_dics = api.get_nested_api_dict(api.get_api_all(api.call_api(api.make_api_url('equipment'))), 'results')
        url = api.get_item_url(item, list_of_dics)
        item_info = (id, item, url, 1)
        database.add_item_row(conn, item_info)
