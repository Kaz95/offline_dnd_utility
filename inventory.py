# Inventory class. Used to keep track of current inventory selected.
# This allows items to capture the inventory_id value.


class Inventory:
    def __init__(self, inventory_id, name):
        self.id = inventory_id
        self.name = name
