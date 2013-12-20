# Thanks eflorenzano.com/blog/2008/11/17/writing-markov-chain-irc-bot-twisted-and-python/

import re

from twisted.words.protocols import irc
from twisted.internet import task
from twisted.internet import protocol

from unknown_replies import smartass_reply


class MainBot(irc.IRCClient):
    # commands
    commands = {}

    @property
    def nickname(self):
        return self.factory.nickname

    def signedOn(self):
        self._add_commands()
        print "Signed on as %s." % (self.nickname,)


    def _must_register(self):
        self.msg("NickServ", "identify %s" % (self.factory.password,))

    def noticed(self, user, channel, message):
        print "Notice from %s in channel %s: %s" % (user, channel, message)
        if user.startswith("NickServ") and "This nickname is registered. Please" in message:
            self._must_register()
        if user.startswith("NickServ") and "You are now identified for" in message: 
            print "Ready"
            self.join_channels()

    def join_channels(self):
        print "Joining channels %r " % self.factory.channels
        for channel in self.factory.channels:
            self.join(channel)

    def joined(self, channel):
        print "Joined %s." % (channel,)

    def privmsg(self, user, channel, msg):
        """ This is where the magic happens """
        if not user or not channel:
            print msg
            return
        self._handle_message(user, channel, msg)

    def _add_commands(self):
        for plugin in self.factory.command_plugins:
            try:
                self.commands.update(plugin.install(self))
            except Exception as e:
                print "Could not install %s: %s" % (plugin.name, e)

    def _handle_message(self, user, channel, msg):
        if msg.startswith(self.nickname):
            command = self._get_msg_content(msg.strip())
            self._match_command(user, channel, command)
        # SEE HERE: non-command plugins only work for non-commands!!
        else:
            self._process_message(user, channel, msg)

    def _is_command(self, msg):
        return msg.startswith(self.nickname)

    def _process_message(self, user, channel, msg):
        for plugin in self.factory.message_plugins:
            plugin.run(user, channel, msg, self)

    def _get_msg_content(self, msg):
        return re.compile(self.nickname + "[:,]* ?", re.I).sub('', msg)

    def _match_command(self, user, channel, msg):
        try:
            self.commands[msg].__call__(user, channel)
        except KeyError:
            self.msg(channel, smartass_reply())


class MainBotFactory(protocol.ClientFactory):

    protocol = MainBot

    def __init__(self, channels,
                 command_plugins=[],
                 message_plugins=[],
                 nickname="montybot",
                 password="snausages"
                 ):
        """
        :param channels: List of channels to join
        :param command_plugins: List of plugins that add extra commands
        :param message_plugins: List of plugins that do things to messages but
            are not commands
        """
        self.channels = channels
        self.nickname = nickname
        self.password = password
        self.command_plugins = command_plugins
        self.message_plugins = message_plugins

    def clientConnectionLost(self, connector, reason):
        print "Lost connections (%s), reconnecting." % (reason,)

        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "Could not connect: %s" % (reason,)

