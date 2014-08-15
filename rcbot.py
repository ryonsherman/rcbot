#!/usr/bin/env python2

import argparse

from twisted.internet import ssl, reactor
from twisted.internet.protocol import ClientFactory
from twisted.words.protocols.irc import IRCClient

from utils.text import style

class RCBot:
    def __init__(self, host, port, nickname, channel, **kwargs):
        client_factory = RCBotClientFactory(
            nickname, channel, 
            reconnect=kwargs.get('reconnect', False))
        if kwargs.get('ssl', False): 
            reactor.connectSSL(host, port, client_factory, ssl.ClientContextFactory())
        else: 
            reactor.connectTCP(host, port, client_factory)
        reactor.run()

    @staticmethod
    def log(type, message):
        from time import strftime
        print "[%s] (%s) %s" % (strftime("%Y-%m-%d %H:%M:%S"), type, message)


class RCBotIRCClient(IRCClient):
    def __init__(self, nickname, channel):
        self.nickname = nickname
        self.channel = channel

    def connectionMade(self):
        RCBot.log('Server', "Connected")
        IRCClient.connectionMade(self)

    def connectionLost(self, reason):
        RCBot.log('Server', "Disconnected")
        IRCClient.connectionLost(self, reason)

    def signedOn(self):
        self.join(self.channel)

    def joined(self, channel):
        RCBot.log('Server', "Joined %s Channel" % channel)

    def privmsg(self, user, channel, message):
        user = user.split('!', 1)[0]
        if channel == self.nickname:
            self.parsePrivateMessage(user, message)
        else:
            self.parseChannelMessage(user, channel, message)

    def parsePrivateMessage(self, user, message):
        RCBot.log('Message', "%s: %s" % (user, message))
        self.parseMessage(user, message)

    def parseChannelMessage(self, user, channel, message):
        RCBot.log('Channel', "%s: %s" % (user, message))
        self.parseMessage(user, message, channel)

    def parseMessage(self, user, message, channel=None):
        message = message.strip()
        kwargs = {'client': self, 'user': user, 'channel': channel}
        
        if not message.startswith('!'):
            kwargs['args'] = filter(lambda arg: arg, message.strip().split(' '))
            __import__('commands.global', fromlist=('Global')).Global(**kwargs)
            return

        args = filter(lambda arg: arg, message.split('!')[1].strip().split(' '))
        command = args.pop(0)
        kwargs.update({'args': args, 'command': command})

        module = False
        try:
            module = __import__('commands.%s.%s' % ('channel' if channel else 'message', command), fromlist=(command))
        except ImportError:
            try:
                module = __import__('commands.global.%s' % command, fromlist=(command))
            except ImportError as error:
                RCBot.log('System', error.message)
                message = "Invalid command \"%s\". Type %s for help." % (command, style.bold("!help"))
                if channel:
                    self.messageChannel(channel, message, user)
                else:
                    self.messageUser(user, message)
        if module:
            getattr(module, command)(**kwargs)

    def messageUser(self, user, message):
        self.msg(user, message.encode('utf-8'))
        message = "%s: %s" % (user, message)
        RCBot.log('MessageResponse', message)

    def messageChannel(self, channel, message, user=None):
        message = "%s: %s" % (user, message) if user else "%s" % message
        self.msg(channel, message.encode('utf-8'))
        RCBot.log('ChannelResponse', message)

class RCBotClientFactory(ClientFactory):
    def __init__(self, nickname, channel, **kwargs):
        self.protocol = RCBotIRCClient(nickname, channel)
        self.reconnect = kwargs.get('reconnect', False)

    def buildProtocol(self, address):
        return self.protocol

    def clientConnectionLost(self, connector, reason):
        if not self.reconnect:
            RCBot.log('Server', "Connection lost.")
        else:
            RCBot.log('Server', "Connection lost. Reconnecting...")
            connector.connect()

    def clientConnectionFailed(self, connector, reason):        
        RCBot.log('Server', "Connection failed: %s" % reason)
        reactor.stop()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('host')
    parser.add_argument('--port', type=int, default=6667)
    parser.add_argument('--ssl', action='store_true', default=False)
    parser.add_argument('--reconnect', action='store_true', default=False)
    parser.add_argument('nickname')
    parser.add_argument('channel')
    args = parser.parse_args()

    RCBot(args.host, args.port, args.nickname, args.channel, ssl=args.ssl)
