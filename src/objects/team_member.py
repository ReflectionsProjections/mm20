import config.handle_constants
import unittest
import math


## Holds information and functions for individual team members
class TeamMember(object):
    _INVALID = "Invalid Request"
    Archetypes = config.handle_constants.retrieveConstants("archetypes")
    ticks_in_hour = config.handle_constants.retrieveConstants("generalInfo")["TICKSINHOUR"]
    effectiveness_drops = 60.0

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
        self.hunger = 0
        self.fatigue = 50.0 #Start at 8 hours awake (halfway to passed out)
        self.asleep = False
        self.acted = False

    def output_dict(self):
        my_info = dict(self.__dict__)
        del my_info["team"]
        my_info["location"] = self.location.name
        return my_info
        
    ## Moves the team member from one room to another.
    # @param destination
    #   The room (a Room object) to move to.
    def move(self, destination):
        if not self.acted and not self.asleep:
            if not self.location.isConnectedTo(destination):
                raise ValueError(
                    "NOTCONNECTED",
            "Cannot move to destination, it is not connected to current location")
            else:
                self.location = destination
            self.acted = True
        else:
            pass #TODO: throw errors

    ## The team member sleeps for some time to regain energy.
    #  The amount of energy regained depends on their Archetype
    # @param turns
    #   The number of turns the team member sleeps for.
    def sleep(self):
        if not self.acted and self.hunger < 100:
            self.asleep = True
        else:
            pass #TODO: throw errors

    ##  Code!
    #
    #   @param code_type A string containing the type of coding to be done
    #   @param turn The turn so that the player knows how long they've been coding
    def code(self, code_type, turn):
        if not self.acted and not self.asleep and self.hunger < 100:
            ai = self.team.ai
            effective = self._getEffectiveness()
            if code_type == "refactor":
                ai.complexity -= effective * self.archetype["refactor"]
                if ai.complexity < ai.implementation * .25:
                    ai.complexity = ai.implementation * .25
                if ai.complexity < 1:
                    ai.complexity = 1.0
            elif code_type == "test":
                amount = effective * self.archetype["test"] / (ai.complexity / 10.0)
                ai.stability += amount / 100.0
                if ai.stability > 1:
                    ai.stability = 1.0
            elif code_type == "implement":
                amount = effective * self.archetype["codingProwess"] / (ai.complexity / 10.0)
                ai.implementation += amount
                ai.complexity += amount
                ai.optimization -= amount / 10.0
                ai.stability -= amount / 200.0
                if ai.implementation > ai.theory:
                    ai.implementation = ai.theory
                if ai.stability < 0.0:
                    ai.stability = 0.0
                if ai.optimization < 0.0:
                    ai.optimization = 0.0
            elif code_type == "optimize":
                amount = effective * self.archetype["optimize"] / (ai.complexity / 10.0)
                ai.complexity += amount
                ai.optimization += amount
            self.acted = True
        else:
            pass #TODO: throw errors

    ##  Theorize!
    #
    #   @param turn The turn so that the player knows how long they've been theorizing
    def theorize(self, turn):
        if not self.acted and not self.asleep and self.hunger < 100:
            effective = self._getEffectiveness()
            self.team.ai.theory += self.archetype["theorize"] * effective
            self.acted = True
        else:
            pass #TODO: Throw error

    ##Calculate effectiveness based on fatigue and hunger
    def _getEffectiveness(self):
        effective = 1.0
        if self.hunger > TeamMember.effectiveness_drops:
            effective -= 0.5 * (100-self.hunger) / (100-TeamMember.effectiveness_drops)
        if self.fatigue > TeamMember.effectiveness_drops:
            effective -= 0.5 * (100-self.fatigue) / (100-TeamMember.effectiveness_drops)
        return effective

    ##  Called every turn to reset values and make incremental changes
    def update(self):
        if not self.asleep:
            self.hunger += 100.0 / (8.0 * TeamMember.ticks_in_hour)
            self.fatigue += 100.0 / (16.0 * TeamMember.ticks_in_hour)
            if self.hunger > 100:
                self.hunger = 100.0
            if self.fatigue > 100:
                self.asleep = True
        else:
            self.hunger += 100.0 / (16.0 * TeamMember.ticks_in_hour)
            self.fatigue -= 100.0 / (8.0 * TeamMember.ticks_in_hour)
            if self.hunger > 100:
                self.hunger = 100.0
                self.asleep = False
        self.acted = False


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
        self.testMember = TeamMember("Joe", "Coder", self.testRoom,
                                     self.testTeam, 0)

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
