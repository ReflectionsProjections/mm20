import unittest
import client_action
## Manages "rooms" which are nodes on our locations graph.
#  Hallways are also "rooms" in this sense.
#  Rooms contain team members, chairs, standing spots,
#  and possibly snack tables and projectors.
class Room(object):
    ## Initializes a Room object.
    # @param name
    #   The identifier of the room.
    # @param furniture
    #   Test
    def __init__(self, room_id):
        if room_id is None:
            raise TypeError(
                "Attempted to initialize Room with room_id of None")
        self.connectedRooms = dict()
        self.name = room_id
        self.people = set() # All people in the room
        self.sitting = set() # People sitting in the room
        self.resources = set()
        self.chairs = list() # All chairs in the room
        self.stand = list() # All standing positions in the room
        self.desks = list()
        self.doors = list()
        self.snacktable = list()
        self.dirmarkers = list()
        self.paths = None

    ## Adds a member to this room
    # @param member
    #   The member to add to this room
    def addMember(self, member):
        if member in self.people:
            raise client_action.ActionError(
                "ALREADYINROOM",
                "Cannot move to destination, you are in the room already")
        additionalpeople = 0
        if "PROFESSOR" in self.resources:
            additionalpeople += 1
        if len(self.people) + 1 + additionalpeople > len(self.chairs + self.stand):
            raise client_action.ActionError(
                "ROOMISFULL",
                "Cannot move to destination, it is full.")
        self.people.add(member)
        member.sitting = False
        
    ## Removes a member from this room
    # @param member
    #   The member to remove from this room
    def removeMember(self, member):
        if not member in self.people:
            raise client_action.ActionError(
                "NOTINROOM",
                "This person is not in this room")
        self.people.remove(member)
        if member in self.sitting:
            self.sitting.remove(member)
            member.sitting = False

    ## This person is trying to sit down
    # @param member
    #   The member trying to sit
    def sitDown(self, member):
        if not member in self.people:
            raise client_action.ActionError(
                "NOTINROOM",
                "This person is not in this room")
        elif len(self.sitting) + 1 > len(self.chairs):
            return
        elif not member in self.sitting:
            self.sitting.add(member)
            member.sitting = True

    ## This person is trying to stand up
    # @param member
    #   The member trying to stand
    def standUp(self, member):
        if not member in self.people:
            raise client_action.ActionError(
                "NOTINROOM",
                "This person is not in this room")
        if member in self.sitting:
            self.sitting.remove(member)
            member.sitting = False

    ## Make a resource available in this room
    # @param resource
    #   the resource to make available as a string.
    def addResource(self, resource):
        self.resources.add(resource)

    ## Remove a resource from a this room
    # @parameter resource
    #   The resource to remove from this room
    def removeResource(self, resource):
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
        room_info = {
            "room": self.name,
            "connectedRooms": self.connectedRooms.keys(),
            "peopleInRoom": [p.person_id for p in self.people],
            "resources": [resource for resource in self.resources],
            "seatsTotal": len(self.chairs),
            "standsTotal": len(self.stand),
            "seatsAvailable": len(self.chairs) - len(self.sitting),
            "standsAvailable": len(self.stand) - (len(self.people) - len(self.sitting))
        }
        return room_info

    ## Returns connected rooms
    def getConnectedRooms(self):
        return self.connectedRooms.keys()

    ## Connects one room to another
    # @param room
    #   The room to connect to this room
    def connectToRoom(self, room):
        self.connectedRooms[room.name] = room
        room.connectedRooms[self.name] = self

    ## Disconnects two rooms
    # @param room
    #   The room to disconnect from this room
    def disconnectRoom(self, room):
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

    ## Reports whether there are room for the specified number of people in the room
    # @param num_people
    #   The number of people to add to the room
    # @return
    #   boolean value stating whether adding them is possible or not
    def canAdd(self, num_people):
        return num_people <= len(self.stand) + len(self.chairs) - len(self.people)

class TestRoom(unittest.TestCase):
    def setUp(self):
        from objects.team_member import TeamMember
        self.room = Room("testRoom")
        self.room.chairs = [(1,1), (2,2), (3,3)]
        self.room.stand = [(4,4), (5,5), (6,6)]
        self.team_member = TeamMember("Joe", "Coder", self.room, None, 0)

    def testInitCorrect(self):
        room = Room("testRoom")
        self.assertEqual(room.name, "testRoom")
        self.assertFalse(room.getConnectedRooms())

    def testInitIncorrect(self):
        with self.assertRaises(TypeError):
            Room(None)

    def testAddMember(self):
        self.assertTrue(self.team_member in self.room.people)

    def testAddMemberAlreadyThere(self):
        with self.assertRaises(client_action.ActionError):
            self.room.addMember(self.team_member)

    def testRemoveMember(self):
        self.room.removeMember(self.team_member)
        self.assertFalse(self.team_member in self.room.people)

    def testRemoveMemberNotInRoom(self):
        with self.assertRaises(client_action.ActionError):
            self.room.removeMember("Jim")

    def testAddResource(self):
        self.room.addResource('food')
        self.assertTrue(self.room.isAvailable('food'))

    def testRemoveResource(self):
        self.room.addResource('food')
        self.room.removeResource('food')
        self.assertFalse(self.room.isAvailable('food'))

    def testRemoveResourceNotAvailable(self):
        with self.assertRaises(KeyError):
            self.room.removeResource('food')

    def testConnectAValidRoom(self):
        roomTwo = Room("testRoom2")
        self.room.connectToRoom(roomTwo)
        self.assertListEqual(self.room.getConnectedRooms(), [roomTwo.name])

    def testDisconnectRoom(self):
        roomTwo = Room("testRoom2")
        self.room.connectToRoom(roomTwo)
        self.room.disconnectRoom(roomTwo)
        self.assertFalse(self.room.getConnectedRooms())

    def testDisconnectNotConnectedRoom(self):
        roomTwo = Room("testRoom2")
        with self.assertRaises(KeyError):
            self.room.disconnectRoom(roomTwo)

    def testIsConnectedToActuallyConnected(self):
        roomTwo = Room("testRoom2")
        self.room.connectToRoom(roomTwo)
        self.assertTrue(self.room.isConnectedTo(roomTwo))

    def testIsConnectedNotConnected(self):
        roomTwo = Room("testRoom2")
        self.assertFalse(self.room.isConnectedTo(roomTwo))

    def testRoomFull(self):
        from objects.team_member import TeamMember
        for i in range(1, len(self.room.chairs + self.room.stand)):
            TeamMember(str(i), "Coder", self.room, None, i)
        with self.assertRaises(client_action.ActionError):
            TeamMember("Jim", "Coder", self.room, None, 18)

    def testSit(self):
        self.room.sitDown(self.team_member)
        self.assertTrue(self.team_member.sitting)

    def testSitNoChairs(self):
        from objects.team_member import TeamMember
        for i in range(1, len(self.room.chairs + self.room.stand)):
            newmem = TeamMember(str(i), "Coder", self.room, None, i)
            self.room.sitDown(newmem)
        self.room.sitDown(self.team_member)
        self.assertFalse(self.team_member.sitting)

    def testStand(self):
        self.room.sitDown(self.team_member)
        self.assertTrue(self.team_member.sitting)
        self.room.standUp(self.team_member)
        self.assertFalse(self.team_member.sitting)

if __name__ == "__main__":
    unittest.main()
