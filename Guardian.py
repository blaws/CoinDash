import pygame

class Guardian(pygame.sprite.Sprite):
	def __init__(self, gs = None):
		pygame.sprite.Sprite.__init__(self)

		self.gs = gs
		self.image = pygame.image.load("images/InvisiblePlatform.png")
		self.rect = self.image.get_rect()
		self.rect = self.rect.move(600, 230)
		self.yspeed = 0
		self.xspeed = 0

	def tick(self):
		self.rect = self.rect.move(self.xspeed, self.yspeed)
		if self.rect.x <= -40:
			self.xspeed = 0
			self.image = pygame.image.load("images/InvisiblePlatform.png")
			self.rect = self.rect.move(600 - self.rect.x, 230 - self.rect.y)

	def move(self, key):
		if key == pygame.K_DOWN:
			self.yspeed = 10
		elif key == pygame.K_UP:
			self.yspeed = -10

	def stopMove(self):
		self.yspeed = 0

	def makePlatform(self):
		self.image = pygame.image.load("images/Platform.png")
		self.xspeed = -10

class GameSpace:
	def main(self):
		pygame.init()

		self.size = self.width, self.height = 640, 480
		self.black = 0, 0, 0

		self.screen = pygame.display.set_mode(self.size)

		self.clock = pygame.time.Clock()

		self.guardian = Guardian(self)

		while True:
			self.clock.tick(60)

			for event in pygame.event.get():
				if event.type is pygame.KEYDOWN:
					if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
						self.guardian.move(event.key)
					elif event.key == pygame.K_RETURN:
						self.guardian.makePlatform()
					elif event.key == pygame.K_ESCAPE:
						sys.exit(0)
				elif event.type is pygame.KEYUP:
					if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
						self.guardian.stopMove()

			self.guardian.tick()

			self.screen.fill(self.black)

			self.screen.blit(self.guardian.image, self.guardian.rect)

			pygame.display.flip()

if __name__ == '__main__':
	gs = GameSpace()
	gs.main()
