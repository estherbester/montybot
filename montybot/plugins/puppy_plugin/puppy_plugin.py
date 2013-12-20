# Plugin class to call the puppy photo fetcher
# TODO: This sucks.

from functools import partial

from .get_puppy import PuppyFetch
from .get_puppy import AVAILABLE_COMMANDS


class PuppyCommandPlugin(object):
    """
    Commands to respond to for puppy links
    """
    name = 'Puppy Commands'


    def __init__(self, bot_instance):
        """ Get the bot instance so we can do stuff with it. """
        self.bot_instance = bot_instance

    @classmethod
    def install(cls, bot_instance):
        """
        Instantiate the plugin instance, couple it to the bot instance.
        :returns: commands to which this plugin responds.
        :rtype: Dictionary
        """
        plugin = cls(bot_instance)
        return plugin._create_command_dict()

    def spit(self, reply, user, channel):
        self.bot_instance.msg(channel, reply)

    def get_link(self, puppy_type, user, channel):
        """
        This is the function mapped to each puppy command. Args are passed
        in via the partial (in _create_command_dict).
        """
        reply = PuppyFetch.get(puppy_type)
        self.bot_instance.msg(channel, reply)

    def _create_command_dict(self):
        """ Create the dict of commands this bot responds to. """
        commands = {}
        
        commands['what have you?'] = partial(self.spit, self._command_string())
        for puppy_command in AVAILABLE_COMMANDS:
            commands[puppy_command.command] = partial(self.get_link,
                                                      puppy_command.puppy_type)
        return commands

    def _command_string(self):
        return '; '.join(self._command_list())

    def _command_list(self):
        return [command.command for command in AVAILABLE_COMMANDS]

if __name__ == "__main__":
    from mock import Mock

    def mock_msg(chan, msg):
        print chan
        print msg
    bot_instance = Mock()
    bot_instance.msg = mock_msg

    pcp = PuppyCommandPlugin.install(bot_instance)

    pcp['puppy lottery'].__call__('test user', '#test-channel')
