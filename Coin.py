# CoinDash
# blaws, amarti36
# Coin.py

import pygame
from pygame.locals import *
from random import randint

class Coin(pygame.sprite.Sprite):
    def __init__(self, gs, y):
        pygame.sprite.Sprite.__init__(self)
        self.gs = gs
        self.colorkey = Color(255, 0, 255)
        self.numframes = 7
        self.frames = list()
        for i in range(1, self.numframes+1):
            self.frames.append(pygame.image.load('images/coin'+str(i)+'.png').convert())
            self.frames[-1].set_colorkey(self.colorkey)
            self.frames[-1] = pygame.transform.scale(self.frames[-1], (20, 20))
        self.currentframe = 0
        self.image = self.frames[self.currentframe]
        self.rect = self.image.get_rect().move(self.gs.width*1.5, y)

    def tick(self):
        self.rect.centerx -= self.gs.bg_speed
        self.currentframe = (self.currentframe + 1) % self.numframes
        self.image = self.frames[self.currentframe]
