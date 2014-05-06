# CoinDash
# blaws, amarti36
# CoinDash.py

import sys
from random import randint

from twisted.internet import reactor
from twisted.internet.task import LoopingCall

import pygame
from pygame.locals import *

from Guardian import *
from Runner import *
from Connection import *
from Platform import *
from Coin import *
from Wiley import *
from Explosion import *

class PyTwist:
    def __init__(self):
        pygame.init()
        self.connection = None
        self.side = None
        self.size = self.width, self.height = 640, 480
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption('PyTwist')
        self.bg = pygame.image.load('images/Background.png').convert()
        self.reverse_bg = pygame.transform.flip(self.bg, True, False)
        self.bg_rect = self.bg.get_rect()
        self.bg_speed = 4
	self.count = 1
	self.gap = 0
	self.score = 0
	self.font = pygame.font.Font(None, 72)
	self.connectionFont = pygame.font.Font(None, 72)
        self.addcoin = -1
        self.addwiley = -1

        # create game objects
        self.runner = Runner(self)
	self.guardian = Guardian(self)
	self.platforms = list()
	self.wileys = list()
        self.newplatform = False
	self.grounds = list()
        self.groundimage = pygame.image.load('images/Ground.png').convert()  # separated from the Ground class because the list of ground objects must be pickled and sent over the connection
        self.spikegroundimage = pygame.image.load('images/Ground2.png').convert()
        for i in range(0,721,120):
            self.grounds.append(Ground(i, 360))
        self.coins = list()

	# create game sounds
	self.explosionSound = pygame.mixer.Sound("sounds/Explosion.wav")
	self.jumpSound = pygame.mixer.Sound("sounds/Jump.aiff")
	self.coinSound = pygame.mixer.Sound("sounds/Coin.wav")
	pygame.mixer.music.load("sounds/LazyInSpain.wav")
	pygame.mixer.music.play(-1)

    def connect(self, side, port, addr=None):
        self.side = side
        if side == 0:
            reactor.listenTCP(port, ConnectionFactory(self))
        if side == 1:
            reactor.connectTCP(addr, port, ConnectionClientFactory(self))

    def printerror(self, error):
        print error
        reactor.stop()

    def start(self):
        self.gameloop = LoopingCall(self.main).start(1/float(60))
        self.gameloop.addErrback(self.printerror)
        reactor.run()

    def main(self):  # pygame loop - called by Twisted's event loop every 1/60 of a second
        # handle input
        for event in pygame.event.get():
            if event.type == QUIT:
                reactor.stop()
            elif event.type == KEYUP or event.type == KEYDOWN:
                if event.key == K_q or event.key == K_ESCAPE:
                    reactor.stop()
                else:
                    if self.side == 0:
                        self.runner.input(event)
                    elif self.side == 1:
                        self.guardian.input(event)

        # iterate game objects
        self.runner.tick()
        self.guardian.tick()
	for platform in self.platforms:
		platform.tick()
	for wiley in self.wileys:
		wiley.tick()
	for ground in self.grounds:
		ground.tick()
		if ground.rect.right < -120:  # can't be in Ground.tick() because Ground cannot have a reference to the gamespace (because of pickling)
                    del self.grounds[self.grounds.index(ground)]
        if self.connection and self.side == 0 and randint(0,100) == 0:
            self.addcoin = randint(0, self.height-150)
            self.coins.append(Coin(self, self.addcoin))
        elif self.connection and self.side == 1 and self.addcoin > -1:
            self.coins.append(Coin(self, self.addcoin))
            self.addcoin = -1
        for coin in self.coins:
            coin.tick()
        self.move_background()
	self.count += 1
	if self.count == 24:
		self.count = 1
		if (self.side == 0 and 1 != randint(0,9) and self.gap == 0) or self.connection == None or self.gap == 4:
			self.grounds.append(Ground(640, 360))
#                        self.groundrects.append(self.grounds[-1].rect)
		elif self.side == 0:
			self.gap += 1
	if 1 == randint(0, 600) and self.connection != None and self.side == 0:
            self.addwiley = randint(0, self.height-150)
            self.wileys.append(Wiley(self, self.addwiley))
        elif self.connection and self.side == 1 and self.addwiley > -1:
            self.wileys.append(Wiley(self, self.addwiley))
            self.addwiley = -1


        # update other player
        if self.connection:
            self.connection.sendUpdate()

        # display
	self.blit_bg()
        self.screen.blit(self.guardian.image, self.guardian.rect)
	self.blit_platforms()
	self.blit_grounds()
	self.blit_coins()
        self.screen.blit(self.runner.image, self.runner.rect)
	self.blit_wileys()
	self.blit_text()
        pygame.display.flip()

    def move_background(self):
        self.bg_rect = self.bg_rect.move(-self.bg_speed, 0)
        if self.bg_rect.right <= 0:
            self.bg_rect.left = self.width

    def gameover(self):
	self.explosion = Explosion(self)
	scoreFont = pygame.font.Font(None, 72)
	scoreText = scoreFont.render("SCORE:", 1, (10, 10, 10))
	scoreTextpos = scoreText.get_rect()
	text = self.font.render(str(self.score), 1, (10, 10, 10))
	textpos = text.get_rect()
	textpos.x = 320
	textpos.y = 80
	scoreTextpos.x = 250
	self.youDied = pygame.image.load("images/youDied.png")
	self.youDied_rect = self.youDied.get_rect()
	self.explosionSound.play()

	while self.explosion.animation != 15:
		self.explosion.tick()
		

		self.blit_bg()
		self.screen.blit(self.guardian.image, self.guardian.rect)
		for platform in self.platforms:
			self.screen.blit(platform.image, platform.rect)
		for ground in self.grounds:
                    if self.grounds.index(ground) == 0 or abs(self.grounds[self.grounds.index(ground)-1].rect.x - ground.rect.x) > 120:
                        self.screen.blit(self.spikegroundimage, ground.rect)  #ground.image, 
                    else:
                        self.screen.blit(self.groundimage, ground.rect)  #ground.image, ground.rect)
		for wiley in self.wileys:
			self.screen.blit(wiley.image, wiley.rect)
		self.screen.blit(text, textpos)
		self.screen.blit(scoreText, scoreTextpos)
		self.screen.blit(self.explosion.image, self.explosion.rect)
		self.screen.blit(self.youDied, self.youDied_rect)
		pygame.display.flip()
	reactor.stop()

    def blit_coins(self):
	for coin in self.coins:
	    if coin.rect.right > self.width:
		tmp_rect = Rect(coin.rect)
		tmp_rect.right = self.width
		self.screen.blit(coin.image, tmp_rect)
	    else:
		self.screen.blit(coin.image, coin.rect)

    def blit_bg(self):
	self.screen.blit(self.bg, self.bg_rect)
	if self.bg_rect.right < self.width:
	    self.screen.blit(self.reverse_bg, self.bg_rect.move(self.width, 0))
	else:
	    self.screen.blit(self.reverse_bg, self.bg_rect.move(-self.width, 0))
	
    def blit_platforms(self):
	for platform in self.platforms:
		self.screen.blit(platform.image, platform.rect)

    def blit_grounds(self):
	for ground in self.grounds:
	    if self.grounds.index(ground) == 0 or abs(self.grounds[self.grounds.index(ground)-1].rect.x - ground.rect.x) > 120:
		self.screen.blit(self.spikegroundimage, ground.rect)
	    else:
		self.screen.blit(self.groundimage, ground.rect)

    def blit_wileys(self):
	for wiley in self.wileys:
		self.screen.blit(wiley.image, wiley.rect)

    def blit_text(self):
	text = self.font.render(str(self.score), 1, (10, 10, 10))
	textpos = text.get_rect()
	self.screen.blit(text, textpos)
	if self.connection == None:
		connectionText = self.connectionFont.render("WAITING FOR PLAYER 2", 1, (255, 0, 0))
		connectionTextpos = connectionText.get_rect()
		connectionTextpos.y = 140
		self.screen.blit(connectionText, connectionTextpos)

if __name__ == '__main__':
    if (len(sys.argv)!=3 and len(sys.argv)!=4) or (sys.argv[1].lower()!='runner' and sys.argv[1].lower()!='guardian'):
        print 'usage: python '+sys.argv[0]+' <runner/guardian> <port> <hostname (guardian only)>'
        sys.exit(1)

    pt = PyTwist()

    if sys.argv[1].lower() == 'runner':
        pt.connect(0, int(sys.argv[2]))
    elif sys.argv[1].lower() == 'guardian' and len(sys.argv) > 3:
        pt.connect(1, int(sys.argv[2]), sys.argv[3])

    pt.start()
