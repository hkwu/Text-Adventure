import data
import string
import utils


# Entity classes #

# Base entity
class Entity(object):
    def __init__(self, name, loc, inv,
                 money, weapon, armour,
                 desc, gender):
        self.name = name
        self.loc = loc
        self.inv = inv
        self.money = money
        self.weapon = weapon
        self.armour = armour
        self.desc = desc
        self.gender = gender


# Player entity with additional traits
class Player(Entity):
    hp = 100

    def __init__(self, name):
        Entity.__init__(self, name, data.wTiles['spawn'], {},
                        50, None, None, None, None)

    def get_inv(self):
        """Print player's inventory"""
        # utils.cls()

        if self.inv:
            print("Inventory:")

            for item in self.inv:
                if self.inv[item] > 1:
                    print(data.wItems[item].name + " (%d)" % self.inv[item])
                else:
                    print(data.wItems[item].name)
        else:
            print("Your inventory is empty.")

    def move(self, direction):
        """Moves player in direction"""
        # utils.cls()

        if direction == "north" and self.loc.north:
            self.loc = data.wTiles[self.loc.north]
            self.loc.location()
        elif direction == "south" and self.loc.south:
            self.loc = data.wTiles[self.loc.south]
            self.loc.location()
        elif direction == "east" and self.loc.east:
            self.loc = data.wTiles[self.loc.east]
            self.loc.location()
        elif direction == "west" and self.loc.west:
            self.loc = data.wTiles[self.loc.west]
            self.loc.location()
        elif direction == "up" and self.loc.up:
            self.loc = data.wTiles[self.loc.up]
            self.loc.location()
        elif direction == "down" and self.loc.down:
            self.loc = data.wTiles[self.loc.down]
            self.loc.location()
        else:
            self.loc.location()
            print("There is nothing over there!")

    ### NEED TO FIX THIS ###
    def take(self, item):
        """Moves pickable item to player's inventory"""
        case_proper = string.capwords(item)
        # utils.cls()

        if not item:
            # self.loc.location()
            print("What are you trying to take?")
        elif case_proper in self.loc.ground:
            # Decrease item count if multiple copies exist,
            # remove item altogether if only one copy
            if not data.wItems[case_proper].pickable:
                print("You can't take that!")

                return

            if self.loc.ground[case_proper] > 1:
                self.loc.ground[case_proper] -= 1
            else:
                self.loc.ground.pop(case_proper)

            if case_proper in self.inv:
                self.inv[case_proper] += 1
            else:
                self.inv[case_proper] = 1

            # self.loc.location()
            print("You take the %s." % case_proper)
        else:
            # self.loc.location()
            print("That's not even on the ground.")

    def take_all(self):
        """Moves all pickable items to player's inventory"""
        if self.loc.ground:
            for item in self.loc.ground:
                if data.wItems[item].pickable and item in self.inv:
                    self.inv[item] += self.loc.ground[item]
                    self.loc.ground.pop(item)
                elif data.wItems[item].pickable:
                    self.inv[item] = self.loc.ground[item]
                    self.loc.ground.pop(item)

            # self.loc.location()
            print("You take everything you can.")
        else:
            # self.loc.location()
            print("There is nothing to take.")

    def drop(self, item):
        """Moves item in player's inventory to the ground"""
        case_proper = string.capwords(item)
        # utils.cls()

        if not item:
            # self.loc.location()
            print("What are you trying to drop?")
        elif case_proper in self.inv:
            if self.inv[case_proper] > 1:
                self.inv[case_proper] -= 1
            else:
                self.inv.pop(case_proper)

            if case_proper in self.loc.ground:
                self.loc.ground[case_proper] += 1
            else:
                self.loc.ground[case_proper] = 1

            # self.loc.location()
            print("You throw the %s on the ground." % case_proper)
        else:
            # self.loc.location()
            print("You don't even have one of those.")

    def drop_all(self):
        """Moves all items in player's inventory to the ground"""
        if self.inv:
            for item in self.inv:
                if item in self.loc.ground:
                    self.loc.ground[item] += self.inv[item]
                else:
                    self.loc.ground[item] = self.inv[item]

            self.inv = {}

            # self.loc.location()
            print("You drop everything on the ground.")
        else:
            # self.loc.location()
            print("You have nothing to drop.")

    def examine_item(self, item):
        """Examines an item on the ground."""
        case_proper = string.capwords(item)

        for item in self.loc.ground:
            if case_proper == data.wItems[item].name:
                print("You examine the %s.\n" % data.wItems[item].name)
                utils.wrap_str(data.wItems[item].desc)
                print("\nIt is worth %d coins." % data.wItems[item].price)

                break
        else:
            print("That doesn't even exist here.")


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
                print(data.wItems[item].name)
        else:
            print("%s has nothing to sell!" % self.name)

    def purchase(self, item):
        """Purchases item from merchant"""
        if self.merchant:
            pass
        else:
            # player.loc.location()
            print("You can't buy anything from %s." % self.name)

    def sell(self, item):
        """Sells item to the merchant"""
        if self.merchant:
            pass
        else:
            # player.loc.location()
            print("You can't sell anything to %s." % self.name)


# Mobs
class Mob(Entity):
    def __init__(self, name, desc, loc,
                 inv, credits, weapon, armour):
        Entity.__init__(self, name, loc, inv,
                        credits, weapon, armour,
                        desc, None)
