#! python3

# Text adventure in Python (name pending)
# by Kelvin Wu
# initial commit 2015-06-01

# kudos to Al Sweigart and Phillip Johnson for their Python
# text game guides

# required libraries
import cmd
import sys
import textwrap

# some constant variables

# for tiles
TILENAME = 'tilename'
DESC = 'desc'
NORTH = 'north'
SOUTH = 'south'
EAST = 'east'
WEST = 'west'
GROUND = 'GROUND'
# MERCHANT = 'merchant'
# MOB = 'mob'

# for items
# REFNAME = 'refname'
LONGDESC = 'longdesc'
SHORTDESC = 'shortdesc'
PICKABLE = 'pickable'
# EDIBLE = 'edible'

# screen dimension
SCREEN_WIDTH = 80


# possible replacement for dictionary tiles
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
            print("NORTH: %s" % self.north.name)
        if self.south:
            print("SOUTH: %s" % self.south.name)
        if self.east:
            print("EAST: %s" % self.east.name)
        if self.west:
            print("WEST: %s" % self.west.name)

    def pickup(self, item):
        """
        moves pickable item to player's inventory
        """
        player.inv.append(item)
        self.ground.remove(item)


class NPCTile(TravelTile):
    def __init__(self, name, desc, north, 
                 south, east, west, ground,
                 npc):
        BaseTile.__init__(name, desc, north, south, 
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
        Entity.__init__(self, name, spawn, [],
                        50, None, None)
        self.hp = 100
        self.win = False

    def get_inv(self):
        """
        print player's inventory
        """
        print("Inventory:")

        for item in self.inv:
            print(item)

    def move(self, direction):
        """
        moves player in direction
        """
        if direction.lower() == NORTH and self.loc.north:
            self.loc = self.loc.north
            self.loc.location()
        elif direction.lower() == SOUTH and self.loc.south:
            self.loc = self.loc.south
            self.loc.location()
        elif direction.lower() == EAST and self.loc.east:
            self.loc = self.loc.east
            self.loc.location()
        elif direction.lower() == WEST and self.loc.west:
            self.loc = self.loc.west
            self.loc.location()
        else:
            print("There is nothing over there!")


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


# tile instances
path0 = TravelTile("Forest Path",
                 "A trodden dirt path in the forest",
                 None, None, None, None, [])
spawn = TravelTile("Forest Clearing",
                 ("A nondescript clearing. "
                  "There are trees all over. "
                  "The only way to go is north."),
                 path0, None, None, None,
                 ["test", "test"])

# entity instances
player = Player("Test")


# cmd interface class
class InputCmd(cmd.Cmd):
    prompt = "\n>"

    def do_quit(self, arg):
        return True

    def help_quit(self):
        print("Quit the game.")

    def help_movement(self):
        print("Type the direction in which you want to move.")

    def default(self, arg):
        print("That is not a valid command. Please try again "
              "(try HELP for a list of commands).")

# input loop
if __name__ == '__main__':
    player = Player("Test")
    player.loc.location()
    InputCmd().cmdloop()
    print("Game Over!")
