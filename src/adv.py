from room import Room

from player import Player

from item import Item

from item import LightSource

# Declare all the rooms

room = {
    'outside':  Room("Outside Cave Entrance",
                     "North of you, the cave mount beckons", [], True),

    'foyer':    Room("Foyer", """Dim light filters in from the south. Dusty
passages run north and east.""", [LightSource("lamp", "An old lamp")]),

    'overlook': Room("Grand Overlook", """A steep cliff appears before you, falling
into the darkness. Ahead to the north, a light flickers in
the distance, but there is no way across the chasm.""", [Item("fork", "Used for stabbing ... or eating")]),

    'narrow':   Room("Narrow Passage", """The narrow passage bends here from west
to north. The smell of gold permeates the air.""", []),

    'treasure': Room("Treasure Chamber", """You've found the long-lost treasure
chamber! Sadly, it has already been completely emptied by
earlier adventurers. The only exit is to the south.""", []),
}


# Link rooms together

room['outside'].n_to = room['foyer']
room['foyer'].s_to = room['outside']
room['foyer'].n_to = room['overlook']
room['foyer'].e_to = room['narrow']
room['overlook'].s_to = room['foyer']
room['narrow'].w_to = room['foyer']
room['narrow'].n_to = room['treasure']
room['treasure'].s_to = room['narrow']

#
# Main
#

# Make a new player object that is currently in the 'outside' room.

# Write a loop that:
#
# * Prints the current room name
# * Prints the current description (the textwrap module might be useful here).
# * Waits for user input and decides what to do.
#
# If the user enters a cardinal direction, attempt to move to the room there.
# Print an error message if the movement isn't allowed.  
#
# If the user enters "q", quit the game.


def start_game():
    player = Player("Chad", room['outside'])

    playing = True

    print(f"You're name is {player.name}\n")

    # Handles Directional input
    def select_room(player_input):

        no_room_message = "\nYou couldn't find a room that direction!"

        room = player.current_room
        
        # North
        if player_input == "n":
            if not hasattr(room, "n_to"):
                print(no_room_message)
                ask_for_input()
            else:
                player.current_room = room.n_to

        # South
        elif player_input == "s":
            if not hasattr(room, "s_to"):
                print(no_room_message)
                ask_for_input()
            else:
                player.current_room = room.s_to

        # East
        elif player_input == "e":
            if not hasattr(room, "e_to"):
                print(no_room_message)
                ask_for_input()
            else:
                player.current_room = room.e_to

        # West
        elif player_input == "w":
            if not hasattr(room, "w_to"):
                print(no_room_message)
                ask_for_input()
            else:
                player.current_room = room.w_to


    # Handles Player Actions
    def player_action(player_input):

        if len(player_input.split()) == 1:

            # Inventory
            if player_input == "i":
                print("\nYour Items")
                for i in player.items:
                    print(f"  {i}")
                ask_for_input()

            # Controls
            elif player_input == "c":
                print(("\nControls: \n"
                    "  move [n, s, e, w]\n"
                    "  look [l]\n"
                    "  action [take item_name, get item_name, drop item_name]\n"
                    "  inventory [i]\n"
                    "  quit [q]\n"))
                ask_for_input()

            # Look Around
            elif player_input == "l":
                print_surroundings()
                ask_for_input()

            # Quit Game
            elif player_input == "q":
                print("\nGame exited!")
                nonlocal playing
                playing = False

            # Directional
            elif player_input in ("n", "s", "e", "w"):
                select_room(player_input)

            # Error for invalid input
            else:
                print("\nPlease enter a valid input!")
                ask_for_input()

        else:
            action, item_name = player_input.split()

            # Get or Take actions
            if action == "get" or action == "take":
                if check_for_light():
                    item = (
                        next((i for i in player.current_room.items if i.name == item_name), None)
                    )
                    if item:
                        player.items.append(item)
                        player.current_room.items.remove(item)
                        item.on_take()
                        ask_for_input()
                    else:
                        print("\nThere is no item with that name in room!")
                        ask_for_input()
                else:
                    print("\nGood luck finding that in the dark!")
                    ask_for_input()


            # Drop action
            elif action == "drop":
                item = next((i for i in player.items if i.name == item_name), None)
                if item:
                    player.items.remove(item)
                    player.current_room.items.append(item)
                    item.on_drop()
                    check_for_items()
                    ask_for_input()
                else:
                    print("\nThere is no item with that name in your inventory!")
                    ask_for_input()

             # Error for invalid input
            else:
                print("\nPlease enter a valid input!")
                ask_for_input()


    # Starts player input
    def ask_for_input():
        player_input = input(("\n------\nWhat would you like to do?  " 
            "  (type c for help)\n------\n"))

        player_action(player_input)


    # Prints room items
    def check_for_items():
        if len(player.current_room.items) > 0:
            print("\nIn the room you see\n")
            player.current_room.print_items()


    # Check room and player for lightsource
    def check_for_light():
        if player.current_room.is_light:
            return True

        for i in player.current_room.items:
            if isinstance(i, LightSource):
                return True

        for i in player.items:
            if isinstance(i, LightSource):
                return True

        return False


    # Print room name and description
    def print_surroundings():
        print(f"\nYou are in the {player.current_room.name}\n")
        if check_for_light():
            print(player.current_room.description)
            check_for_items()
        else:
            print("It's pitch black!")


    # Start gameplay loop 
    while playing:
        print_surroundings()
        
        ask_for_input()

        print("\n -------------------------------------- \n")

start_game()
