import pygame


class Animation(object):

    def __init__(self, color, visualizer):
        self.color = color
        self.animations = {}
        self.ScreenSurface = visualizer.ScreenSurface
        self.scale = visualizer.scale
        
        self.constants = visualizer.constants
        for a_type in self.constants["animations"]:
            self.animations[a_type] = []
            # self.animations[a_type] = a list of frames
            for i, frame_name in enumerate(self.constants["animations"][a_type]):
                image = pygame.image.load(frame_name).convert_alpha()
                self.animations[a_type].append(self.colorize(image, color))

        # Colorize all the frames

    def colorize(self, image, color):
        teamImage = image.copy()
        pygame.PixelArray(teamImage).replace(pygame.Color(255, 0, 255, 255), color)
        return teamImage

    def draw(self, person, frame, a_type):
        scale_pos = self.scale((person.pos[0], person.pos[1]))
        self.ScreenSurface.blit(self.animations["STAND"][0], [p - 16 for p in scale_pos])
        