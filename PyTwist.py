# PyTwist
# blaws, amarti36
# PyTwist.py

import sys
import pygame
from pygame.locals import *
from Runner import Runner
from Guardian import Guardian

class PyTwist:
    def __init__(self):
        pygame.init()
        self.size = self.width, self.height = 640, 480
        self.screen = pygame.display.set_mode(self.size)
        self.bg = pygame.image.load('images/Background.png').convert()
        self.reverse_bg = pygame.transform.flip(self.bg, True, False)
        self.bg_rect = self.bg.get_rect()
        self.bg_speed = 4
        pygame.display.set_caption('PyTwist')

    def main(self):
        # game objects
        self.clock = pygame.time.Clock()
        self.runner = Runner(self)
	self.guardian = Guardian(self)

        # game loop
        while 1:  # will be replaced by a function call later, to integrate with Twisted's event loop
            self.clock.tick(60)  # will be deleted when integrated with Twisted

            # handle input
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                elif event.type == KEYUP or event.type == KEYDOWN:
                    if event.key == K_q or event.key == K_ESCAPE:
                        sys.exit()
                    else:
                        self.runner.input(event)
			self.guardian.input(event)

            # iterate game objects
            self.runner.tick(self.guardian.rect)
            self.guardian.tick()
            self.move_background()

            # display
            self.screen.blit(self.bg, self.bg_rect)
            if self.bg_rect.right < self.width:
                self.screen.blit(self.reverse_bg, self.bg_rect.move(self.width, 0))
            else:
                self.screen.blit(self.reverse_bg, self.bg_rect.move(-self.width, 0))
	    self.screen.blit(self.guardian.image, self.guardian.rect)
            self.screen.blit(self.runner.image, self.runner.rect)
            pygame.display.flip()

    def move_background(self):
        self.bg_rect = self.bg_rect.move(-self.bg_speed, 0)
        if self.bg_rect.right <= 0:
            self.bg_rect.left = self.width


if __name__ == '__main__':
    pt = PyTwist()
    pt.main()
