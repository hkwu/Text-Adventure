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
