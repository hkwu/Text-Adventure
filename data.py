import tiles
import entities
import items

# World tiles
wTiles = {
    # Spawn - Control Station
    'spawn': tiles.TravelTile("Forest Path",
                              ("A path in the forest. It looks like every "
                               "other one that you've walked so far."),
                              'f_path0', None, None, None, None, None, {},
                              [("After a long day of hiking, your feet give "
                                "out under you. You stop to rest under the "
                                "nearest tree and watch the birds fly over "
                                "for a while.")]),
    'f_path0': tiles.TravelTile("Forest Path",
                                "A path in the forest.",
                                None, 'spawn', None, None, None, None, {}, None)
}

# Entities
wNPC = {

}

# Items
wItems = {

}
