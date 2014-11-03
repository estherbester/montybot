# This plugin allows the bot to respond in specific ways to specific
# users

from .metaclass import PluginMetaClass

class FiberCheck(object):
    """
	TODO: consider not making classes but just register the users
	and their response methods
	"""
    __metaclass__ = PluginMetaClass

    name = "Speed test check" 
    # TODO: get from config
    endpoint = ""

    # TODO: Not sure this is properly done (see metaclass)
    def __init__(self, bot_instance):
        self.bot_instance = bot_instance

    @classmethod
    def install(cls, bot_instance):
        """ """
        plugin = cls(bot_instance)
        return plugin._get_message()


    def _get_message():
        pass

        # if the targeted user is the sender
        if self._speed_check(user, message):
            self.bot_instance.handled = True
            self.bot_instance.msg(channel, " message:%s" % ("foo")) 

    def _speed_check(self, user, message):
        return message.startswith("fiber")

    def _run(self, user, channel, message):
        """ abstract method """



