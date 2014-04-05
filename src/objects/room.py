from random import randint
class Room(object):

    ## Initializes a Room object with the following attributes
    # @param furniture A dict of furniture objects to be placed in the room of {key:value} format {name:(posX,posY)}
    def __init__(self, furniture=dict(), name = (0,0,0,0), connectedRooms={}):

        # Initialize parameters
        self.furniture = furniture
        self.name = name
        self.connectedRooms = connectedRooms

    def __str__(self):
        return "<id:{}, connected_rooms:{}>".format(name, connectedRooms.keys)
        

    ## Get connected rooms
    def getConnectedRooms(self):
        return self.connected_rooms
        
    
    ## Connect one room to another (both ways)
    # @throws ValueError Thrown if self and room are already connected
    def addConnectedRoom(self,room):
        if isConnectedTo(room):
            raise ValueError("These two rooms are already connected.")
        else:
            self.connectedRooms.append(room)
            room.connectedRooms.append(self) # This goes both ways
    
    ## Remove connected room
    # @errors Won't error if self and room aren't connected
    def removeConnectedRoom(self,room):

        # Check that connection goes both ways; otherwise error out
        if isConnectedTo(room):
            self.connected_rooms.remove(room)
            room.connected_rooms.remove(self)
            
    ##  Check if this room is connected to another
    # @throws ValueError Thrown if self and room are only connected in one way (indicates an error somewhere upstream)
    def isConnectedToRoom(room):
        counter = 0
        if room in self.connectedRooms:
            counter += 1
        if self in room.connectedRooms:
            counter += 1

        # Error check
        if counter == 1:
            raise ValueError("The connection between these rooms only goes one way (i.e. A --> B, instead of A <-> B).")

        # Done!
        return counter == 2;
    

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


