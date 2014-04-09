import re

from twisted.words.protocols import irc
from twisted.internet import task
from twisted.internet import protocol

from unknown_replies import smartass_reply


class Message(object):
    def __init__(self, user, channel, message, bot_instance):
        self.user = user
        self.channel = channel
        self.msg = message
        self.bot_instance = bot_instance

    def handle(self):
        self.bot_instance.handled = False
        self._handle()

    def _handle(self):
        if self.bot_instance.factory.taunt_plugins:
            self._taunt()
        if self._is_command() and not self.bot_instance.handled:
            command = self._get_msg_content()
            self._match_command()
        else:
            for plugin in self.bot_instance.factory.message_plugins:
                plugin.run(self.user, self.channel, self.msg, self.bot_instance)

    def _get_msg_content(self):
        """ return the message content only.
        """
        msg = self.msg.strip()
        return re.compile(self.bot_instance.nickname + "[:,]* ?", re.I).sub('', msg)

    def _is_command(self):
        return self.msg.startswith(self.bot_instance.nickname)

    def _match_command(self):
        """
        Call the command that matches anything in our command dict.
        If no matches, return a smartass reply.
        """
        commands = [func for command, func in self.bot_instance.commands.items() \
            if self._msg_contains_cmd(command)]

        # if nothing available, send a smartass reply
        if len(commands) > 0:
           commands[0].__call__(self.user, self.channel)
        else:
            self.bot_instance.msg(self.channel, smartass_reply())

    def _msg_contains_cmd(self, cmd):
        """ Scrub the message """
        msg = self.msg.lower()
        cmd = cmd.lower()
        return cmd in msg

    def _taunt(self):
        for plugin in self.bot_instance.factory.taunt_plugins:
            plugin.run(self.user, self.channel, self.msg, self.bot_instance)


class MainBot(irc.IRCClient):
    # commands
    commands = {}

    @property
    def nickname(self):
        return self.factory.nickname

    def ghost(self):

        self.msg('nickserv', 'GHOST puppybot snausages')
        self.quit()

    def signedOn(self):
        self._add_commands()
        print "Signed on as %s." % (self.nickname,)

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

    def noticed(self, user, channel, message):
        """ Callback for if the bot receives a Notice. """
        print "Notice from %s in channel %s: %s" % (user, channel, message)
        if user.startswith("NickServ") and "This nickname is registered. Please" in message:
            self._must_register()
        if user.startswith("NickServ") and "You are now identified for" in message:
            print "Ready"
        self.join_channels()

    def _add_commands(self):
        for plugin in self.factory.command_plugins:
            try:
                self.commands.update(plugin.install(self))
            except Exception as e:
                print "Could not install %s: %s" % (plugin.name, e)

    def _handle_message(self, user, channel, msg):
        """ Every message is handled.
        """
        try:
            self.message = Message(user, channel, msg, self)
            self.message.handle()
            del self.message
        except Exception as error:
            print error

    def _must_register(self):
        self.msg("NickServ", "identify %s" % (self.factory.password,))



class MainBotFactory(protocol.ClientFactory):

    protocol = MainBot

    def __init__(self, channels,
                 command_plugins=[],
                 message_plugins=[],
                 taunt_plugins=[],
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
        self.taunt_plugins = taunt_plugins

    def clientConnectionLost(self, connector, reason):
        print "Lost connections (%s), reconnecting." % (reason,)

        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "Could not connect: %s" % (reason,)

