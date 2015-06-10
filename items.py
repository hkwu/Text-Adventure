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
        # player.loc.location()

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
