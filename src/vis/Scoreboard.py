import pygame
import time

class Scoreboard(object):

	def __init__(self, **kwargs):
		self.serverDefaults = retrieveConstants("serverDefaults")
        self.constants = retrieveConstants("visualizerDefaults")
        self.SCREEN_WIDTH = self.constants["SCREEN_WIDTH"]
        self.SCREEN_HEIGHT = self.constants["SCREEN_HEIGHT"]
        self.MAX_FPS = self.constants["MAX_FPS"]
        self.TITLE = "SCOREBOARD" #TODO: move to constants file
        self.running = True
        self.team_names = list()
        self.messages = list()
        self.game_done = False
        self.game_result = None
        self.debug = kwargs.get("debug", False)
        self.quitWhenDone = self.constants['QUIT_WHEN_DONE']

        pygame.init()
        self.setup()

    def setup(self):
    	pygame.display.set_caption(self.TITLE)
    	self.ScreenSurface = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
    	self.GameClock = pygame.time.Clock()

    # SAM!
    # This is blindly pasted from visualizer. It looks like it should work, but check it for me?
    def run_from_file(self, file_name=""):

        # Load game log
        json_file = None
        try:
            json_file = open(file_name)
        except:
            self.running = False
            print "ERROR: Invalid game logfile."
            return

        # Run the game
        for turn_str in json_file:
            self.test(turn_str)
            turn_count += 1

        # If game is done and we're supposed to quit on exit, wait a while then exit
        if self.quitWhenDone:
            print "Game done; exiting"
            time.sleep(5)
            pygame.quit()

    def turn(self, turn=None):
    	while self.running and self.update_state(json.loads(turn)):
    		self.draw()

    def draw(self):
    	# TODO:
    	pass

    def update_state(self, turn):
        # Check to see if the game has ended
        firstTurn = next(t for t in turn if t)
        if "winner" in firstTurn:
            self.game_done = True
            self.game_result = turn
            return not self.quitWhenDone
        if "team_name" in firstTurn:
            self.add_teams(turn)
            return False

        return True