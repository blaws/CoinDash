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
        self.jumpvel = 8
	self.frames = [pygame.image.load('images/Runner1.png'), pygame.image.load('images/Runner2.png'), pygame.image.load('images/Runner3.png')]
        self.currentframe = 0
        self.jumpheld = False
	self.canJump = False
        self.numframes = 3
        self.image = self.frames[0]
	self.rect = self.image.get_rect()
        self.rect = self.rect.move(35, 200)
        self.yvel = 0
        self.lock = Lock()

    def tick(self):
	self.lock.acquire()
	self.canJump = False

        # jump
        self.rect = self.rect.move(0, -self.yvel)

	# gravity
        if self.rect.top < self.gs.height:
            if self.jumpheld and self.yvel > 0:
                self.yvel = self.yvel - 0.25
            else:
                self.yvel = self.yvel - 0.5
        else:
		self.gs.gameover()

	#ground
	for ground in self.gs.grounds:
		if self.rect.colliderect(ground.rect):
		    if self.rect.bottom - ground.rect.top >= 15 and abs(self.rect.right - ground.rect.left) <= 8:
			self.gs.gameover()
		    self.yvel = 0
		    self.canJump = True

	#platform
	for platform in self.gs.platforms:
		if self.rect.colliderect(platform.rect) and abs(self.rect.bottom - platform.rect.top) <= 8:
		    self.yvel = 0
		    self.canJump = True
		if platform.rect.x <= -40:
			del self.gs.platforms[self.gs.platforms.index(platform)]

	#wiley
	for wiley in self.gs.wileys:
		if self.rect.colliderect(wiley.rect):
			self.gs.gameover()

	#coin
	for coin in self.gs.coins:
		if self.rect.colliderect(coin.rect):
			self.gs.score += 1
			del self.gs.coins[self.gs.coins.index(coin)]

        # animate
        self.currentframe = (self.currentframe+0.5) % self.numframes
        self.image = self.frames[int(self.currentframe)]

        self.lock.release()

    def input(self, event):
        if event.key == K_UP:
            if event.type == KEYDOWN and (self.rect.bottom >= self.gs.height or self.canJump == True):
                self.yvel = self.jumpvel
                self.jumpheld = True
            else:
                self.jumpheld = False
