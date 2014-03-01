##Authored by Brendan Moriarty (github:Moriartyb)
import random
class Room(object):
    ##
    # Passes in objects to be placed within the room.
    ##
    def __init__(self, furniture={}):
        """
        Initializes a room object with the following attributes
        Keyword arguments:
        furniture -- a dictionary of furniture objects to be placed in the room
        with a tuple key of coordinates for where it should be placed
        """

        self.furniture = furniture  # key is a tuple coordinate(?), value is object to be placed in room.

    def spawnObjects(self):
        """
        Spawns all objects that are currently in the furniture dictionary
        """
        for obj in self.furniture:
            placeFurniture(self.furniture[obj],obj[0],obj[1])

    def placeFurniture(furn, x, y):
        """
        Adds the furniture object to the dictionary and places it at a given coordinate
        """
        if(furn not in furniture):
            furniture[(x,y)] = furn

        pass
    def randomizeCoord(self, oldX, oldY):
        """
        generates a new coordinate, checks if it is already in the dictionary,
        if not removes key and adds new key value pair with new coordinates
        """

        oldCoord = (oldX, oldY)

        x = random.randint(0, self.width)
        y = random.randint(0, self.length)
        newCoord = (x,y)
        if(newCoord not in self.furniture):
            self.furniture[newCoord] = self.furniture[oldCoord]
            self.furniture.pop(oldCoord,None)
        else:
            randomizeCoord(oldX,oldY) # If the room was ever full this would totally break.... probably a bad idea
        pass


    def removeFurniture(furn, x, y):
        """
        Finds a piece of furniture in the dictionary and deletes it. Is this how this should be implemented?
        """
        
        if(furn in furniture):
            del furniture[(x,y)]
        pass
        

if __name__ == "__main__":
    room1104 = Room({(0,0),object})
    print room1104.furniture

    room2405 = Room({(2,4), object})
    print room2405.furniture


