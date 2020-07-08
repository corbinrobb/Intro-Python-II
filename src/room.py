# Implement a class to hold room information. This should have name and
# description attributes.

class Room:
    def __init__(self, name, description, items, is_light=False):
        self.name = name
        self.description = description
        self.items = items
        self.is_light = is_light

    def print_items(self):
        for i in self.items:
            print(f"- {i.name}")
