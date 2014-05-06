# PyTwist
# blaws, amarti36
# Guardian.py

import pygame
from Platform import *
from threading import Lock

class Ground(pygame.sprite.Sprite):
	def __init__(self, gs = None, x = 0, y = 0):
		pygame.sprite.Sprite.__init__(self)
		self.gs = gs
		if abs(self.gs.grounds[self.gs.grounds.index(self) - 1].rect.x - x) < 120:
			self.image = pygame.image.load("images/Ground2.png")
		else:
			self.image = pygame.image.load("images/Ground.png")
		self.rect = self.image.get_rect()
		self.rect = self.rect.move(x, y)
		self.xspeed = -5
		self.yspeed = 0

	def tick(self):
			self.rect = self.rect.move(self.xspeed, self.yspeed)

class Guardian(pygame.sprite.Sprite):
	def __init__(self, gs = None):
		pygame.sprite.Sprite.__init__(self)

		self.gs = gs
		self.image = pygame.image.load("images/InvisiblePlatform.png")
		self.rect = self.image.get_rect()
		self.rect = self.rect.move(600, 230)
		self.yspeed = 0
		self.xspeed = 0
		self.addplatform = False
		self.counter = 0

		self.lock = Lock()

	def tick(self):
		self.lock.acquire()
		if self.addplatform:
			if self.counter <= 0:
				self.gs.platforms.append(Platform(self.gs))
				self.counter = self.rect.width/6
			else:
				self.counter -= 1
		self.gs.newplatform = True
		self.rect = self.rect.move(self.xspeed, self.yspeed)
		self.lock.release()

	def input(self, event):
		if event.type is pygame.KEYDOWN:
			if event.key == pygame.K_w or event.key == pygame.K_s or event.key == pygame.K_a or event.key == pygame.K_d:
				self.move(event.key)
			elif event.key == pygame.K_RETURN:
				self.addplatform = True
				self.counter = 0
		elif event.type is pygame.KEYUP:
			if event.key == pygame.K_s or event.key == pygame.K_w or event.key == pygame.K_a or event.key == pygame.K_d:
				self.stopMove()
			elif event.key == pygame.K_RETURN:
				self.addplatform = False

	def move(self, key):
		if key == pygame.K_s:
			self.yspeed = 10
		elif key == pygame.K_w:
			self.yspeed = -10
		elif key == pygame.K_a:
			self.xspeed = -10
		elif key == pygame.K_d:
			self.xspeed = 10

	def stopMove(self):
		self.yspeed = 0
		self.xspeed = 0
