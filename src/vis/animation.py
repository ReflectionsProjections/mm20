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

    def rot_center(self, image, angle):
        """rotate an image while keeping its center and size"""
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

    def draw(self, person, frame, ):
        scale_pos = self.scale((person.pos[0], person.pos[1]))
        if person.action == "move":
            if person.pos[0] - person.targetPos[0] > 1.0 or person.pos[1] - person.targetPos[1] > 1.0:
                rot_image = self.rot_center(self.animations["WALK"][(frame / 4) % 4], person.rotation)
                self.ScreenSurface.blit(rot_image, [p - 16 for p in scale_pos])
            else:
                rot_image = self.rot_center(self.animations["STAND"][0], person.rotation)
                self.ScreenSurface.blit(rot_image, [p - 16 for p in scale_pos])
        elif person.action == "spy":
            if frame % 40 < 20:
                rot_image = self.rot_center(self.animations["SPY"][2], person.rotation + frame)
            if frame % 40 >= 20:
                rot_image = self.rot_center(self.animations["SPY"][2], person.rotation + (40 - frame))
            self.ScreenSurface.blit(rot_image, [p - 16 for p in scale_pos])
        elif person.action == "view":
            rot_image = self.rot_center(self.animations["SPY"][2], person.rotation)
            self.ScreenSurface.blit(rot_image, [p - 16 for p in scale_pos])
        elif person.action == "eat":
            rot_image = self.rot_center(self.animations["EAT"][(frame / 4) % 3], person.rotation)
            self.ScreenSurface.blit(rot_image, [p - 16 for p in scale_pos])
        elif person.action == "sleep" or person.asleep:
            rot_image = self.rot_center(self.animations["SLEEP"][0], person.rotation)
            self.ScreenSurface.blit(rot_image, [p - 16 for p in scale_pos])
        else:
            rot_image = self.rot_center(self.animations["STAND"][0], person.rotation)
            self.ScreenSurface.blit(rot_image, [p - 16 for p in scale_pos])
        if person.action == "code":
            self.ScreenSurface.blit(self.animations["CODE"][0], [scale_pos[0] - 8, scale_pos[1] - 48])
        elif person.action == "theorize":
            self.ScreenSurface.blit(self.animations["THEORIZE"][0], [scale_pos[0] - 8, scale_pos[1] - 48])
        elif person.action == "sleep" or person.asleep:
            self.ScreenSurface.blit(self.animations["SLEEP"][1], [scale_pos[0] - 8, scale_pos[1] - 48])
        elif person.action == "distract":
            self.ScreenSurface.blit(self.animations["DISTRACT"][0], [scale_pos[0] - 8, scale_pos[1] - 48])
        elif person.isDistracted:
            self.ScreenSurface.blit(self.animations["DISTRACTED"][0], [scale_pos[0] - 8, scale_pos[1] - 48])


            
            



"""        
 # Rotate an image while keeping its center and size
        # @source http://www.pygame.org/wiki/RotateCenter
        orig_rect = self.image.get_rect()
        rot_image = pygame.transform.rotate(self.image, rotation)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center

        # Update properties
        self.rotatedImage = rot_image.subsurface(rot_rect).copy()
"""        

        
