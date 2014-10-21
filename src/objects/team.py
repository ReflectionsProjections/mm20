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
    def __init__(self, name, members, startingLocation, people, my_id, ticks):
        self.name = name
        self.my_id = my_id
        self.members = dict()
        for member in members:
            newMember = team_member.TeamMember(member["name"],
                                               member["archetype"],
                                               startingLocation, self,
                                               len(people), ticks)
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
        return {k: r.output_dict() for k, r in rooms.items()}

    ## Returns a list of serializeable dictionaries of all of
    #  the team members on this team
    def get_team_members(self):
        return {k: m.output_dict() for k, m in self.members.items()}

    def get_info_on_people(self, people_list):
        output = {}
        for p in people_list:
            if p.team == self:
                output[p.person_id]=p.output_dict()
            else:
                same_room = False
                for person in p.location.people:
                    if person.team == self:
                        same_room = True
                        break
                if same_room:
                    output[p.person_id]=p.output_dict_same_room()
                else:
                    output[p.person_id]=p.output_dict_limited()
        return output

import room


class TestTeam(unittest.TestCase):
    def setUp(self):
        self.testRoom = room.Room("Narnia")
        self.testRoom.stand = [(4,4), (5,5), (6,6)]
        self.team = Team("testTeam",
                         [
                             {"name": "Steve", "archetype": "Coder"},
                             {"name": "Bob", "archetype": "Theorist"}
                         ], self.testRoom, [], 0)

    def testInit(self):
        self.assertEqual(self.team.name, "testTeam")
        self.assertIn("Steve", self.team.members)
        self.assertIn("Bob", self.team.members)
        self.assertEqual(self.team.numMembers, 2)

if __name__ == "__main__":
    unittest.main()
