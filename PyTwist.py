# PyTwist
# blaws, amarti36
# PyTwist.py

import sys
from twisted.internet import reactor
from twisted.internet.task import LoopingCall
import pygame
from pygame.locals import *
from Guardian import *
from Runner import *
from Connection import *
from Platform import *

class PyTwist:
    def __init__(self):
        pygame.init()
        self.connection = None
        self.side = None
        self.size = self.width, self.height = 640, 480
        self.screen = pygame.display.set_mode(self.size)
        self.bg = pygame.image.load('images/Background.png').convert()
        self.reverse_bg = pygame.transform.flip(self.bg, True, False)
        self.bg_rect = self.bg.get_rect()
        self.bg_speed = 4
        pygame.display.set_caption('PyTwist')

        # create game objects
        self.clock = pygame.time.Clock()
        self.runner = Runner(self)
	self.guardian = Guardian(self)
	self.platforms = list()

    def connect(self, side, port, addr=None):
        self.side = side
        if side == 0:
            reactor.listenTCP(port, ConnectionFactory(self))
        if side == 1:
            reactor.connectTCP(addr, port, ConnectionClientFactory(self))

    def printerror(self, error):
        print error
        reactor.stop()

    def start(self):
        self.gameloop = LoopingCall(self.main).start(1/float(60))
        reactor.run()

    def main(self):  # pygame loop - called by Twisted's event loop
        # handle input
        for event in pygame.event.get():
            if event.type == QUIT:
                reactor.stop()
            elif event.type == KEYUP or event.type == KEYDOWN:
                if event.key == K_q or event.key == K_ESCAPE:
                    reactor.stop()
                else:
                    if self.side == 0:
                        self.runner.input(event)
                    elif self.side == 1:
                        self.guardian.input(event)

        # iterate game objects
        self.runner.tick()
        self.guardian.tick()
	for platform in self.platforms:
		platform.tick()
        self.move_background()

        # update other player
        if self.connection:
            self.connection.sendUpdate()

        # display
        self.screen.blit(self.bg, self.bg_rect)
        if self.bg_rect.right < self.width:
            self.screen.blit(self.reverse_bg, self.bg_rect.move(self.width, 0))
        else:
            self.screen.blit(self.reverse_bg, self.bg_rect.move(-self.width, 0))
        self.screen.blit(self.guardian.image, self.guardian.rect)
        self.screen.blit(self.runner.image, self.runner.rect)
	for platform in self.platforms:
		self.screen.blit(platform.image, platform.rect)
        pygame.display.flip()

    def move_background(self):
        self.bg_rect = self.bg_rect.move(-self.bg_speed, 0)
        if self.bg_rect.right <= 0:
            self.bg_rect.left = self.width


if __name__ == '__main__':
    if (len(sys.argv)!=3 and len(sys.argv)!=4) or (sys.argv[1].lower()!='runner' and sys.argv[1].lower()!='guardian'):
        print 'usage: python '+sys.argv[0]+' <runner/guardian> <port> <hostname (guardian only)>'
        sys.exit(1)

    pt = PyTwist()

    if sys.argv[1].lower() == 'runner':
        pt.connect(0, int(sys.argv[2]))
    elif sys.argv[1].lower() == 'guardian' and len(sys.argv) > 3:
        pt.connect(1, int(sys.argv[2]), sys.argv[3])

    pt.start()
