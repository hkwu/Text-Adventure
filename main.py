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
DESC = 'desc'
NORTH = 'north'
SOUTH = 'south'
EAST = 'east'
WEST = 'west'
TILE = 'tile'
#MERCH = 'merch'
GROUND = 'ground'
LISTDESC = 'listdesc'
LOOKDESC = 'lookdesc'
PICKABLE = 'pickable'
EDIBLE = 'edible'
DESCWORDS = 'descwords'

SCREEN_WIDTH = 80

# player variables
location = 'Spawn'
inventory = []
showFullExits = True

# world data
wTiles = {
    'Spawn': {
        DESC: "You spawned here.",
        NORTH: "North of spawn.",
        SOUTH: "South of spawn.",
        EAST: "East of spawn.",
        WEST: "West of spawn.",
        GROUND: []
    }
}

# helper functions
def location(tile):
    """
    prints out tile information
    """
    pass
