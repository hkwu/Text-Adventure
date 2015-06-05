#! python3

# Text adventure in Python (name pending)
# by Kelvin Wu
# initial commit 2015-06-01

# kudos to Al Sweigart and Phillip Johnson for their Python
# text game guides

# required libraries
import cmd
import os
import string
import textwrap

# some constant variables (keeping them as legacy code for now)

# # for tiles
# TILENAME = 'tilename'
# DESC = 'desc'
# NORTH = 'north'
# SOUTH = 'south'
# EAST = 'east'
# WEST = 'west'
# GROUND = 'GROUND'
# MERCHANT = 'merchant'
# MOB = 'mob'

# # for items
# REFNAME = 'refname'
# LONGDESC = 'longdesc'
# SHORTDESC = 'shortdesc'
# PICKABLE = 'pickable'
# # EDIBLE = 'edible'

# screen dimension
SCREEN_WIDTH = 80


# tile classes
class TravelTile(object):
    def __init__(self, name, desc, north,
                 south, east, west, ground):
        self.name = name
        self.desc = desc
        self.north = north
        self.south = south
        self.east = east
        self.west = west
        self.ground = ground

    def location(self):
        """
        prints location information
        """
        cls()
        border_len = len(self.name)

        print(":" * border_len)
        print(self.name)
        print(":" * border_len + "\n")

        print("\n".join(textwrap.wrap(self.desc, SCREEN_WIDTH)))
        print("")

        if self.ground:
            print("Items on the ground:")

            for item in self.ground:
                print(item)
        else:
            print("There are no items on the ground.")

        print("")

        if self.north:
            print("NORTH: %s" % wTiles[self.north].name)
        if self.south:
            print("SOUTH: %s" % wTiles[self.south].name)
        if self.east:
            print("EAST: %s" % wTiles[self.east].name)
        if self.west:
            print("WEST: %s" % wTiles[self.west].name)


class NPCTile(TravelTile):
    def __init__(self, name, desc, north,
                 south, east, west, ground,
                 npc):
        TravelTile.__init__(name, desc, north, south,
                          east, west, ground)
        self.npc = npc

    def talk(self, npc):
        pass


# entity classes

# base entity
class Entity(object):
    def __init__(self, name, loc, inv,
                 coin, weapon, armour):
        self.name = name
        self.loc = loc
        self.inv = inv
        self.coin = coin
        self.weapon = weapon
        self.armour = armour

    def examine(self):
        """
        prints out details of the entity
        """
        pass


# player entity with additional traits
class Player(Entity):
    def __init__(self, name):
        Entity.__init__(self, name, wTiles['spawn'], [],
                        50, None, None)
        self.hp = 100
        self.win = False

    def get_inv(self):
        """
        print player's inventory
        """
        cls()

        print("Inventory:")

        for item in self.inv:
            print(item)

    def move(self, direction):
        """
        moves player in direction
        """
        if direction == "north" and self.loc.north:
            self.loc = wTiles[self.loc.north]
            self.loc.location()
        elif direction == "south" and self.loc.south:
            self.loc = wTiles[self.loc.south]
            self.loc.location()
        elif direction == "east" and self.loc.east:
            self.loc = wTiles[self.loc.east]
            self.loc.location()
        elif direction == "west" and self.loc.west:
            self.loc = wTiles[self.loc.west]
            self.loc.location()
        else:
            print("There is nothing over there!")

    def take(self, item):
        """
        moves pickable item to player's inventory
        """
        case_proper = string.capwords(item)
        cls()

        if not item:
            print("What are you trying to take?")
        elif case_proper in self.loc.ground:
            self.loc.ground.remove(case_proper)
            self.inv.append(case_proper)
            print("You take the %s." % case_proper)
        else:
            print("That's not even on the ground.")

    def drop(self, item):
        """
        moves item to the ground
        """
        case_proper = string.capwords(item)
        cls()

        if not item:
            print("What are you trying to drop?")
        elif case_proper in self.inv:
            self.inv.remove(case_proper)
            self.loc.ground.append(case_proper)
            print("You throw the %s on the ground." % case_proper)
        else:
            print("You don't even have one of those.")


# NPC entities
class NPC(Entity):
    def __init__(self, name, desc, loc,
                 inv, coin, weapon, armour,
                 lines):
        Entity.__init__(self, name, loc, inv,
                        coin, weapon, armour)
        self.desc = desc
        self.lines = lines

    def purchase(self, item):
        pass


# item classes

# base item
class Item(object):
    def __init__(self, name, desc, price):
        self.name = name
        self.desc = desc
        self.price = price


# weapons
class Weapon(Item):
    def __init__(self, name, desc, price,
                 damage):
        Item.__init__(name, desc, price)
        self.damage = damage


# armour
class Armour(Item):
    def __init__(self, name, desc, price,
                 defence):
        Item.__init__(name, desc, price)
        self.defence = defence


# tile instances (legacy code)
# path0 = TravelTile("Forest Path",
#                    "A trodden dirt path in the forest",
#                    None, None, None, None, [])
# spawn = TravelTile("Forest Clearing",
#                    ("A nondescript clearing. "
#                     "There are trees all over. "
#                     "The only way to go is north."),
#                    path0, None, None, None,
#                    ["test", "test"])

# using dictionary to contain the tiles
wTiles = {
    'spawn': TravelTile("Forest Clearing",
                        ("A nondescript clearing. "
                         "There are trees all over. "
                         "The only way to go is north."),
                        'path0', None, None, None,
                        ["Crumpled Note", "Sword"]),
    'path0': TravelTile("Forest Path",
                        "A trodden dirt path in the forest",
                        None, 'spawn', None, None, [])
}

# entity instances
player = Player("Test")


# cmd interface class
class InputCmd(cmd.Cmd):
    prompt = "\n> "

    # interface functions
    def do_quit(self, arg):
        """Quit the game."""
        cls()

        return True

    def do_location(self, arg):
        """Where am I?"""
        player.loc.location()

    def do_inventory(self, arg):
        """Lists the items in your inventory."""
        player.get_inv()

    # movement functions
    def do_north(self, arg):
        """Go north."""
        player.move("north")

    def do_south(self, arg):
        """Go south."""
        player.move("south")

    def do_east(self, arg):
        """Go east."""
        player.move("east")

    def do_west(self, arg):
        """Go west."""
        player.move("west")

    # interaction functions
    def do_take(self, arg):
        """Pick up an item."""
        player.take(arg)

    def do_drop(self, arg):
        """Drop an item."""
        player.drop(arg)

    # help topics
    def help_movement(self):
        cls()
        print("Type NORTH [N], SOUTH [S], "
              "EAST [E] or WEST [W] to travel.")

    # invalid command message
    def default(self, arg):
        cls()
        print("That is not a valid command. Please try again "
              "(try HELP for a list of commands).")

    # aliases
    do_q = do_Q = do_QUIT = do_quit
    do_l = do_L = do_LOCATION = do_location
    do_i = do_I = do_INVENTORY = do_inventory

    do_n = do_N = do_NORTH = do_north
    do_s = do_S = do_SOUTH = do_south 
    do_e = do_E = do_EAST = do_east 
    do_w = do_W = do_WEST = do_west

    do_t = do_T = do_TAKE = do_take
    do_d = do_D = do_DROP = do_drop

    do_h = do_H = do_HELP = do_help


# utility functions
def cls():
    """Clears the screen."""
    os.system("cls" if os.name == "nt" else "clear")

# input loop
if __name__ == '__main__':
    cls()
    print("Python Text Adventure\n"
          "====================\n\n"
          "Press any key to begin.\n")
    input("> ")
    cls()

    player = Player("Test")
    player.loc.location()
    InputCmd().cmdloop()

    print("Game Over!")
