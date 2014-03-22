from objects.room import Room
from objects.team import Team
from objects.team_member import TeamMember
from map_functions import getRoomsFromMap as map_reader

class Game(object):

    def __init__(self, file_url):
        """
        This is called once to init the server
        the map reader will return a list of rooms that have been
        linked together as defined in the design doc.
        """
        self.rooms = map_reader(file_url)
        self.turn = 0
        
    def add_new_team(self):
        pass

    def execute_turn(self):
        pass

    def queue_turn(self, action_list, player_id):
        error_list = []
        return error_list

    def get_info(self, player_id):
        return {"warnings": [], "map": []}