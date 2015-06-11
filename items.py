import utils


# Item classes #

# Base item
class Item(object):
    def __init__(self, name, desc, price, stackable, pickable):
        self.name = name
        self.desc = desc
        self.price = price
        self.stackable = stackable
        self.pickable = pickable


# Generic items
class Sign(Item):
    def __init__(self, desc):
        Item.__init__(self, "Sign", desc, 0, False, False)


class WelcomeSign(Sign):
    def __init__(self):
        Sign.__init__(self,
                      ("Welcome to the woods! Hope you're having a "
                       "grand time. Watch out for the dangers lurking "
                       "beyond every corner!"))


# Weapons
class Weapon(Item):
    is_firearm = False

    def __init__(self, name, desc, price,
                 damage):
        Item.__init__(self, name, desc, price, False, True)
        self.damage = damage


class Ammunition(Item):
    def __init__(self, name, desc, price):
        Item.__init__(self, name, desc, price, True, True)


class Firearm(Weapon):
    def __init__(self, name, desc, price,
                 damage, ammo):
        Weapon.__init__(self, name, desc, price, damage)
        self.ammo = ammo
        self.is_firearm = True


class IronSword(Weapon):
    def __init__(self):
        Weapon.__init__(self, "Iron Sword",
                        "A sturdy iron sword.", 15, 5)


# Armour
class Armour(Item):
    def __init__(self, name, desc, price,
                 defence):
        Item.__init__(self, name, desc, price, False, True)
        self.defence = defence
