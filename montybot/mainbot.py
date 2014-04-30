
from twisted.words.protocols import irc
from twisted.internet import task
from twisted.internet import protocol
from .message import Message
from ConfigParser import SafeConfigParser

class MainBot(irc.IRCClient):
    # commands
    commands = {}

    is_registered = False
    must_register = False

    @property
    def nickname(self):
        return self.factory.nickname

    @property
    def password(self):
        return self.factory.password

    def ghost(self):
        """ 
        A stupid way to re-identify when cut off. Not sure 
        how even to call this method while the app is running.
        """
        self.msg('nickserv', 'GHOST %s %s' % (self.nickname, 'snausages'))
        self.quit()

    def signedOn(self):
        self._add_commands()
        print "Signed on as %s." % (self.nickname,)

    def join_channels(self):
        """ 
        Only join channels if the bot is registered, or
        if it does not need to register
        """
        if not self.must_register or self.is_registered:
            print "Joining channels %r " % self.factory.channels
            for channel in self.factory.channels:
                self.join(channel)

    def joined(self, channel):
        """"
        Callback once channel is joined
        """
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
            self.must_register = True
            self._asked_to_register()
        if user.startswith("NickServ") and "You are now identified for" in message:
            self.is_registered=True
            print "Ready"
        # TODO: this makes no sense
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

    def _asked_to_register(self):
        if self.must_register and not self.is_registered:
            self.msg("NickServ", "identify %s" % (self.factory.password,))


class MainBotFactory(protocol.ClientFactory):

    protocol = MainBot

    def __init__(self, config_file, 
                 channels,
                 command_plugins=[],
                 message_plugins=[],
                 taunt_plugins=[]
                 ):
        """
        :param channels: List of channels to join
        :param command_plugins: List of plugins that add extra commands
        :param message_plugins: List of plugins that do things to messages but
            are not commands
        """
        #TODO: clean this up 
        settings = self._read_config(config_file)['irc']
        self.channels = channels
        try:
            self.nickname = settings['nickname'] 
            self.password = settings['password']
        except KeyError as key:
            print "You are missing %s in your config file."  % (key,)
        self.command_plugins = command_plugins
        self.message_plugins = message_plugins
        self.taunt_plugins = taunt_plugins

    def clientConnectionLost(self, connector, reason):
        print "Lost connections (%s), reconnecting." % (reason,)
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "Could not connect: %s" % (reason,)

    def _read_config(self, config_file):
        config = SafeConfigParser()
        config.read(config_file)
        config_dict = {}
        for section in config.sections():
            config_dict[section] = dict(config.items(section))
        if not config_dict:
            raise Exception("No configs were loaded from %s" % config_file)
        return config_dict


