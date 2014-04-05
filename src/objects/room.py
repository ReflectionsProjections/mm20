class Room(object): #TODO: This class doesn't need to know what the furniture's location is, it just needs to know that it exists

    ## Initializes a Room object with the following attributes
    # @param furniture A dict of furniture objects to be placed in the room of {key:value} format {name:(posX,posY)}
    def __init__(self, furniture=dict(), color=(0, 0, 0, 0), connectedRooms=[]):
        # Initialize parameters
        self.furniture = furniture
        self.color = color
        self.connectedRooms = connectedRooms

    ## Get connected rooms
    def getConnectedRooms(self):
        return self.connected_rooms

    ## Connect one room to another (both ways)
    # @throws ValueError Thrown if self and room are already connected
    def addConnectedRoom(self, room):
        if self.isConnectedTo(room):
            raise ValueError("These two rooms are already connected.")
        else:
            self.connectedRooms.append(room)
            room.connectedRooms.append(self)  # This goes both ways

    ## Remove connected room
    # @errors Won't error if self and room aren't connected
    def removeConnectedRoom(self, room):

        # Check that connection goes both ways; otherwise error out
        if self.isConnectedTo(room):
            self.connected_rooms.remove(room)
            room.connected_rooms.remove(self)

    ##  Check if this room is connected to another
    # @throws ValueError Thrown if self and room are only connected in one way (indicates an error somewhere upstream)
    def isConnectedToRoom(self, room):
        counter = 0
        if room in self.connectedRooms:
            counter += 1
        if self in room.connectedRooms:
            counter += 1

        # Error check
        if counter == 1:
            raise ValueError("The connection between these rooms only goes one way (i.e. A --> B, instead of A <-> B).")

        # Done!
        return counter == 2

    # What is the point of this? furniture and self.furniture seem like the same thing - Ace
    # (were you intending furniture to be something outside of this class? if so, you should
    #  pass it in as an argument)
    def spawnObjects(self):
        """
        Spawns all objects that are currently in the furniture dictionary
        """
        for obj in self.furniture:
            self.placeFurniture(self.furniture[obj], obj[0], obj[1])

    def removeFurniture(self, furn):
        """
        Delete all pieces of furniture in the furniture dictionary with the name {furn}.
        """
        for coords in self.furniture:
            if self.furniture[coords] == furn:
                del self.furniture[coords]
        pass

if __name__ == "__main__":
    room1104 = Room({(0,0):"couch", (2,2):"chair"})
    print room1104.furniture

    room2405 = Room({(2,4):"snack table"})
    print room2405.furniture


