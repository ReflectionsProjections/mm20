class Team(object):

    #Attributes
    # teamName = ""
    # color = ""
    # members = []
    # numMembers = 0
    teamCount = 0

    def __init__(self,teamName,members):
        self.teamName = teamName
        self.members = members
        self.numMembers = len(members)
        self.teamNum = Team.teamCount
        Team.teamCount += 1


#Test
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