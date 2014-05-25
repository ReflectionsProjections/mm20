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
    def __init__(self, name, members, startingLocation, people, my_id):
        self.name = name
        self.my_id = my_id
        self.members = dict()
        for member in members:
            newMember = team_member.TeamMember(member["name"],
                                               member["archetype"],
                                               startingLocation, self,
                                               len(people))
            self.members[member["name"]] = newMember
            people.append(newMember)
        self.numMembers = len(members)
        self.ai = ai.AI()

    ## returns a serializable representation of what the player sees
    def get_visible_map(self):
        rooms = dict()
        for m in self.members.values():
            visible_room = m.location
            rooms[visible_room.name] = visible_room
        return [r.output_dict() for r in rooms.values()]

    ## Returns a list of serializeable dictionaries of all of
    #  the team members on this team
    def get_team_members(self):
        return [m.output_dict() for m in self.members.values()]

    def get_info_on_people(self, people_list):
        return [p.output_dict() if p.team.my_id == self.my_id
                else p.output_dict_limited() for p in people_list]

import room


class TestTeam(unittest.TestCase):
    def setUp(self):
        self.testRoom = room.Room("Narnia")
        self.team = Team("testTeam",
                         [
                             {"name": "Steve", "class": "Coder"},
                             {"name": "Bob", "class": "Theorist"}
                         ], self.testRoom, [], 0)

    def testInit(self):
        self.assertEqual(self.team.name, "testTeam")
        self.assertIn("Steve", self.team.members)
        self.assertIn("Bob", self.team.members)
        self.assertEqual(self.team.numMembers, 2)

if __name__ == "__main__":
    unittest.main()
