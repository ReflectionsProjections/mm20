from unittest import TestCase, main


## Manages "rooms" which are nodes on our locations graph.
#  Hallways are also "rooms" in this sense.
#  Rooms contain team members and furniture (TODO)
class Room(object):

    ## Initializes a Room object.
    # @param name
    #   The identifier of the room.
    # @param furniture
    #   Test
    def __init__(self, room_id):
        self.connectedRooms = dict()
        self.name = room_id

    def __str__(self):
        return "<id:{}, connected_rooms:{}>".format(self.name, self.connectedRooms.keys())

    ## Returns connected rooms
    def getConnectedRooms(self):
        return self.connectedRooms.keys()

    ## Connects one room to another
    # @param room
    #   The room to connect to this room
    # @throws ValueError
    #   Throws a value error if this room and the passed in
    #   room are already connected.
    def connectRoom(self, room):
        if not isinstance(room, Room):
            raise TypeError("room is not a Room Object")
        if self.isConnectedTo(room):
            raise ValueError("These two rooms are already connected.")
        else:
            self.connectedRooms[room.name] = room
            room.connectedRooms[self.name] = self

    ## Disconnects two rooms
    # @param room
    #   The room to disconnect from this room
    def disconnectRoom(self, room):
        if not isinstance(room, Room):
            raise TypeError("room is not a Room Object")
        if not self.isConnectedTo(room):
            raise KeyError("These two rooms are not connected")
        del self.connectedRooms[room.name]
        del room.connectedRooms[self.name]

    ## Reports whether two rooms are connected
    # @param room
    #   The room which is check whether it is connected to
    #   this room.
    # @return
    #   Returns whether this room is connected to the passed in room.
    def isConnectedTo(self, room):
        if not isinstance(room, Room):
            raise TypeError("room is not a Room Object")
        return room.name in self.connectedRooms


## ## Tests all of the functionality in Room
class TestRoom(TestCase):
    def setUp(self):
        self.room = Room("testRoom")

    def testInitCorrect(self):
        room = Room("testRoom")
        self.assertEqual(room.name, "testRoom")
        self.assertFalse(room.getConnectedRooms())

    def testInitIncorrect(self):
        with self.assertEqual(TypeError):
            Room(None)

    def testConnectAValidRoom(self):
        roomTwo = Room("testRoom2")
        self.room.connectRoom(roomTwo)
        self.assertListEqual(self.room.getConnectedRooms(), [roomTwo.name])

    def testConnectAnInvalidRoom(self):
        with self.assertRaises(TypeError):
            self.room.connectRoom("NotARoom")

    def testConnectARoomAlreadyConnected(self):
        roomTwo = Room("testRoom2")
        self.room.connectRoom(roomTwo)
        with self.assertRaises(ValueError):
            self.room.connectRoom(roomTwo)

    def testDisconnectRoom(self):
        roomTwo = Room("testRoom2")
        self.room.connectRoom(roomTwo)
        self.room.disconnectRoom(roomTwo)
        self.assertFalse(self.room.getConnectedRooms())

    def testDisconnectNotARoom(self):
        with self.assertRaises(TypeError):
            self.room.disconnectRoom("NotARoom")

    def testDisconnectNotConnectedRoom(self):
        roomTwo = Room("testRoom2")
        with self.assertRaises(KeyError):
            self.room.disconnectRoom(roomTwo)

    def testIsConnectedToActuallyConnected(self):
        roomTwo = Room("testRoom2")
        self.room.connectRoom(roomTwo)
        self.assertTrue(self.room.isConnectedTo(roomTwo))

    def testIsConnectedNotConnected(self):
        roomTwo = Room("testRoom2")
        self.assertFalse(self.room.isConnectedTo(roomTwo))

    def testIsConnectedNotARoom(self):
        with self.assertRaises(TypeError):
            self.room.isConnectedTo("NotARoom")

if __name__ == "__main__":
    main()
