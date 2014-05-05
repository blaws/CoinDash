# PyTwist
# blaws, amarti36
# Runner.py

import pygame
from pygame.locals import *
from threading import Lock

class Runner(pygame.sprite.Sprite):
    def __init__(self, gs):
        pygame.sprite.Sprite.__init__(self)
        self.gs = gs
        self.jumpvel = 10
	self.frames = [pygame.image.load('images/Runner1.png'), pygame.image.load('images/Runner2.png'), pygame.image.load('images/Runner3.png')]
        self.currentframe = 0
        self.jumpheld = False
	self.canJump = False
        self.numframes = 3
        self.image = self.frames[0]
	self.rect = self.image.get_rect()
        self.rect = self.rect.move(35, self.gs.height)
        self.yvel = 0
        self.lock = Lock()

    def tick(self, guardianRect):
        self.lock.acquire()

        # jump
        self.rect = self.rect.move(0, -self.yvel)

	# gravity
        if self.rect.bottom < self.gs.height:
            if self.jumpheld and self.yvel > 0:
                self.yvel = self.yvel - 0.25
            else:
                self.yvel = self.yvel - 0.5
        else:
            self.yvel = 0

	# floor
        if self.rect.bottom > self.gs.height:
            self.yvel = 0
            self.rect.bottom = self.gs.height

	#platform
	if self.rect.colliderect(guardianRect) and -self.yvel > 0:
	    self.rect.bottom = guardianRect.top
	    self.canJump = True
	else:
	    self.canJump = False

        # animate
        self.currentframe = (self.currentframe+1) % self.numframes
        self.image = self.frames[self.currentframe]

        self.lock.release()

    def input(self, event):
        if event.key == K_UP:
            if event.type == KEYDOWN and (self.rect.bottom >= self.gs.height or self.canJump == True):
                self.yvel = self.jumpvel
                self.jumpheld = True
            else:
                self.jumpheld = False
