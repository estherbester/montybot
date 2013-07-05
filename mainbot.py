# Thanks eflorenzano.com/blog/2008/11/17/writing-markov-chain-irc-bot-twisted-and-python/

import re

from twisted.words.protocols import irc
from twisted.internet import protocol

from unknown_replies import smartass_reply

QUIT = "go home, you're drunk"

LISTEN_FOR = []


class MainBot(irc.IRCClient):
    # commands
    commands = {}

    @property
    def nickname(self):
        return self.factory.nickname

    def signedOn(self):
        self._add_quit_command()
        self._add_commands()
        self.join(self.factory.channel)
        print "Signed on as %s." % (self.nickname,)

    def joined(self, channel):
        print "Joined %s." % (channel,)

    def _add_quit_command(self):
        self.commands[QUIT] = self.quit

    def privmsg(self, user, channel, msg):
        if not user:
            return
        self._handle_message(user, channel, msg)

    def _add_commands(self):
        for plugin in self.factory.command_plugins:
            try:
                self.commands.update(plugin.install())
            except Exception:
                print "Could not install %s" % (plugin.__class__,)

    def _handle_message(self, user, channel, msg):
        if self.nickname in msg:
            msg = self._get_msg_content(msg.strip())
            reply = self._match_commands(msg)
            self.msg(self.factory.channel, reply)
        # SEE HERE: non-command plugins only work for non-commands!!
        else:
            self._process_message(user, msg)

    def _process_message(self, user, msg):
        for plugin in self.factory.message_plugins:
            # User name, message, callback, args.
            plugin.run(user, msg, self)
            #self.msg(self.factory.channel, reply)

    def _get_msg_content(self, msg):
        return re.compile(self.nickname + "[:,]* ?", re.I).sub('', msg)

    def _match_commands(self, msg):
        try:
            reply = self.commands[msg].__call__()
        except KeyError:
            reply = smartass_reply()
        return str(reply)


class MainBotFactory(protocol.ClientFactory):
    protocol = MainBot

    def __init__(self, channel,
                 command_plugins=[],
                 message_plugins=[],
                 nickname="montybot"):
        """
        command_plugins: a list of plugins that add extra commands
        """
        self.channel = channel
        self.nickname = nickname
        self.command_plugins = command_plugins
        self.message_plugins = message_plugins
        assert command_plugins is not None
        #for plugin in command_plugins.extend(message_plugins):
        #    print "Plugin: %s" % plugin.name

    def clientConnectionLost(self, connector, reason):
        print "Lost connections (%s), reconnecting." % (reason,)

        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "Could not connect: %s" % (reason,)

