import pygame
from Platform import *
from threading import Lock

class Ground(pygame.sprite.Sprite):
	def __init__(self, gs = None, x = 0, y = 0):
		pygame.sprite.Sprite.__init__(self)
		self.gs = gs
		if self.gs.gap == 4:
			self.image = pygame.image.load("images/Ground2.png")
		else:
			self.image = pygame.image.load("images/Ground.png")
		self.rect = self.image.get_rect()
		self.rect = self.rect.move(x, y)
		self.xspeed = -5
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
