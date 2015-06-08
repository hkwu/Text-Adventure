#! python3

__title__ = "Python Space Adventure (real name pending)"

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
    'spawn': NPCTile("Control Station",
                        ("This is a control station located fore of "
                         "the midship. "
                         "Commands issued by the bridge are relayed "
                         "here via electronic links to the various "
                         "sections of the ships directly. "
                         "Wires and panels now hang loose from the "
                         "ceiling and several displays have gone dark, "
                         "though everything else seems to be in good "
                         "physical condition."),
                        'ctrl_storage', 'ctrl_entrance', 'ctrl_hall1',
                        'ctrl_lift_4', None, None, {}, ['lt_nates'],
                        [("You awaken to the feeling of blood dripping "
                          "down your forehead. Your eyes try to follow "
                          "lines of the floor when you realize that "
                          "your whole body feels like it's been thrown "
                          "out of a car. Slowly, you ease your head up "
                          "to try to gather your senses. The room around "
                          "you looks a little different than it did before. "
                          "Dim auxiliary lighting has taken the place of the "
                          "usual overhead lamps, some of which have fallen "
                          "out of the ceiling and flail around helplessly "
                          "in their wires. Chairs, or at least those not "
                          "bolted down, are scattered around the room.\n"
                          "As you come to, a fuzzy face hovers over you."),
                         ("Stranger: \"Are you awake? Take your time. "
                          "We had quite a landing.\""),
                         ("You ease yourself up against the wall. The "
                          "unfamiliar face begins to sharpen and you "
                          "manage to catch a glimpse of the name on "
                          "her uniform."),
                         ("Lt. Nates: \"What happened? Don't know. Hit "
                          "some kind of trouble in the atmosphere. I "
                          "know about as much as you. The ship got dragged "
                          "down pretty quick. I've never seen anything like "
                          "it. I overheard a couple of techs over IntraNet; "
                          "they were saying something about a gravitational "
                          "anomaly, but that's not really my expertise.\"\n"
                          "Lt. Nates' eyes drift to your forehead.\n"
                          "Lt. Nates: \"Hey, if you feel like you're up "
                          "for it, would you mind heading to the bridge "
                          "and asking around a bit? Figure out what's "
                          "going on? I've got to stick around here and "
                          "manage this mess. You can stop by the MedBay "
                          "while you're at it.\"\n"
                          "She glances over her shoulder.\n"
                          "Lt. Nates: \"Oh, and I should probably mention "
                          "that the PowerLift over there is down, so you'll "
                          "need to find another way to get to the other "
                          "floors. Best of luck!\"")]),
    'ctrl_storage': TravelTile("Bow Storage",
                               ("A medium-sized room that lies beyond "
                                "the main controls, capable of storing "
                                "more than a hundred cargo blocks. "
                                "There might be something useful in here, "
                                "but everything has fallen onto the floor. "
                                "You groan at the thought of cleaning "
                                "this up."),
                               None, 'spawn', None, None, None, None,
                               {'off_pistol': 3, 'Test': 10}, None),
    'ctrl_lift_4': TravelTile("PowerLift",
                              ("A PowerLift is capable of transporting "
                               "goods and people to different floors. "
                               "The unit is currently unpowered."),
                              None, None, 'spawn', None, None, None, {},
                              None),
    'ctrl_entrance': TravelTile("Control Station - Entry",
                                ("You stand at the entry to the bow control "
                                 "station. The airtight doors to the room "
                                 "have jammed themselves open, and it doesn't "
                                 "look like they'll be operational any time "
                                 "soon."
                                 "To the left is the door to the west wing "
                                 "of the control station, which includes "
                                 "the officers' lounge. The door is locked "
                                 "and requires a keycard to get in."),
                                'spawn', None, None, None, None, None, {},
                                None),
    'ctrl_hall1': TravelTile("Control Wing - East",
                             ("A hallway in the eastern wing of the "
                              "control station. Weapons Control lies "
                              "to the south."),
                             None, 'ctrl_weps', 'ctrl_hall2',
                             'spawn', None, None, {}, None),
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
                            'ctrl_hall1', None, None, None, None, None, {},
                            None),
    'ctrl_hall2': TravelTile("Control Wing - East",
                             ("A hallway in the eastern wing of the "
                              "control station. Life Support lies "
                              "to the north and Comms are to the south."),
                             'ctrl_ls', 'ctrl_comm', None,
                             'ctrl_hall1', None, None, {},
                             None),
    'ctrl_ls': TravelTile("Life Support Control",
                          ("You stand before the various displays "
                           "pulling readings from the different "
                           "sections of the ship. Everything from "
                           "oxygen levels, temperature, atmospheric "
                           "pressure and more is collected and analyzed "
                           "by the ship's AI. You slightly marvel at "
                           "the complexity of the machinery."),
                          None, 'ctrl_hall2', None, None, None, None, {},
                          None),
    'ctrl_comm': TravelTile("Communications Control",
                            ("The communications hub hasn't sustained "
                             "much damage at all. A few upturned cups "
                             "of coffee stain the workstations but other "
                             "than that it's as if the room had been "
                             "untouched."),
                            'ctrl_hall2', None, None, None, None, None, {},
                            None)
}

# Entity instances
player = Player("Test")
wNPC = {
    'lt_nates': NPC("Lt. Nates", "F",
                    ("She gives you an annoyed look when you stare "
                     "in her direction."), 'spawn',
                    {'off_uniform': 1, 'off_pistol': 1},
                    100, ['off_pistol'], 'off_uniform', {}, False)
}

# Item instances
wItems = {
    'Test': Item("Test", "Test", 1, True),
    # Weapons
    'off_pistol': Firearm("Officer's Pistol",
                          ("The standard issue officer's pistol, "
                           "constructed from a hardened CarboSteel "
                           "body that's guaranteed to be sleek and "
                           "functional."), 50, 15, 'Gauss Pellet'),
    # Ammunition
    'Gauss Pellet': Ammunition("Gauss Pellet",
                               ("A common projectile found in many of the "
                                "Air Force's off-world combat equipment. "
                                "The pellet is shaped to induce maximum "
                                "penetration at longer distances than "
                                "conventional projectiles."), 1),
    # Armour
    'off_uniform': Armour("Officer's Uniform",
                          ("A dark blue uniform issued to the officers "
                           "in the Air Force. It comes with leather boots "
                           "and a custom colour sash."), 25, 10)
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
