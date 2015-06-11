import data
import utils


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
        # utils.cls()

        if not self.visited and self.on_first_visit:
            self.visited = True

            for paragraph in self.on_first_visit:
                utils.cls()
                utils.wrap_str(paragraph)
                print("\nPress ENTER to continue.\n")
                utils.dialogue_prompt()

        # utils.cls()
        border_len = len(self.name)

        print(":" * border_len)
        print(self.name)
        print(":" * border_len + "\n")

        utils.wrap_str(self.desc)
        print("")

        if self.ground:
            print("Items on the ground:")

            for item in self.ground:
                if self.ground[item] > 1:
                    print(data.wItems[item].name + " (%d)" % self.ground[item])
                else:
                    print(data.wItems[item].name)
        else:
            print("There are no items on the ground.")

        print("")

        if self.north:
            print("NORTH: %s" % data.wTiles[self.north].name)
        if self.south:
            print("SOUTH: %s" % data.wTiles[self.south].name)
        if self.east:
            print("EAST: %s" % data.wTiles[self.east].name)
        if self.west:
            print("WEST: %s" % data.wTiles[self.west].name)
        if self.up:
            print("UP: %s" % data.wTiles[self.up].name)
        if self.down:
            print("DOWN: %s" % data.wTiles[self.down].name)

        # events will appear under this border
        # print("")
        # print("~" * 20)
        # print("")


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
        # utils.cls()

        if not self.visited and self.on_first_visit:
            self.visited = True

            for paragraph in self.on_first_visit:
                utils.cls()
                utils.wrap_str(paragraph)
                print("\nPress ENTER to continue.\n")
                utils.dialogue_prompt()

        # utils.cls()
        border_len = len(self.name)

        print(":" * border_len)
        print(self.name)
        print(":" * border_len + "\n")

        utils.wrap_str(self.desc)
        print("")

        if self.npc:
            print("People in this area:")

            for person in self.npc:
                print(data.wNPC[person].name)

            print("")

        if self.ground:
            print("Items on the ground:")

            # Printing item count if there are multiple copies
            for item in self.ground:
                if data.wItems[item] > 1:
                    print(data.wItems[item].name + " (%d)" % self.ground[item])
                else:
                    print(data.wItems[item].name)
        else:
            print("There are no items on the ground.")

        print("")

        if self.north:
            print("NORTH: %s" % data.wTiles[self.north].name)
        if self.south:
            print("SOUTH: %s" % data.wTiles[self.south].name)
        if self.east:
            print("EAST: %s" % data.wTiles[self.east].name)
        if self.west:
            print("WEST: %s" % data.wTiles[self.west].name)
        if self.up:
            print("UP: %s" % data.wTiles[self.up].name)
        if self.down:
            print("DOWN: %s" % data.wTiles[self.down].name)

        # events will appear under this border
        print("")
        print("~" * 20)
        print("")
