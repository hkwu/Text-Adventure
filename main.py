#! python3

# Text adventure in Python
# produced by Kelvin Wu
# initial commit 2015-06-01
# guidelines from Al Sweigart's guide to text games in Python

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
                 south, east, west):
        self.name = name
        self.desc = desc
        self.north = north
        self.south = south
        self.east = east
        self.west = west

    def location(self):
        """
        print location information
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


class ItemTile(TravelTile):
    def __init__(self, name, desc, north, 
                 south, east, west, ground):
        TravelTile.__init__(name, desc, north, south,
                            east, west)
        self.ground = ground

    def pickup(self, item):
        pass


class NPCTile(ItemTile):
    def __init__(self, name, desc, north, 
                 south, east, west, ground,
                 npc):
        BaseTile.__init__(name, desc, north, south, 
                          east, west, ground)
        self.npc = npc

    def talk(self, npc):
        pass

# world tiles
path0 = BaseTile("Forest Path",
                 "A trodden dirt path in the forest",
                 None, None, None, None, [])
spawn = BaseTile("Forest Clearing",
                 ("A nondescript clearing. "
                  "There are trees all over. "
                  "The only way to go is north."),
                 path0, None, None, None,
                 ["test", "test"])


# entity classes

# base entity with name and location info
class Entity(object):
    def __init__(self, name, loc):
        self.name = name
        self.loc = loc


# player entity with additional traits
class Player(Entity):
    def __init__(self, name, loc, coin):
        Entity.__init__(self, name, loc)
        self.hp = 100
        self.coin = coin
        self.inv = []
        self.win = False

    def get_inv(self):
        """
        print player's inventory
        """
        print("Inventory:")

        for item in self.inv:
            print(item)

    def move(self, direction):
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
    def __init__(self, name, loc, coin, inv):
        Entity.__init__(self, name, loc)
        self.coin = coin
        self.inv = inv

    def purchase(self, item, price):
        pass

# entity instances
player = Player("Test", spawn, 0)
player.loc.location()
player.move(NORTH)
