#! python3

__title__ = "Python Fantasy Adventure (real name pending)"

# by Kelvin Wu
# initial commit 2015-06-01

# kudos to Al Sweigart and Phillip Johnson for their Python
# text game guides

# Required libraries
import string
import textwrap
import cmd
import os

# Screen dimension
SCREEN_WIDTH = 75


# Tile classes

# Basic tile
class TravelTile(object):
    visited = False

    def __init__(self, name, desc, north,
                 south, east, west, up,
                 down, ground, on_first_visit):
        self.name = name
        self.desc = desc
        self.north = north
        self.south = south
        self.east = east
        self.west = west
        self.up = up
        self.down = down
        self.ground = ground
        self.on_first_visit = on_first_visit

    def location(self):
        """
        Prints location information and sets visited status
        to True
        """
        cls()

        if not self.visited and self.on_first_visit:
            self.visited = True

            for paragraph in self.on_first_visit:
                cls()
                wrapStr(paragraph)
                print("\nPress ENTER to continue.\n")
                dialoguePrompt()

        cls()
        border_len = len(self.name)

        print(":" * border_len)
        print(self.name)
        print(":" * border_len + "\n")

        wrapStr(self.desc)
        print("")

        if self.ground:
            print("Items on the ground:")

            for item in self.ground:
                if wItems[item] > 1:
                    print(wItems[item].name + " (%d)" % self.ground[item])
                else:
                    print(wItems[item].name)
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
                 down, ground, npc,
                 on_first_visit):
        TravelTile.__init__(self, name, desc, north, south,
                            east, west, up, down, ground,
                            on_first_visit)
        self.npc = npc

    def location(self):
        """
        Prints location information and sets visited status
        to True
        """
        cls()

        if not self.visited and self.on_first_visit:
            self.visited = True

            for paragraph in self.on_first_visit:
                cls()
                wrapStr(paragraph)
                print("\nPress ENTER to continue.\n")
                dialoguePrompt()

        cls()
        border_len = len(self.name)

        print(":" * border_len)
        print(self.name)
        print(":" * border_len + "\n")

        wrapStr(self.desc)
        print("")

        if self.npc:
            print("People in this area:")

            for person in self.npc:
                print(wNPC[person].name)

            print("")

        if self.ground:
            print("Items on the ground:")

            # Printing item count if there are multiple copies
            for item in self.ground:
                if wItems[item] > 1:
                    print(wItems[item].name + " (%d)" % self.ground[item])
                else:
                    print(wItems[item].name)
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


# Entity classes #

# Base entity
class Entity(object):
    def __init__(self, name, loc, inv,
                 credits, weapon, armour,
                 desc, gender):
        self.name = name
        self.loc = loc
        self.inv = inv
        self.credits = credits
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
    hp = 100

    def __init__(self, name):
        Entity.__init__(self, name, wTiles['spawn'], {},
                        50, None, None, None, None)

    def get_inv(self):
        """Print player's inventory"""
        cls()

        if self.inv:
            print("Inventory:")

            for item in self.inv:
                if self.inv[item] > 1:
                    print(wItems[item].name + " (%d)" % self.inv[item])
                else:
                    print(wItems[item].name)
        else:
            print("Your inventory is empty.")

    def move(self, direction):
        """Moves player in direction"""
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
        """Moves pickable item to player's inventory"""
        case_proper = string.capwords(item)
        cls()

        if not item:
            self.loc.location()
            print("What are you trying to take?")
        elif case_proper == "All" and self.loc.ground:
            for item in self.loc.ground:
                if item in self.inv:
                    self.inv[item] += self.loc.ground[item]
                else:
                    self.inv[item] = self.loc.ground[item]

            self.loc.ground = {}

            self.loc.location()
            print("You take everything.")
        elif case_proper == "All":
            self.loc.location()
            print("There is nothing to take.")
        elif case_proper in self.loc.ground:
            # Decrease item count if multiple copies exist,
            # remove item altogether if only one copy
            if self.loc.ground[case_proper] > 1:
                self.loc.ground[case_proper] -= 1
            else:
                self.loc.ground.pop(case_proper)

            if case_proper in self.inv:
                self.inv[case_proper] += 1
            else:
                self.inv[case_proper] = 1

            self.loc.location()
            print("You take the %s." % case_proper)
        else:
            self.loc.location()
            print("That's not even on the ground.")

    def drop(self, item):
        """Moves item to the ground"""
        case_proper = string.capwords(item)
        cls()

        if not item:
            self.loc.location()
            print("What are you trying to drop?")
        elif case_proper == "All" and self.inv:
            for item in self.inv:
                if item in self.loc.ground:
                    self.loc.ground[item] += self.inv[item]
                else:
                    self.loc.ground[item] = self.inv[item]

            self.inv = {}

            self.loc.location()
            print("You drop everything on the ground.")
        elif case_proper == "All":
            self.loc.location()
            print("You have nothing to drop.")
        elif case_proper in self.inv:
            if self.inv[case_proper] > 1:
                self.inv[case_proper] -= 1
            else:
                self.inv.pop(case_proper)

            if case_proper in self.loc.ground:
                self.loc.ground[case_proper] += 1
            else:
                self.loc.ground[case_proper] = 1

            self.loc.location()
            print("You throw the %s on the ground." % case_proper)
        else:
            self.loc.location()
            print("You don't even have one of those.")


# NPC entities
class NPC(Entity):
    def __init__(self, name, gender, desc,
                 loc, inv, credits, weapon,
                 armour, lines, merchant):
        Entity.__init__(self, name, loc, inv,
                        credits, weapon, armour, desc,
                        gender)
        self.lines = lines
        self.merchant = merchant

    def talk(self):
        """Engages dialogue with NPC"""
        pass

    def shop(self):
        """Prints out the merchant's inventory"""
        if self.merchant and self.inv:
            print("Merchant's Inventory:")

            for item in self.inv:
                print(wItems[item].name)
        else:
            print("%s has nothing to sell!" % self.name)

    def purchase(self, item):
        """Purchases item from merchant"""
        if self.merchant:
            pass
        else:
            player.loc.location()
            print("You can't buy anything from %s." % self.name)

    def sell(self, item):
        """Sells item to the merchant"""
        if self.merchant:
            pass
        else:
            player.loc.location()
            print("You can't sell anything to %s." % self.name)


# Mobs
class Mob(Entity):
    def __init__(self, name, desc, loc,
                 inv, credits, weapon, armour):
        Entity.__init__(self, name, loc, inv,
                        credits, weapon, armour,
                        desc, None)


# Item classes #

# Base item
class Item(object):
    def __init__(self, name, desc, price, stackable):
        self.name = name
        self.desc = desc
        self.price = price
        self.stackable = stackable

    def examine(self):
        cls()
        player.loc.location()

        print("You examine the %s.\n" % self.name)
        print(self.desc + " It is worth %d credits." % self.price)


# Weapons
class Weapon(Item):
    is_firearm = False

    def __init__(self, name, desc, price,
                 damage):
        Item.__init__(self, name, desc, price, False)
        self.damage = damage


class Ammunition(Item):
    def __init__(self, name, desc, price):
        Item.__init__(self, name, desc, price, True)


class Firearm(Weapon):
    def __init__(self, name, desc, price,
                 damage, ammo):
        Weapon.__init__(self, name, desc, price, damage)
        self.ammo = ammo
        self.is_firearm = True


# Armour
class Armour(Item):
    def __init__(self, name, desc, price,
                 defence):
        Item.__init__(self, name, desc, price, False)
        self.defence = defence


# Dictionaries to contain the class instances

# World tiles
wTiles = {
    # Spawn - Control Station
    'spawn': TravelTile("Forest Path",
                        ("A path in the forest. It looks like every "
                         "other one that you've walked so far."),
                        'f_path0', None, None, None, None, None, {},
                        [("After a long day of hiking, your feet give "
                          "out under you. You stop to rest under the "
                          "nearest tree and watch the birds fly over "
                          "for a while.")]),
    'f_path0': TravelTile("Forest Path",
                          ("A path in the forest."),
                          None, 'spawn', None, None, None, None, {}, None)
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

        help_msg = ("Welcome to the game. The aim is to explore "
                    "the world and interact with the different "
                    "entities within. For help at any time, "
                    "enter HELP [?] to list help topics or "
                    "type \"HELP <topic>\" to get specific "
                    "information on a topic. Type all commands "
                    "in lowercase. You can QUIT [Q] the game at "
                    "any time.")

        print("=" * 7)
        print("GENERAL")
        print("=" * 7)
        print("")
        wrapStr(help_msg)

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
        wrapStr(help_msg)

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
        wrapStr(help_msg)

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
        wrapStr(error_msg)

    # Aliases
    do_q = do_quit

    do_n = do_north
    do_s = do_south
    do_e = do_east
    do_w = do_west
    do_u = do_up
    do_d = do_down


# Utility functions
def wrapStr(string):
    """
    Textwraps a string using SCREEN_WIDTH 
    and joins them with newlines, then prints
    """
    split_str = string.splitlines()

    if len(split_str) == 1:
        print("\n".join(textwrap.wrap(split_str[0], SCREEN_WIDTH)))
    else:
        index = 0

        for paragraph in split_str:
            print("\n".join(textwrap.wrap(paragraph, SCREEN_WIDTH)))

            # We don't print extra line at end of entire dialogue
            if index < len(split_str) - 1:
                print("")

            index += 1


def cls():
    """Clears the screen"""
    os.system("cls" if os.name == "nt" else "clear")


def dialoguePrompt():
    """Special prompt for dialogue sequences that allows quitting"""
    choice = raw_input("> ")
    if choice.lower() == "q" or choice.lower() == "quit":
        cls()
        print("Game Over!")
        raise SystemExit
    else:
        return


# Input loop
if __name__ == '__main__':
    cls()
    print(__title__)
    print("=" * len(__title__))
    print("")
    welcome_msg = ("Welcome to the game. The aim is to explore "
                   "the world and interact with the different "
                   "entities within. For help at any time, "
                   "enter HELP [?] to list help topics or "
                   "type \"HELP <topic>\" to get specific "
                   "information on a topic. Type all commands "
                   "in lowercase. You can QUIT [Q] the game at "
                   "any time.")
    wrapStr(welcome_msg)
    print("")
    player_name = raw_input("What's your name? ")
    cls()

    player = Player(player_name)
    player.loc.location()
    InputCmd().cmdloop()

    print("Game Over!")
