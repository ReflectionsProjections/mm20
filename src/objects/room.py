import unittest


## Raised when an error occurs due to two rooms already being connected
class AlreadyConnectedError(Exception):
    def __init__(self, roomOne, roomTwo):
        self.msg = "Room {0} and {1} are already connected.".format(roomOne, roomTwo)

    def __str__(self):
        return self.msg


## Raised when an error occurs due to two rooms not being connected
class NotConnectedError(Exception):
    def __init__(self, roomOne, roomTwo):
        self.msg = "Room {0} and {1} are not connected!".format(roomOne, roomTwo)

    def __str__(self):
        return self.msg


## Raised when an error occurs due to a member already being in a room
class AlreadyInRoomError(Exception):
    def __init__(self, room, member):
        self.msg = "{0} is already in {1}.".format(member, room)

    def __str__(self):
        return self.msg


## Raised when an error occurs due to a member not being in a room
class NotInRoomError(Exception):
    def __init__(self, room, member):
        self.msg = "{0} is not in {1}.".format(member, room)

    def __str__(self):
        return self.msg


## Raised when an error occurs due to a resource already being available in a room
class AlreadyAvailableError(Exception):
    def __init__(self, room, resource):
        self.msg = "{0} is already available in {1}".format(resource, room)

    def __str__(self):
        return self.msg


## Raised when an error occurs due to a resource not being available in a room
class NotAvailableError(Exception):
    def __init__(self, room, resource):
        self.msg = "{0} is not an available resource in {1}".format(resource, room)

    def __str__(self):
        return self.msg


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
        self.people = set()
        self.resources = set()

    ## Adds a member to this room
    # @param member
    #   The member to add to this room
    def addMember(self, member):
        if member in self.people:
            raise AlreadyInRoomError(self, member)
        self.people.add(member)

    ## Removes a member from this room
    # @param member
    #   The member to remove from this room
    def removeMember(self, member):
        if not member in self.people:
            raise NotInRoomError(self, member)
        self.people.remove(member)

    ## Make a resource available in this room
    # @param resource
    #   the resource to make available as a string.
    def addResource(self, resource):
        if resource in self.resources:
            raise AlreadyAvailableError(self, resource)
        self.resources.add(resource)

    ## Remove a resource from a this room
    # @parameter resource
    #   The resource to remove from this room
    def removeResource(self, resource):
        if not (resource in self.resources):
            raise NotAvailableError(self, resource)
        self.resources.remove(resource)

    ## Returns whether or not a given resource is available in this room
    # @parameter resource
    #   The resource to test the presence of
    def isAvailable(self, resource):
        return resource in self.resources

    def __str__(self):
        return "<id:{0}, connected_rooms:{1}>".format(
            self.name, self.connectedRooms.keys())

    def output_dict(self):
        room_info = {"room": self.name,
                     "connectedRooms": self.connectedRooms.keys(),
                     "peopleInRoom": [p.output_dict() for p in self.people]}
        return room_info

    ## Returns connected rooms
    def getConnectedRooms(self):
        return self.connectedRooms.keys()

    ## Connects one room to another
    # @param room
    #   The room to connect to this room
    # @throws ValueError
    #   Throws a value error if this room and the passed in
    #   room are already connected.
    def connectToRoom(self, room):
        if self.isConnectedTo(room):
            raise AlreadyConnectedError(self, room)
        else:
            self.connectedRooms[room.name] = room
            room.connectedRooms[self.name] = self

    ## Disconnects two rooms
    # @param room
    #   The room to disconnect from this room
    def disconnectRoom(self, room):
        if not self.isConnectedTo(room):
            raise NotConnectedError(self, room)
        del self.connectedRooms[room.name]
        del room.connectedRooms[self.name]

    ## Reports whether two rooms are connected
    # @param room
    #   The room which is check whether it is connected to
    #   this room.
    # @return
    #   Returns whether this room is connected to the passed in room.
    def isConnectedTo(self, room):
        return room.name in self.connectedRooms


## ## Tests all of the functionality in Room
class TestRoom(unittest.TestCase):
    def setUp(self):
        self.room = Room("testRoom")

    def testInitCorrect(self):
        room = Room("testRoom")
        self.assertEqual(room.name, "testRoom")
        self.assertFalse(room.getConnectedRooms())

    def testInitIncorrect(self):
        with self.assertRaises(TypeError):
            Room(None)

    def testAddMember(self):
        self.room.addMember('Jim')
        self.assertTrue('Jim' in self.room.people)

    def testAddMemberAlreadyThere(self):
        self.room.addMember('Jim')
        with self.assertRaises(AlreadyInRoomError):
            self.room.addMember('Jim')

    def testRemoveMember(self):
        self.room.addMember('Jim')
        self.room.removeMember('Jim')
        self.assertFalse('Jim' in self.room.people)

    def testRemoveMemberNotInRoom(self):
        with self.assertRaises(NotInRoomError):
            self.room.removeMember('Jim')

    def testAddResource(self):
        self.room.addResource('food')
        self.assertTrue(self.room.isAvailable('food'))

    def testAddResourceAlreadyAdded(self):
        self.room.addResource('food')
        with self.assertRaises(AlreadyAvailableError):
            self.room.addResource('food')

    def testRemoveResource(self):
        self.room.addResource('food')
        self.room.removeResource('food')
        self.assertFalse(self.room.isAvailable('food'))

    def testRemoveResourceNotAvailable(self):
        with self.assertRaises(NotAvailableError):
            self.room.removeResource('food')

    def testConnectAValidRoom(self):
        roomTwo = Room("testRoom2")
        self.room.connectToRoom(roomTwo)
        self.assertListEqual(self.room.getConnectedRooms(), [roomTwo.name])

    def testConnectARoomAlreadyConnected(self):
        roomTwo = Room("testRoom2")
        self.room.connectToRoom(roomTwo)
        with self.assertRaises(AlreadyConnectedError):
            self.room.connectToRoom(roomTwo)

    def testDisconnectRoom(self):
        roomTwo = Room("testRoom2")
        self.room.connectToRoom(roomTwo)
        self.room.disconnectRoom(roomTwo)
        self.assertFalse(self.room.getConnectedRooms())

    def testDisconnectNotConnectedRoom(self):
        roomTwo = Room("testRoom2")
        with self.assertRaises(NotConnectedError):
            self.room.disconnectRoom(roomTwo)

    def testIsConnectedToActuallyConnected(self):
        roomTwo = Room("testRoom2")
        self.room.connectToRoom(roomTwo)
        self.assertTrue(self.room.isConnectedTo(roomTwo))

    def testIsConnectedNotConnected(self):
        roomTwo = Room("testRoom2")
        self.assertFalse(self.room.isConnectedTo(roomTwo))

if __name__ == "__main__":
    unittest.main()
