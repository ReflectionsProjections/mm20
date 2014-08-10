import config.handle_constants
import client_action
import unittest


## Holds information and functions for individual team members
class TeamMember(object):
    Archetypes = config.handle_constants.retrieveConstants("archetypes")
    ticks_in_hour = config.handle_constants.retrieveConstants("generalInfo")[
        "TICKSINHOUR"]
    effectiveness_drops = config.handle_constants.retrieveConstants(
        "memberConstants")["effectiveness_drops"]

    ## Initializes a TeamMember with name, archetype, and team
    # @param name
    #   The name of the TeamMember.
    # @param archetype
    #   The archetype of the TeamMember.
    # @param location
    #   The location (a Room object) that the TeamMember will start in.
    def __init__(self, name, archetype, location, team, person_id):
        constants = config.handle_constants.retrieveConstants(
            "memberConstants")
        self.person_id = person_id
        self.name = name
        self.stats = TeamMember.Archetypes[archetype]
        self.archetype = archetype
        self.location = location
        self.position = None
        location.addMember(self)
        self.team = team
        self.hunger = constants["hunger"]
        self.fatigue = constants["fatigue"]  # Start at 8 hours awake
            # (halfway to passed out)
        self.asleep = False
        self.acted = None  # acted is the string of the action performed.
                           # (True) or None (False)

    ## Each person should have a unique person_id that will never change once a
    #  person has been created.
    #  This makes the hash function dependent on the person_id
    def __hash__(self):
        return hash(self.person_id)

    ## Each person should have a unique person_id that will never change once a
    #  person has been created.
    #  This makes the hash function dependent on the person_id
    def __eq__(self, other):
        return self.person_id == other.person_id

    ## Make a seralible repesentaion of this team member and everything in it
    # @return
    #    A dict that reprents the team member
    def output_dict(self):
        my_info = dict(self.__dict__)
        my_info["team"] = self.team.my_id
        my_info["location"] = self.location.name
        return my_info

    ## Make a serializable repesentaion of this team member with limited in it
    # @return
    #    A dict that reprents the team member
    def output_dict_limited(self):
        my_info = dict()
        my_info["team"] = self.team.my_id
        my_info["person_id"] = self.person_id
        my_info["name"] = self.name
        self.asleep = False
        
        return my_info

    def output_dict_same_room(self):
        my_info = dict()
        my_info["team"] = self.team.my_id
        my_info["person_id"] = self.person_id
        my_info["name"] = self.name
        my_info["location"] = self.location.name
        my_info["acted"] = self.acted
        my_info["asleep"] = self.asleep
        self.asleep = False
        
        return my_info

    ## Moves the team member from one room to another.
    # @param destination
    #   The room (a Room object) to move to.
    def move(self, destination):
        if not self.acted and not self.asleep:
            if not self.location.isConnectedTo(destination):
                raise client_action.ActionError(
                    "NOTCONNECTED",
                    "Cannot move to destination, \
                    it is not connected to current location")
            else:
                self.location.removeMember(self)
                destination.addMember(self)
                self.location = destination
            self.acted = "move"
        else:
            if self.acted:
                if self.acted == "distracted":
                    raise client_action.ActionError(
                        "DISTRACTED",
                        "You have been distracted this turn")
                raise client_action.ActionError(
                    "ALREADYACTED",
                    "Cannot move to destination, \
                    this player has already acted this turn")
            if self.asleep:
                raise client_action.ActionError(
                    "ASLEEP",
                    "Cannot move to destination, this player is asleep")

    ## The team member sleeps for some time to regain energy.
    def sleep(self):
        self._can_move()
        self.asleep = True

    ##  Code!
    #
    #   @param code_type
    #     A string containing the type of coding to be done
    #   @param turn
    #     The turn so that the player knows how long they have been coding
    def code(self, code_type, turn):
        self._can_move()
        ai = self.team.ai
        effective = self._getEffectiveness()
        if code_type == "refactor":
            ai.complexity -= effective * self.stats["refactor"]
            ai.complexity = max(ai.complexity, ai.implementation * .25)
            ai.complexity = max(ai.complexity, 1.0)
        elif code_type == "test":
            amount = effective * self.stats["test"] /\
                (ai.complexity / 10.0)
            ai.stability += amount / 100.0
            ai.stability = min(ai.stability, 1.0)
        elif code_type == "implement":
            amount = effective * self.stats["codingProwess"] /\
                (ai.complexity / 10.0)
            ai.implementation += amount
            ai.implementation = min(ai.implementation, ai.theory)
            ai.complexity += amount
            ai.optimization -= amount / 10.0
            ai.optimization = max(ai.optimization, 0.0)
            ai.stability -= amount / 200.0
            ai.stability = max(ai.stability, 0.0)
        elif code_type == "optimize":
            amount = effective * self.stats["optimize"] /\
                (ai.complexity / 10.0)
            ai.complexity += amount
            ai.optimization += amount
        self.acted = "code"

    ##  Theorize!
    #
    #   @param turn
    #     The turn so that the player knows how long they've been theorizing
    def theorize(self, turn):
        self._can_move()
        effective = self._getEffectiveness()
        self.team.ai.theory += self.stats["theorize"] * effective
        self.acted = "theorize"

    ##  Eat!
    #
    #   @param foodTable ???
    def eat(self):
        if self.acted:
            raise client_action.ActionError(
                "ALREADYACTED",
                "This player has already acted this turn")
        if self.asleep:
            raise client_action.ActionError(
                "ASLEEP",
                "This player is asleep")
        if not self.location.isAvailable('FOOD'):
            raise client_action.ActionError('NOFOODHERE',
                                            "This room does not contain food")
        self.hunger -= 10.0 * (100.0 / (8.0 * TeamMember.ticks_in_hour))
        if self.hunger < 0.0:
            self.hunger = 0.0
        self.acted = "eat"
        self.position = self.location.snacktables[0]

    ##  Distract!
    #
    #   @param victim The person you are trying to distract
    def distract(self, victim):
        self._can_move()
        if victim.location != self.location:
            raise client_action.ActionError(
                "UNDISTRACTABLE",
                "Cannot distract someone who is in another room")
        if victim.asleep:
            raise client_action.ActionError(
                "UNDISTRACTABLE",
                "Cannot distract someone who is asleep")
        if victim.acted:
            raise client_action.ActionError(
                "UNDISTRACTABLE",
                "Distraction failed because they ignored you")
        if victim.hunger >= 100:
            raise client_action.ActionError(
                "UNDISTRACTABLE",
                "Cannot distract someone who is focused on food")
        victim.acted = "distracted"
        self.acted = "distract"

    ##  Spy!
    def spy(self):
        self._can_move()
        effective = self._getEffectiveness() * self.stats["spy"]
        amount = 0
        for person in self.location.people:
            if person.team != self.team:
                if person.acted == "theorize":
                    amount += 2 * effective
                if person.acted == "code":
                    amount += effective
        self.acted = "spy"

    ##  Wake up!
    #
    #   @param victim The person you are trying to wake up
    def wake(self, victim):
        self._can_move()
        if victim.location != self.location:
            raise client_action.ActionError(
                "CANNOTWAKE",
                "Cannot wake someone who is in another room")
        if not victim.asleep:
            raise client_action.ActionError(
                "CANNOTWAKE",
                "Cannot wake someone who is not asleep")
        victim.asleep = False
        self.acted = "wake"

    ## Calculate effectiveness based on fatigue and hunger
    def _getEffectiveness(self):
        effective = 1.0
        if self.hunger > TeamMember.effectiveness_drops:
            effective -= 0.5 * (100 - self.hunger) /\
                (100 - TeamMember.effectiveness_drops)
        if self.fatigue > TeamMember.effectiveness_drops:
            effective -= 0.5 * (100 - self.fatigue) /\
                (100 - TeamMember.effectiveness_drops)
        return effective

    def _can_move(self):
        if self.acted:
            if self.acted == "distracted":
                raise client_action.ActionError(
                    "DISTRACTED",
                    "You have been distracted this turn")
            raise client_action.ActionError(
                "ALREADYACTED",
                "This player has already acted this turn")
        if self.asleep:
            raise client_action.ActionError(
                "ASLEEP",
                "This player is asleep")
        if self.hunger >= 100:
            raise client_action.ActionError(
                "HUNGRY",
                "This player is too hungry to think about anything but food")

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


import team
import room


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
        self.assertEqual(testMember.archetype, "Coder")
        self.assertEqual(testMember.stats, TeamMember.Archetypes["Coder"])
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
        with self.assertRaises(client_action.ActionError):
            self.testMember.move(roomTwo)

    def testEat(self):
        self.testRoom.addResource('FOOD')
        self.testMember.hunger = 100
        self.testMember.eat()
        self.assertEqual(self.testMember.hunger,
                        (100.0 - 10.0 *
                            (100.0 / (8.0 * TeamMember.ticks_in_hour))))

    def testEatNoFood(self):
        with self.assertRaises(client_action.ActionError):
            self.testMember.eat()

    @unittest.skip("Not yet implemented")
    def testSleep(self):
        # TODO
        self.assertTrue(False)

    def testTooHungry(self):
        self.testMember.hunger = 100
        with self.assertRaises(client_action.ActionError):
            self.testMember.sleep()

    def testAsleep(self):
        self.testRoom.addResource('FOOD')
        self.testMember.asleep = True
        with self.assertRaises(client_action.ActionError):
            self.testMember.eat()


if __name__ == "__main__":
    unittest.main()
