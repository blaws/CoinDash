import pygame
from random import randint

class Wiley(pygame.sprite.Sprite):
	def __init__(self, gs = None):
		pygame.sprite.Sprite.__init__(self)

		self.gs = gs
		self.count = 0
		self.image = pygame.image.load("images/Wiley1.png")
		self.rect = self.image.get_rect()
		self.rect = self.rect.move(640, randint(0, 300))
		self.yspeed = 0
		self.xspeed = -5

	def tick(self):
		self.rect = self.rect.move(self.xspeed, self.yspeed)
		self.count += 1
		self.animation = self.count % 8
		if self.animation == 0:
			self.image = pygame.image.load("images/Wiley1.png")
		elif self.animation == 2:
			self.image = pygame.image.load("images/Wiley2.png")
		elif self.animation == 4:
			self.image = pygame.image.load("images/Wiley3.png")
		elif self.animation == 6:
			self.image = pygame.image.load("images/Wiley4.png")