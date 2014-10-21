import config.handle_constants
import client_action
import unittest


## Holds information and functions for individual team members
class TeamMember(object):
    Archetypes = config.handle_constants.retrieveConstants("archetypes")
    constants = config.handle_constants.retrieveConstants(
            "memberConstants")
    effectiveness_drops = constants["effectiveness_drops"]
    coding_bonus = constants["coding_bonus"]
    turns_to_bonus = constants["turns_to_bonus"]

    ## Initializes a TeamMember with name, archetype, and team
    # @param name
    #   The name of the TeamMember.
    # @param archetype
    #   The archetype of the TeamMember.
    # @param location
    #   The location (a Room object) that the TeamMember will start in.
    def __init__(self, name, archetype, location, team, person_id, ticks):
        self.person_id = person_id
        self.name = name
        self.stats = TeamMember.Archetypes[archetype]
        self.archetype = archetype
        self.location = location
        self.sitting = False
        location.addMember(self)
        self.team = team
        self.turns_coding = 0
        self.hunger = TeamMember.constants["hunger"]
        self.fatigue = TeamMember.constants["fatigue"]  # Start at 8 hours awake
        self.ticks_in_hour = ticks
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

    ## Make a serializable repesentaion of this team member and everything in it
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
        
        return my_info

    def output_dict_same_room(self):
        my_info = dict()
        my_info["team"] = self.team.my_id
        my_info["person_id"] = self.person_id
        my_info["name"] = self.name
        my_info["location"] = self.location.name
        my_info["acted"] = self.acted
        my_info["asleep"] = self.asleep
        my_info["sitting"] = self.sitting
        
        return my_info

    ## Moves the team member from one room to another.
    # @param destination
    #   The room (a Room object) to move to.
    def move(self, destination):
        if not self.acted and not self.asleep:
            if not self.location.isConnectedTo(destination):
                raise client_action.ActionError(
                    "NOTCONNECTED",
                    "Cannot move to destination, it is not connected to current location")
            elif len(destination.people) + 1 > len(destination.chairs + destination.stand):
                raise client_action.ActionError(
                    "ROOMISFULL",
                    "Cannot move to destination, it is full.")
            else:
                destination.addMember(self)
                self.location.removeMember(self)
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
                    "Cannot move to destination, this player has already acted this turn")
            if self.asleep:
                raise client_action.ActionError(
                    "ASLEEP",
                    "Cannot move to destination, this player is asleep")

    ## The team member sleeps for some time to regain energy.
    def sleep(self):
        self._can_move()
        if self.sitting:
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
        roombonus = self.getRoomBonus(self.location)
        effectmod = 1.0
        if self.turns_coding < TeamMember.turns_to_bonus:
            self.turns_coding += 1
        if not self.sitting:
            effectmod = 0.5
        effective = roombonus * effectmod * self.getEffectiveness() * (TeamMember.coding_bonus * self.turns_coding / TeamMember.turns_to_bonus)
        if code_type == "refactor":
            ai.complexity -= effective * self.stats["refactor"]
            ai.complexity = max(ai.complexity, ai.implementation * .25)
            ai.complexity = max(ai.complexity, 1.0)
        elif code_type == "test":
            amount = effective * self.stats["test"] /\
                ((ai.complexity +1 ) / 10.0)
            ai.stability += amount / 100.0
            ai.stability = min(ai.stability, 1.0)
        elif code_type == "implement":
            amount = effective * self.stats["codingProwess"] /\
                ((ai.complexity + 1) / 10.0)
            ai.implementation += amount
            ai.implementation = min(ai.implementation, ai.theory)
            ai.complexity += amount
            ai.optimization -= amount / 10.0
            ai.optimization = max(ai.optimization, 0.0)
            ai.stability -= amount / 200.0
            ai.stability = max(ai.stability, 0.0)
        elif code_type == "optimize":
            amount = effective * self.stats["optimize"] /\
                ((ai.complexity +1) / 10.0)
            ai.complexity = min(amount + ai.complexity, ai.implementation)
            ai.optimization += amount
            ai.optimization = min(ai.optimization, ai.implementation)
        self.acted = "code"

    ##  Theorize!
    #
    #   @param turn
    #     The turn so that the player knows how long they've been theorizing
    def theorize(self, turn):
        self._can_move()
        roombonus = self.getRoomBonus(self.location)
        effectmod = 1.0
        if not self.sitting:
            effectmod = 0.5
        effective = effectmod * self.getEffectiveness() * roombonus
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
        self.hunger -= 10.0 * (100.0 / (8.0 * self.ticks_in_hour))
        if self.hunger < 0.0:
            self.hunger = 0.0
        self.acted = "eat"
        self.location.standUp(self)

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
        effective = self.getEffectiveness() * self.stats["spy"]
        amount = 0
        for person in self.location.people:
            if person.team != self.team:
                if person.acted == "theorize":
                    amount += 2 * effective
                if person.acted == "code":
                    amount += effective
        self.team.ai.theory += amount
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

    ##  View the projection in order to gain information about other teams
    def view(self):
        self._can_move()
        if not self.location.isAvailable('PROJECTOR'):
            raise client_action.ActionError('NOPROJECTOR',
                                            "This room does not have a projector!")
        if not self.location.isAvailable('PRACTICE'):
            raise client_action.ActionError('NOPRACTICE',
                                            "The projector is not currently running practice games.")
        self.acted = "view"

    ## Calculate effectiveness based on fatigue and hunger
    def getEffectiveness(self):
        effective = 1.0
        if self.hunger > TeamMember.effectiveness_drops:
            effective += -0.5 + 0.5 * (100 - self.hunger) /\
                (100 - TeamMember.effectiveness_drops)
        if self.fatigue > TeamMember.effectiveness_drops:
            effective += -0.5 + 0.5 * (100 - self.fatigue) /\
                (100 - TeamMember.effectiveness_drops)
        return effective

    ## Look at room resources and calculate room bonus
    def getRoomBonus(self, r):
        bonus = 1.0
        if "PROFESSOR" in r.resources:
            bonus += 1.0
        for person in r.people:
            if person != self and person.team == self.team:
                bonus += 0.1
        return bonus

    def _can_move(self):
        if self.acted != None:
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
        if self.acted != "code":
            self.turns_coding = 0
        if not self.asleep:
            self.hunger += 100.0 / (8.0 * self.ticks_in_hour)
            self.fatigue += 100.0 / (16.0 * self.ticks_in_hour)
            if self.hunger > 100:
                self.hunger = 100.0
            if self.fatigue > 100:
                self.asleep = True
        else:
            self.hunger += 100.0 / (16.0 * self.ticks_in_hour)
            timetoremovefatigue = 5.5 + .5 * len(self.location.people)
            if not self.sitting:
                timetoremovefatigue *= 2
            if "PROFESSOR" in self.location.resources:
                timetoremovefatigue = timetoremovefatigue/2
            if timetoremovefatigue > 12.0:
                timetoremovefatigue = 12.0
            self.fatigue -= 100.0 / (timetoremovefatigue * self.ticks_in_hour)
            self.fatigue = max(self.fatigue, 0.0)
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
        self.testRoom.stand = [(4,8), (4,7), (4,6)]
        self.testTeam = TestTeamMember.PseudoTeam()
        self.testMember = TeamMember("Joe", "Coder", self.testRoom,
                                     self.testTeam, 0, 60)

    def testInitCorrect(self):
        testRoom = room.Room("testRoom")
        testRoom.stand = [(4,8), (4,7), (4,6)]
        testTeam = TestTeamMember.PseudoTeam()
        testMember = TeamMember("Joe", "Coder", testRoom, testTeam, 0, 60)
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
            TeamMember("Joe", "NotAnArchetype", testRoom, testTeam, 0, 60)

    def testInitNotAName(self):
        testRoom = room.Room("testRoom")
        testTeam = TestTeamMember.PseudoTeam()
        with self.assertRaises(KeyError):
            TeamMember(None, "NotAnArchetype", testRoom, testTeam, 0, 60)

    def testValidMove(self):
        roomTwo = room.Room("testRoomTwo")
        roomTwo.stand.append((4,5))
        self.testRoom.connectToRoom(roomTwo)
        self.testMember.move(roomTwo)
        self.assertEquals(self.testMember.location, roomTwo)

    def testInvalidMove(self):
        roomTwo = room.Room("testRoomTwo")
        roomTwo.stand.append((4,5))
        with self.assertRaises(client_action.ActionError):
            self.testMember.move(roomTwo)

    def testRoomFull(self):
        roomTwo = room.Room("testRoomTwo")
        roomTwo.stand.append((4,5))
        with self.assertRaises(client_action.ActionError):
            self.testMember.move(roomTwo)

    def testEat(self):
        self.testRoom.addResource('FOOD')
        self.testMember.hunger = 100
        self.testMember.eat()
        self.assertEqual(self.testMember.hunger,
                        (100.0 - 10.0 *
                            (100.0 / (8.0 * 60))))

    def testEatNoFood(self):
        with self.assertRaises(client_action.ActionError):
            self.testMember.eat()

    def testSleep(self):
        self.testMember.asleep = True
        roomTwo = room.Room("testRoomTwo")
        roomTwo.stand.append((4,5))
        self.testRoom.connectToRoom(roomTwo)
        with self.assertRaises(client_action.ActionError):
            self.testMember.move(roomTwo)

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
