# PyTwist
# blaws, amarti36
# PyTwist.py

import pygame
from pygame.locals import *
from Platform import *
from twisted.internet import reactor
from twisted.internet.protocol import Protocol, Factory, ReconnectingClientFactory
from pickle import dumps, loads

class ConnectionFactory(Factory):
    def __init__(self, gs):
        self.gs = gs

    def buildProtocol(self, addr):
        return Connection(self.gs, 0)

class ConnectionClientFactory(ReconnectingClientFactory):
    def __init__(self, gs):
        self.gs = gs

    def buildProtocol(self, addr):
        return Connection(self.gs, 1)

class Connection(Protocol):
    def __init__(self, gs, side):
        self.gs = gs
        self.connType = side  # 0=server/Runner, 1=client/Guardian

    def connectionMade(self):
        print 'Connected'
        self.gs.connection = self

    def dataReceived(self, data):
        self.data = loads(data)
        if self.connType == 0:
            self.gs.guardian.lock.acquire()
            self.gs.guardian.rect = Rect(self.data[0])
            self.gs.guardian.xspeed = int(self.data[1])
            self.gs.guardian.yspeed = int(self.data[2])
            self.gs.guardian.addplatform = bool(self.data[3])
            self.gs.guardian.lock.release()
        else:
            self.gs.runner.lock.acquire()
            self.gs.runner.rect = Rect(self.data[0])
            self.gs.runner.currentframe = int(self.data[1])
            self.gs.runner.jumpheld = int(self.data[2])
            self.gs.runner.yvel = int(self.data[3])
            self.gs.runner.lock.release()

    def connectionLost(self, reason):
        print 'Connection lost/closed'

    def sendUpdate(self):
        if self.connType == 0:
            self.data = [self.gs.runner.rect, self.gs.runner.currentframe, self.gs.runner.jumpheld, self.gs.runner.yvel]
        else:
            self.data = [self.gs.guardian.rect, self.gs.guardian.xspeed, self.gs.guardian.yspeed, self.gs.guardian.addplatform]
            self.gs.newplatform = False
        self.transport.write(dumps(self.data))
