# PyTwist
# blaws, amarti36
# PyTwist.py

from twisted.internet import reactor
from twisted.internet.protocol import Protocol, Factory, ReconnectingClientFactory

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
        self.gs.connection = self
        self.connType = side  # 0=server/Runner, 1=client/Guardian

    def connectionMade(self):
        print 'Connected'

    def dataReceived(self, data):
        print data

    def connectionLost(self, reason):
        print 'Connection lost/closed'
