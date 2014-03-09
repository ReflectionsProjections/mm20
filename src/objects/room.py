from random import randint
class Room(object):

    # Instance values (a complete list)
    furniture = dict()      # A dictionary of furniture in the room (key = (x,y); value = "furniture name")
    connected_rooms = []    # A list of rooms connected to the current one by doors
    color = (0,0,0,0)       # The color of the room on the map

    # Passes in objects to be placed within the room.
    def __init__(self, furniture=dict(), color = (0,0,0,0), connectedRooms=[]):
        """
        Initializes a room object with the following attributes
        Keyword arguments:
            furniture -- a dictionary of furniture objects to be placed in the room
                         with a tuple key of coordinates for where it should be placed
            
        """

        # Initialize parameters
        self.furniture = furniture
        self.color = color
        self.connectedRooms = connectedRooms

    """
    Get connected rooms
    """
    def getConnectedRooms(self):
        return self.connected_rooms
        
    """
    Add connected room
    Doesn't allow duplicates (and will error if it encounters them)
    """
    def addConnectedRoom(self,room):
        if room in self.connectedRooms:
            raise ValueError("This room is already connected to that room.")
        else:
            self.connectedRooms.append(room)
    
    """
    Remove connected room
    Won't error if the two rooms aren't connected
    """
    def removeConnectedRoom(self,room):
        if room in self.connected_rooms:
            self.connected_rooms.remove(room)
            
    """
    Check if this room is connected to another
    """
    def isConnectedToRoom(room):
        return room in self.connected_rooms
    

    # What is the point of this? furniture and self.furniture seem like the same thing - Ace
    # (were you intending furniture to be something outside of this class? if so, you should
    #  pass it in as an argument)
    def spawnObjects(self):
        
        """
        Spawns all objects that are currently in the furniture dictionary
        """
        for obj in self.furniture:
            placeFurniture(self.furniture[obj],obj[0],obj[1])

    # What is the point of this? furniture and self.furniture seem like the same thing - Ace
    # (were you intending furniture to be something outside of this class? if so, you should
    #  pass it in as an argument)
    def placeFurniture(furn, x, y):
        
        """
        Adds the furniture object to the dictionary and places it at a given coordinate
        """
        furniture[(x,y)] = furn
        
    # This randomly moves furniture around the map. Are you sure it wouldn't be a better idea
    # to use a function that generate a random coordinate and simply move furniture to its
    # result? - Ace   
    def randomizeCoord(self, oldX, oldY):
    
        """
        Moves a piece of furniture to a random empty spot in the room
        """
        oldCoord = (oldX, oldY)

        x = randint(0, self.width)
        y = randint(0, self.length)
        newCoord = (x,y)
        if newCoord not in self.furniture:
            self.furniture[newCoord] = self.furniture[oldCoord]
            self.furniture.pop(oldCoord,None)
        else:
            randomizeCoord(oldX,oldY) # This should be done with a loop instead of recursion (it's more natural that way IMHO - functionalitywise, it doesn't matter as long as we don't encounter stack overflows)
        pass


    def removeFurniture(furn):
    
        """
        Delete all pieces of furniture in the furniture dictionary with the name {furn}.
        """
        for coords in furniture:
            if furniture[coords] == furn:
                del furniture[coords]
        pass
        
    def removeFurniture(x,y):
    
        """
        Delete the piece of furniture at the provided location
        """
        coords = (x,y)
        if coords in furniture:
            del furniture[coords]
        pass

if __name__ == "__main__":
    room1104 = Room({(0,0):"couch", (2,2):"chair"})
    print room1104.furniture

    room2405 = Room({(2,4):"snack table"})
    print room2405.furniture


