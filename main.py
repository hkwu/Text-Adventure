#! python3

# Text adventure in Python (name pending)
# by Kelvin Wu
# initial commit 2015-06-01

# kudos to Al Sweigart and Phillip Johnson for their Python
# text game guides

# Required libraries
import cmd
import os
import string
import textwrap

# Screen dimension
SCREEN_WIDTH = 75


# Tile classes

# Basic tile
class TravelTile(object):
    def __init__(self, name, desc, north,
                 south, east, west, up,
                 down, ground):
        self.name = name
        self.desc = desc
        self.north = north
        self.south = south
        self.east = east
        self.west = west
        self.up = up
        self.down = down
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
        if self.up:
            print("UP: %s" % wTiles[self.up].name)
        if self.down:
            print("DOWN: %s" % wTiles[self.down].name)

        # events will appear under this border
        print("")
        print("~" * 20)
        print("")


# NPC tiles
class NPCTile(TravelTile):
    def __init__(self, name, desc, north,
                 south, east, west, up,
                 down, ground, npc):
        TravelTile.__init__(name, desc, north, south,
                            east, west, up, down, ground)
        self.npc = npc

    def talk(self, npc):
        pass


# Entity classes #

# Base entity
class Entity(object):
    def __init__(self, name, loc, inv,
                 coin, weapon, armour,
                 desc, gender):
        self.name = name
        self.loc = loc
        self.inv = inv
        self.coin = coin
        self.weapon = weapon
        self.armour = armour
        self.desc = desc
        self.gender = gender

    def examine(self):
        """Examines the entity."""
        cls()
        self.loc.location()

        print("You look at %s.\n" % self.name)

        examining = ""

        if self.gender == "M":
            examining += "He"
        elif self.gender == "F":
            examining += "She"
        else:
            examining += "It"

        examining += " is wearing a %s and wields a %s." % (self.armour,
                                                            self.weapon)
        print(examining)


# Player entity with additional traits
class Player(Entity):
    def __init__(self, name):
        Entity.__init__(self, name, wTiles['spawn'], [],
                        50, None, None, None, None)
        self.hp = 100
        self.win = False

    def get_inv(self):
        """
        print player's inventory
        """
        cls()

        if self.inv:
            print("Inventory:")

            for item in self.inv:
                print(item)
        else:
            print("Your inventory is empty.")

    def move(self, direction):
        """
        moves player in direction
        """
        cls()

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
        elif direction == "up" and self.loc.up:
            self.loc = wTiles[self.loc.up]
            self.loc.location()
        elif direction == "down" and self.loc.down:
            self.loc = wTiles[self.loc.down]
            self.loc.location()
        else:
            self.loc.location()
            print("There is nothing over there!")

    def take(self, item):
        """
        moves pickable item to player's inventory
        """
        case_proper = string.capwords(item)
        cls()

        if not item:
            self.loc.location()
            print("What are you trying to take?")
        elif case_proper == "All" and self.loc.ground:
            for item in self.loc.ground:
                self.inv.append(item)
            
            self.loc.ground = []

            self.loc.location()
            print("You take everything.")
        elif case_proper == "All":
            self.loc.location()
            print("There is nothing to take.")
        elif case_proper in self.loc.ground:
            self.loc.ground.remove(case_proper)
            self.inv.append(case_proper)

            self.loc.location()
            print("You take the %s." % case_proper)
        else:
            self.loc.location()
            print("That's not even on the ground.")

    def drop(self, item):
        """
        moves item to the ground
        """
        case_proper = string.capwords(item)
        cls()

        if not item:
            self.loc.location()
            print("What are you trying to drop?")
        elif case_proper == "All" and self.inv:
            for item in self.inv:
                self.loc.ground.append(item)

            self.inv = []

            self.loc.location()
            print("You drop everything on the ground.")
        elif case_proper == "All":
            self.loc.location()
            print("You have nothing to drop.")
        elif case_proper in self.inv:
            self.inv.remove(case_proper)
            self.loc.ground.append(case_proper)

            self.loc.location()
            print("You throw the %s on the ground." % case_proper)
        else:
            self.loc.location()
            print("You don't even have one of those.")


# NPC entities
class NPC(Entity):
    def __init__(self, name, gender, desc,
                 loc, inv, coin, weapon,
                 armour, lines):
        Entity.__init__(self, name, loc, inv,
                        coin, weapon, armour, desc,
                        gender)
        self.lines = lines

    def purchase(self, item):
        pass


# Mobs
class Mob(Entity):
    def __init__(self, name, desc, loc,
                 inv, coin, weapon, armour):
        Entity.__init__(self, name, loc, inv,
                        coin, weapon, armour)
        self.desc = desc


# Item classes #

# Base item
class Item(object):
    def __init__(self, name, desc, price):
        self.name = name
        self.desc = desc
        self.price = price

    def examine(self):
        cls()
        self.loc.location()

        print("You examine the %s.\n" % self.name)
        print(self.desc + " It is worth %d coins." % self.price)


# Weapons
class Weapon(Item):
    def __init__(self, name, desc, price,
                 damage):
        Item.__init__(name, desc, price)
        self.damage = damage


# Armour
class Armour(Item):
    def __init__(self, name, desc, price,
                 defence):
        Item.__init__(name, desc, price)
        self.defence = defence


# Dictionaries to contain the class instances

# World tiles
wTiles = {
	# Spawn - Control Station
    'spawn': TravelTile("Control Station",
                        ("This is a control station located fore of "
                         "the ship. "
                         "Commands issued by the bridge are relayed "
                         "here via electronic links to the various "
                         "sections of the ships directly. "
                         "Wires and panels now hang loose from the "
                         "ceiling and several displays have gone dark, "
                         "though everything else seems to be in good "
                         "physical condition."),
                        'ctrl_storage', 'ctrl_entrance', 'ctrl_hall1', 
                        'ctrl_lift_4', None, None, []),
    'ctrl_storage': TravelTile("Bow Storage",
    						   ("A medium-sized room that lies beyond "
    						   	"the main controls, capable of storing "
    						   	"more than a hundred cargo blocks. "
    						   	"There might be something useful in here, "
    						   	"but everything has fallen onto the floor. "
    						   	"You groan at the thought of cleaning "
    						   	"this up."),
    						   None, 'spawn', None, None, None, None, 
    						   ['Broken Electronics', 'PalmPal']),
    'ctrl_lift_4': TravelTile("PowerLift",
    						("A PowerLift is capable of transporting "
    						 "goods and people to different floors. "
    						 "The unit is currently unpowered."),
    						None, None, 'spawn', None, None, None, []),
    'ctrl_entrance': TravelTile("Control Station - Entry",
	                       ("You stand at the entry to the bow control "
	                        "station. The airtight doors to the room have "
	                        "jammed themselves open, and it doesn't look "
	                        "like they'll be operational any time soon.\n\n"
	                        "To the left is the door to the west wing "
	                        "of the control station, which includes "
	                        "the officers' lounge. The door is locked "
	                        "and requires a keycard to get in."), 
                        'spawn', None, None, None, None, None, []),
    'ctrl_hall1': TravelTile("Control Wing - East",
    						 ("A hallway in the eastern wing of the "
    						  "control station. Weapons Control lies "
    						  "to the south."),
    						 None, 'ctrl_weps', 'ctrl_hall2', 
    						 'spawn', None, None, []),
    'ctrl_weps': TravelTile("Weapons Control",
    						("You stand in the darkened room that "
    						 "houses the controls for the ship's batteries. "
    						 "In routine operations the room is lit "
    						 "only by a few darklights. Now that the "
    						 "main power is out, only the consoles "
    						 "are producing any illumination. Weapons "
    						 "is one of the few systems designated as "
    						 "essential and thus capable of drawing "
    						 "auxiliary power in emergencies."),
    						'ctrl_hall1', None, None, None, None, None, []),
    'ctrl_hall2': TravelTile("Control Wing - East",
    						 ("A hallway in the eastern wing of the "
    						  "control station. Life Support lies "
    						  "to the north and Comms are to the south."),
    						 'ctrl_ls', 'ctrl_comm', None, 
    						 'ctrl_hall1', None, None, []),
    'ctrl_ls': TravelTile("Life Support Control",
    	                  ("You stand before the various displays "
    	                   "pulling readings from the different "
    	                   "sections of the ship. Everything from "
    	                   "oxygen levels, temperature, atmospheric "
    	                   "pressure and more is collected and analyzed "
    	                   "by the ship's AI. You slightly marvel at "
    	                   "the complexity of the machinery."),
    	                  None, 'ctrl_hall2', None, None, None, None, []),
    'ctrl_comm': TravelTile("Communications Control",
    						("The communications hub hasn't sustained "
    					     "much damage at all. A few upturned cups "
    					     "of coffee stain the workstations but other "
    					     "than that it's as if the room had been "
    					     "untouched."),
    						'ctrl_hall2', None, None, None, None, None, [])
}

# Entity instances
player = Player("Test")
wNPC = {
    
}

# Item instances
wItems = {
    
}


# CMD interface class
class InputCmd(cmd.Cmd):
    prompt = "\n> "

    # Interface functions
    def do_quit(self, arg):
        """\nQuit the game."""
        cls()

        return True

    def do_location(self, arg):
        """\nWhere am I?"""
        player.loc.location()

    def do_inventory(self, arg):
        """\nLists the items in your inventory."""
        player.get_inv()

    # Movement functions
    def do_north(self, arg):
        """\nGo north."""
        player.move("north")

    def do_south(self, arg):
        """\nGo south."""
        player.move("south")

    def do_east(self, arg):
        """\nGo east."""
        player.move("east")

    def do_west(self, arg):
        """\nGo west."""
        player.move("west")

    def do_up(self, arg):
        """\nGo up."""
        player.move("up")

    def do_down(self, arg):
        """\nGo down."""
        player.move("down")

    # Interaction functions
    def do_take(self, arg):
        """\nPick up an item."""
        player.take(arg)

    def do_drop(self, arg):
        """\nDrop an item."""
        player.drop(arg)

    # Help topics
    def help_general(self):
        cls()

        help_msg = ("Welcome to the Python Text Adventure. "
                    "The aim of the game is to explore the "
                    "world and interact with the different "
                    "entities within. For help at any time, "
                    "enter HELP [?] to list help topics or "
                    "type \"HELP <topic>\" to get specific "
                    "information on a topic. You can QUIT [Q] "
                    "the game at any time.")

        print("=" * 7)
        print("GENERAL")
        print("=" * 7)
        print("")
        print("\n".join(textwrap.wrap(help_msg, SCREEN_WIDTH)))

    def help_movement(self):
        cls()

        help_msg = ("You can move to the NORTH [N], SOUTH [S], "
                    "EAST [E] and WEST [W] in addition to going "
                    "UP [U] or DOWN [D]. Explore as much as you want. "
                    "If you need to remind yourself where you are, "
                    "look up your LOCATION.")

        print("=" * 8)
        print("MOVEMENT")
        print("=" * 8)
        print("")
        print("\n".join(textwrap.wrap(help_msg, SCREEN_WIDTH)))

    def help_interaction(self):
        cls()

        help_msg = ("There are different ways to interact with "
                    "the game environment. If you see something "
                    "you like, you can TAKE it and put it in your "
                    "INVENTORY. You might also find it useful to "
                    "DROP certain items when you don't want to clutter "
                    "your pack. If you're in a rush, it's probably "
                    "easier to just TAKE ALL or DROP ALL of those "
                    "things at once. You can also EXAMINE people "
                    "or items more closely.")

        print("=" * 11)
        print("INTERACTION")
        print("=" * 11)
        print("")
        print("\n".join(textwrap.wrap(help_msg, SCREEN_WIDTH)))

    # Invalid command message
    def default(self, arg):
        cls()

        error_msg = ("That is not a valid command. "
                     "Please try again. "
                     "Remember to type all commands in lowercase "
                     "(check HELP [?] for a list of commands).")

        print("=" * 15)
        print("INVALID COMMAND")
        print("=" * 15)
        print("")
        print("\n".join(textwrap.wrap(error_msg, SCREEN_WIDTH)))

    # Aliases
    do_q = do_quit

    do_n = do_north
    do_s = do_south
    do_e = do_east
    do_w = do_west
    do_u = do_up
    do_d = do_down


# Utility functions
def cls():
    """Clears the screen."""
    os.system("cls" if os.name == "nt" else "clear")

# Input loop
if __name__ == '__main__':
    cls()
    print("Python Text Adventure\n"
          "====================\n\n"
          "Press any key to begin.\n")
    raw_input("> ")
    cls()

    player = Player("Test")
    player.loc.location()
    InputCmd().cmdloop()

    print("Game Over!")
