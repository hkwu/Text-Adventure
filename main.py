#! python3

__title__ = "Python Fantasy Adventure (real name pending)"

# by Kelvin Wu
# initial commit 2015-06-01

# kudos to Al Sweigart and Phillip Johnson for their Python
# text game guides

# Required libraries
import cmd
import entities
import utils


# CMD interface class
class InputCmd(cmd.Cmd):
    prompt = "\n> "

    # Interface functions
    def do_quit(self, arg):
        """Quit the game."""
        utils.cls()

        return True

    def do_location(self, arg):
        """Where am I?"""
        player.loc.location()

    def do_inventory(self, arg):
        """Lists the items in your inventory."""
        player.get_inv()

    # Movement functions
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

    def do_up(self, arg):
        """Go up."""
        player.move("up")

    def do_down(self, arg):
        """Go down."""
        player.move("down")

    # Interaction functions
    def do_take(self, arg):
        """Pick up an item."""
        if arg.lower() == "all":
            player.take_all()
        else:
            player.take(arg)

    def do_drop(self, arg):
        """Drop an item."""
        if arg.lower() == "all":
            player.drop_all()
        else:
            player.drop(arg)

    def do_examine(self, arg):
        """Examine a person or item."""
        player.examine_item(arg)

    # Help topics
    def help_general(self):
        # utils.cls()

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
        utils.wrap_str(help_msg)

    def help_movement(self):
        # utils.cls()

        help_msg = ("You can move to the NORTH [N], SOUTH [S], "
                    "EAST [E] and WEST [W] in addition to going "
                    "UP [U] or DOWN [D]. Explore as much as you want. "
                    "If you need to remind yourself where you are, "
                    "look up your LOCATION.")

        print("=" * 8)
        print("MOVEMENT")
        print("=" * 8)
        print("")
        utils.wrap_str(help_msg)

    def help_interaction(self):
        # utils.cls()

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
        utils.wrap_str(help_msg)

    # Invalid command message
    def default(self, arg):
        # utils.cls()

        error_msg = ("That is not a valid command. "
                     "Please try again. "
                     "Remember to type all commands in lowercase "
                     "(check HELP [?] for a list of commands).")

        print("=" * 15)
        print("INVALID COMMAND")
        print("=" * 15)
        print("")
        utils.wrap_str(error_msg)

    # Aliases
    do_q = do_quit

    do_n = do_north
    do_s = do_south
    do_e = do_east
    do_w = do_west
    do_u = do_up
    do_d = do_down


# Input loop
if __name__ == '__main__':
    utils.cls()
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
    utils.wrap_str(welcome_msg)
    print("")
    player_name = raw_input("What's your name? ")
    utils.cls()

    player = entities.Player(player_name)
    player.loc.location()
    InputCmd().cmdloop()

    print("Game Over!")
