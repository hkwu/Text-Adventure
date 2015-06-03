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
PRINTNAME = 'printname'
DESC = 'desc'
NORTH = 'north'
SOUTH = 'south'
EAST = 'east'
WEST = 'west'
GROUND = 'GROUND'
#MERCHANT = 'merchant'
#MOB = 'mob'

# for items
LONGDESC = 'longdesc'
SHORTDESC = 'shortdesc'
PICKABLE = 'pickable'
#EDIBLE = 'edible'
REFNAME = 'refname'

# screen dimension
SCREEN_WIDTH = 80

# player variables
location = 'Spawn'
inventory = []
showFullExits = True

# world data
wTiles = {
    'spawn': {
        PRINTNAME: "Forest Clearing",
        DESC: ("A nondescript clearing. "
               "There are trees all over. "
               "The only way to go is north."),
        NORTH: "North of spawn.",
        SOUTH: None,
        EAST: None,
        WEST: None,
        GROUND: ["Shovel", "Tape"]
    }
}


# helper functions
def location(tile):
    """
    prints out tile information
    """
    border_len = len(wTiles[tile][PRINTNAME])

    print(":" * border_len)
    print(wTiles[tile][PRINTNAME])
    print(":" * border_len + "\n")

    print("\n".join(textwrap.wrap(wTiles[tile][DESC], SCREEN_WIDTH)))

    if wTiles[tile][GROUND]:
        print("\nItems on the ground:")

        for item in wTiles[tile][GROUND]:
            print("%s" % item)
    else:
        print("There are no items on the ground.")

    print("")

    if wTiles[tile][NORTH]:
        print("NORTH: " + wTiles[tile][NORTH])
    if wTiles[tile][SOUTH]:
        print("SOUTH: " + wTiles[tile][SOUTH])
    if wTiles[tile][EAST]:
        print("EAST: " + wTiles[tile][EAST])
    if wTiles[tile][WEST]:
        print("WEST: " + wTiles[tile][WEST])
