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
                if self.ground[item] > 1:
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
