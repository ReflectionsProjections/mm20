import unittest
import ai
import team_member


## This class represents a team competing in the game.
class Team(object):
    ## Initialize a Team
    # @param name
    #   The name of the Team
    # @param members
    #   The members of the Team (should be a list of dicts with name and class)
    # @param startingLocation
    #   The starting location of members
    # @param people
    #   A global list of people that the game stores and the team initializer
    #   appends all members to
    def __init__(self, name, members, startingLocation, people):
        self.name = name
        self.members = dict()
        #TODO: limit the number of team members one team can have, and throw/catch an appropriate exception
        for member in members:
            newMember = (team_member.TeamMember(member["name"], member["class"], startingLocation, self, len(people)))
            #TODO: check for non-unique names, then throw/catch an appropriate exception
            self.members[member["name"]] = newMember
            people.append(newMember)
        self.numMembers = len(members)
        self.ai = ai.AI()

    ## returns a serializable representation of what the player sees
    def get_visible_map(self):
        rooms = dict()
        for m in self.members.values():
            room = m.location
            rooms[room.name] = room
        return [r.output_dict() for r in rooms.values()]


class TestTeam(unittest.TestCase):
    def setUp(self):
        self.team = Team("testTeam",
                         [
                             {"name": "Steve", "class": "Coder"},
                             {"name": "Bob", "class": "Theorist"}
                         ], "Narnia", [])

    def testInit(self):
        self.assertEqual(self.team.name, "testTeam")
        self.assertIn("Steve", self.team.members)
        self.assertIn("Bob", self.team.members)
        self.assertEqual(self.team.numMembers, 2)

if __name__ == "__main__":
    unittest.main()
