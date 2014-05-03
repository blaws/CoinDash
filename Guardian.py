import pygame

class Ground(pygame.sprite.Sprite):
	def __init__(self, gs = None, x = 0, y = 0):
		pygame.sprite.Sprite.__init__(self)
		self.gs = gs
		self.image = pygame.image.load("images/Ground.png")
		self.rect = self.image.get_rect()
		self.rect = self.rect.move(x, y)
		self.xspeed = -10
		self.yspeed = 0

	def tick(self):
			self.rect = self.rect.move(self.xspeed, self.yspeed)

class Runner(pygame.sprite.Sprite):
	def __init__(self, gs = None):
		pygame.sprite.Sprite.__init__(self)

		self.gs = gs
		self.image = pygame.image.load("images/Runner1.png")
		self.animation = 0
		self.rect = self.image.get_rect()
		self.rect = self.rect.move(50, 290)

	def tick(self):
		self.animation += 1
		animation = self.animation % 6
		if animation == 0:
			self.image = pygame.image.load("images/Runner1.png")
		elif animation == 2:
			self.image = pygame.image.load("images/Runner2.png")
		elif animation == 4:
			self.image = pygame.image.load("images/Runner3.png")

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

	def input(self, event):
		if event.type is pygame.KEYDOWN:
			if event.key == pygame.K_w or event.key == pygame.K_s:
				self.move(event.key)
			elif event.key == pygame.K_RETURN:
				self.makePlatform()
		elif event.type is pygame.KEYUP:
			if event.key == pygame.K_s or event.key == pygame.K_w:
				self.stopMove()

	def move(self, key):
		if key == pygame.K_s:
			self.yspeed = 10
		elif key == pygame.K_w:
			self.yspeed = -10

	def stopMove(self):
		self.yspeed = 0

	def makePlatform(self):
		self.image = pygame.image.load("images/Platform.png")
		self.xspeed = -5

class GameSpace:
	def main(self):
		pygame.init()

		self.size = self.width, self.height = 640, 480
		self.backgroundImage = pygame.image.load("images/Background.png")
		self.backgroundImageRect = self.backgroundImage.get_rect()

		self.screen = pygame.display.set_mode(self.size)

		self.clock = pygame.time.Clock()

		self.guardian = Guardian(self)
		self.runner = Runner(self)
		self.ground = list()
		self.ground.append(Ground(self, 0, 360))
		self.ground.append(Ground(self, 120, 360))
		self.ground.append(Ground(self, 240, 360))
		self.ground.append(Ground(self, 360, 360))
		self.ground.append(Ground(self, 480, 360))
		self.ground.append(Ground(self, 600, 360))
		self.ground.append(Ground(self, 720, 360))

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
			self.runner.tick()
			for grounds in self.ground:
				grounds.tick()
				if grounds.rect.x <= -120:
					del self.ground[0]
					self.ground.append(Ground(self, self.ground[-1].rect.x +120, 360))

			self.screen.blit(self.backgroundImage, self.backgroundImageRect)
			for grounds in self.ground:
				self.screen.blit(grounds.image, grounds.rect)
			self.screen.blit(self.runner.image, self.runner.rect)
			self.screen.blit(self.guardian.image, self.guardian.rect)

			pygame.display.flip()

if __name__ == '__main__':
	gs = GameSpace()
	gs.main()
