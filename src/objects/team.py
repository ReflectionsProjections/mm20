from unittest import TestCase, main
from ai import AI
from team_member import TeamMember


## This class represents a team competing in the game.
class Team(object):
    ## Initialize a Team
    # @param name
    #   The name of the Team
    # @param members
    #   The members of the Team (should be a list of dicts with name and class)
    # @param startingLocation
    #   The starting location of members
    def __init__(self, name, members, startingLocation):
        self.name = name
        self.members = dict()
        for member in members:
            self.members[member["name"]] = (TeamMember(member["name"], member["class"], startingLocation, self))
        self.numMembers = len(members)
        self.ai = AI()


class TestTeam(TestCase):
    def setUp(self):
        self.team = Team("testTeam",
                         [
                             {"name": "Steve", "class": "Aristocrat"},
                             {"name": "Bob", "class": "Commoner"}
                         ], "Narnia")

    def testInit(self):
        self.assertEqual(self.team.name, "testTeam")
        self.assertIn("Steve", self.team.members)
        self.assertIn("Bob", self.team.members)
        self.assertEqual(self.team.numMembers, 2)

if __name__ == "__main__":
    main()
