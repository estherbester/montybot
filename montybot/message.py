import re

from unknown_replies import smartass_reply

class Message(object):
    """
    A message comes from a user and is sent to a channel.
    The MainBot instance handles the message.
    """
    def __init__(self, user, channel, message, bot_instance):
        """
        Initialize the Message object that will be handled smartly.
        """
        self.user = user
        self.channel = channel
        self.message = message
        self.bot_instance = bot_instance

    def handle(self):
        """ 
        Bot needs to know whether a given message has been handled
        """
        self.bot_instance.handled = False
        self._handle()

    def run_command_plugins(self):
        if self._is_command() and not self.bot_instance.handled:
            command = self._get_msg_content()
            self._match_command()

    def run_taunt_plugins(self):
        if self.bot_instance.factory.taunt_plugins:
            for plugin in self.bot_instance.factory.taunt_plugins:
                plugin.run(self.user, self.channel, self.message, self.bot_instance)

    def run_message_plugins(self):
        for plugin in self.bot_instance.factory.message_plugins:
            plugin.run(self.user, self.channel, self.message, self.bot_instance)

    def _handle(self):
        """
        Run through the various plugins for a given message.
        The order matters: taunt plugnis and command plugins
        can't be combined. Message plugins will always respond
            """
        self.run_taunt_plugins()
        self.run_command_plugins()
        self.run_message_plugins()

    def _get_msg_content(self):
        """ return the message content only.
        """
        message = self.message.strip()
        return re.compile(self.bot_instance.nickname + "[:,]* ?", re.I).sub('', message)

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
        msg = self.message.lower()
        cmd = cmd.lower()
        return cmd in msg

    def _is_command(self):
        return self.message.startswith(self.bot_instance.nickname)

    

