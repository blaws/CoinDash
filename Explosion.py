import pygame

class Explosion(pygame.sprite.Sprite):
	def __init__(self, gs = None):
		pygame.sprite.Sprite.__init__(self)

		self.gs = gs
		self.count = 0
		self.animation = 1
		self.image = pygame.image.load("images/Explosion1.png")
		self.rect = self.image.get_rect()
		self.x = self.gs.runner.rect.x + 15
		self.y = self.gs.runner.rect.y
		print self.y
		if self.y >= 400:
			self.y = 400
		self.rect = self.rect.move(self.x, self.y)

	def tick(self):
		if self.count == 30:
			self.animation += 1
			self.image = pygame.image.load("images/Explosion" + str(self.animation) + ".png")
			self.count = 0
		self.count += 1
