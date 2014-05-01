# PyTwist
# blaws, amarti36
# PyTwist.py

import sys
import pygame
from pygame.locals import *
from Runner import Runner

class PyTwist:
    def __init__(self):
        pygame.init()
        self.size = self.width, self.height = 640, 480
        self.screen = pygame.display.set_mode(self.size)
        self.background = 0, 0, 0
        pygame.display.set_caption('PyTwist')

    def main(self):
        # game objects
        self.clock = pygame.time.Clock()
        self.runner = Runner(self)

        # game loop
        while 1:  # will be replaced by a function call later, to integrate with Twisted's event loop
            self.clock.tick(60)  # will be deleted when integrated with Twisted

            # handle input
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_q or event.key == K_ESCAPE:
                        sys.exit()

            # iterate game objects

            # display
            self.screen.fill(self.background)
            pygame.display.flip()


if __name__ == '__main__':
    pt = PyTwist()
    pt.main()
