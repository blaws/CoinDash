import pygame

class Platform(pygame.sprite.Sprite):
	def __init__(self, gs = None):
		pygame.sprite.Sprite.__init__(self)

		self.gs = gs
		self.image = pygame.image.load("images/Platform.png")
		self.rect = self.image.get_rect()
		self.rect = self.rect.move(self.gs.guardian.rect.x, self.gs.guardian.rect.y)
		self.yspeed = 0
		self.xspeed = -5

	def tick(self):
		self.rect = self.rect.move(self.xspeed, self.yspeed)

