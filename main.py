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
#MERCHANT = 'merchant'
#MOB = 'mob'

# for items
#REFNAME = 'refname'
LONGDESC = 'longdesc'
SHORTDESC = 'shortdesc'
PICKABLE = 'pickable'
#EDIBLE = 'edible'

# screen dimension
SCREEN_WIDTH = 80

# world data
wTiles = {
    'spawn': {
        TILENAME: "Forest Clearing",
        DESC: ("A nondescript clearing. "
               "There are trees all over. "
               "The only way to go is north."),
        NORTH: "path0",
        SOUTH: None,
        EAST: None,
        WEST: None,
        GROUND: ['test', 'test', 'test']
    },
    'path0': {
    	TILENAME: "Forest Path",
    	DESC: "A trodden dirt path in the forest.",
    	NORTH: "path1",
    	SOUTH: None,
    	EAST: None,
    	WEST: None,
    	WEST: None,
    	GROUND: []
    }
}

wItems = {
	'Iron Sword': {
		DESC: "An iron sword. Built to last.",
		PICKABLE: True
	}
}

# possible replacement for dictionary tiles
class BaseTile(object):
	def __init__(self, name, desc, north, south, east, west, ground):
		self.name = name
		self.desc = desc
		self.north = north
		self.south = south
		self.east = east
		self.west = west
		self.ground = ground

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
class Entity(object):
	def __init__(self, name, loc):
		self.name = name
		self.loc = loc


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
		if direction == NORTH and self.loc.north:
			self.loc = self.loc.north
			self.loc.location()
		elif direction == SOUTH and self.loc.south:
			self.loc = self.loc.south
			self.loc.location()
		elif direction == EAST and self.loc.east:
			self.loc = self.loc.east
			self.loc.location()
		elif direction == WEST and self.loc.west:
			self.loc = self.loc.west
			self.loc.location()
		else:
			print("There is nothing over there!")


class NPC(Entity):
	def __init__(self, name, coin, inv):
		Entity.__init__(self, name)
		self.coin = coin
		self.inv = inv

	def purchase(self, item, price):
		pass


# helper functions
def location(tile):
    """
    prints out tile information
    """
    border_len = len(wTiles[tile][TILENAME])

    print(":" * border_len)
    print(wTiles[tile][TILENAME])
    print(":" * border_len + "\n")

    print("\n".join(textwrap.wrap(wTiles[tile][DESC], SCREEN_WIDTH)))
    print("")

    if wTiles[tile][GROUND]:
    	# two formats: straight list or line by line

        # items = ", ".join(wTiles[tile][GROUND])
        # items = "Items on the ground: " + items

        # print("\n".join(textwrap.wrap(items, SCREEN_WIDTH)))

        print("Items on the ground:")

        for item in wTiles[tile][GROUND]:
        	print(item)
    else:
        print("There are no items on the ground.")

    print("")

    if wTiles[tile][NORTH]:
        tile_key = wTiles[tile][NORTH]
        
        print("NORTH: " + wTiles[tile_key][TILENAME])
    if wTiles[tile][SOUTH]:
        tile_key = wTiles[tile][SOUTH]
        
        print("SOUTH: " + wTiles[tile_key][TILENAME])
    if wTiles[tile][EAST]:
        tile_key = wTiles[tile][EAST]
        
        print("EAST: " + wTiles[tile_key][TILENAME])
    if wTiles[tile][WEST]:
        tile_key = wTiles[tile][WEST]
        
        print("WEST: " + wTiles[tile_key][TILENAME])

# initialize
#if __name__ == "__main__":
print("What's your name?")
p_name = raw_input("> ")
player = Player(p_name, spawn, 0)
player.loc.location()
player.move(NORTH)
