import config.handle_constants
import unittest


## Holds information and functions for individual team members
class TeamMember(object):
    _INVALID = "Invalid Request"
    Archetypes = config.handle_constants.retrieveConstants("archetypes")

    ## Initializes a TeamMember with name, archetype, and team
    # @param name
    #   The name of the TeamMember.
    # @param archetype
    #   The archetype of the TeamMember.
    # @param location
    #   The location (a Room object) that the TeamMember will start in.
    def __init__(self, name, archetype, location, team, person_id):
        self.name = name
        self.archetype = TeamMember.Archetypes[archetype]
        self.location = location
        self.team = team
        self.person_id = person_id
        self.energy = TeamMember.Archetypes[archetype]["energy"]

    ## Moves the team member from one room to another.
    # @param destination
    #   The room (a Room object) to move to.
    def move(self, destination):
        pass  # TODO

    ## The team member sleeps for some time to regain energy.
    #  The amount of energy regained depends on their Archetype
    # @param turns
    #   The number of turns the team member sleeps for.
    def sleep(self, turns):
        pass  # TODO


import team
import room


## Tests all of the functionality in Team Member
class TestTeamMember(unittest.TestCase):
    def setUp(self):
        class PseudoTeam(team.Team):
            def __init__(self):
                pass
        TestTeamMember.PseudoTeam = PseudoTeam
        self.testRoom = room.Room("testRoom")
        self.testTeam = TestTeamMember.PseudoTeam()
        self.testMember = TeamMember("Joe", "Coder", self.testRoom, self.testTeam, 0)

    def testInitCorrect(self):
        testRoom = room.Room("testRoom")
        testTeam = TestTeamMember.PseudoTeam()
        testMember = TeamMember("Joe", "Coder", testRoom, testTeam, 0)
        self.assertEqual(testMember.name, "Joe")
        self.assertEqual(testMember.archetype, TeamMember.Archetypes["Coder"])
        self.assertEqual(testMember.location, testRoom)
        self.assertEqual(testMember.team, testTeam)

    def testInitNotARoom(self):
        testTeam = TestTeamMember.PseudoTeam()
        with self.assertRaises(TypeError):
            TeamMember("Joe", "Coder", "NotARoom", testTeam)

    def testInitNotATeam(self):
        testRoom = room.Room("testRoom")
        with self.assertRaises(TypeError):
            TeamMember("Joe", "Coder", testRoom, "NotATeam")

    def testInitIncorrectArchetype(self):
        testRoom = room.Room("testRoom")
        testTeam = TestTeamMember.PseudoTeam()
        with self.assertRaises(KeyError):
            TeamMember("Joe", "NotAnArchetype", testRoom, testTeam, 0)

    def testInitNotAName(self):
        testRoom = room.Room("testRoom")
        testTeam = TestTeamMember.PseudoTeam()
        with self.assertRaises(KeyError):
            TeamMember(None, "NotAnArchetype", testRoom, testTeam, 0)

    def testValidMove(self):
        roomTwo = room.Room("testRoomTwo")
        self.testRoom.connectToRoom(roomTwo)
        self.testMember.move(roomTwo)
        self.assertEquals(self.testMember.location, roomTwo)

    def testInvalidMove(self):
        roomTwo = room.Room("testRoomTwo")
        with self.assertRaises(ValueError):
            self.testMember.move(roomTwo)

    def testMoveNotARoom(self):
        with self.assertRaises(TypeError):
            self.testMember.move("NotARoom")

    def testSleep(self):
        energy = self.testMember.energy
        self.testMember.sleep(10)
        self.assertEqual(self.testMember.energy, energy + 10 * TeamMember.Archetypes["Coder"]["sleepEffectiveness"])

if __name__ == "__main__":
    unittest.main()
