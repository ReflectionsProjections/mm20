from unittest import TestCase, main
from ai import AI
from team_member import TeamMember


## This class represents a team competing in the game.
class Team(object):

    # Attributes:
    #   teamName = ""
    #   color = ""
    #   members = []
    #   numMembers = 0

    ## Initialize a Team
    # @param teamName The name of the Team
    # @param members The members of the Team (should be a list of dicts with name and class)
    # @param location The starting location of members
    def __init__(self, teamName, members, location):
        self.teamName = teamName
        self.color = ""
        self.members = []
        for m in members:
            self.members.append(TeamMember(m["name"], m["class"], location, self))
        self.numMembers = len(members)
        self.ai = AI()


class TestTeam(TestCase):
    def setUp(self):
        pass

    def test_(self):
        pass

    def test_2(self):
        pass

if __name__ == "__main__":
    EightBL = Team("teamName", ["Hello", "Goodbye"])
    print EightBL.teamName
    print EightBL.members[0]
    print EightBL.numMembers
    print EightBL.teamNum

    NineBL = Team("fdjaklfasjlkfajlfk", ["What?", "jfkdaljfla"])
    print NineBL.teamName
    print NineBL.members[0]
    print NineBL.numMembers
    print NineBL.teamNum

    main()
