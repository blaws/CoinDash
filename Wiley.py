import pygame
from random import randint

class Wiley(pygame.sprite.Sprite):
	def __init__(self, gs, y):
		pygame.sprite.Sprite.__init__(self)

		self.gs = gs
		self.count = 0
		self.image = pygame.image.load("images/Wiley1.png")
                self.image = pygame.transform.scale(self.image, (75, 75))
		self.rect = self.image.get_rect()
		self.rect = self.rect.move(640, y)
		self.yspeed = 0
		self.xspeed = -5

	def tick(self):
		self.rect = self.rect.move(self.xspeed, self.yspeed)
		self.count += 1
		self.animation = self.count % 8
		if self.animation == 0:
			self.image = pygame.image.load("images/Wiley1.png")
                        self.image = pygame.transform.scale(self.image, (75, 75))
		elif self.animation == 2:
			self.image = pygame.image.load("images/Wiley2.png")
                        self.image = pygame.transform.scale(self.image, (75, 75))
		elif self.animation == 4:
			self.image = pygame.image.load("images/Wiley3.png")
                        self.image = pygame.transform.scale(self.image, (75, 75))
		elif self.animation == 6:
			self.image = pygame.image.load("images/Wiley4.png")
                        self.image = pygame.transform.scale(self.image, (75, 75))
		if self.rect.x <= -100:
			del self.gs.wileys[self.gs.wileys.index(self)]
