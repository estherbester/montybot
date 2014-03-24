from .metaclass import PluginMetaClass


class TauntSeanPlugin(object):
    __metaclass__ = PluginMetaClass

    name = "Taunt Sean plugin"

    # TODO: Not sure this is properly done (see metaclass)
    def __init__(self, bot_instance):
        self.bot_instance = bot_instance

    @classmethod
    def run(cls, user, channel, message, bot_instance):
        """ """
        instance = cls(bot_instance)
        # if sean is asking
        if instance._from_sean_to_bot(user, message):
            instance._run(user, channel, message)

    def _from_sean_to_bot(self, user, message):
        return user == 'seanz' and self.bot_instance.nickname in message

    def _run(self, user, channel, message):
        # pick a random image
        url = "http://www.aston-pharma.com/bionic-animals/images/12-bionic-animals/kvcgj7E.jpg"
        self.bot_instance.msg(channel, "%s: is this what you wanted? %s" % (user, url))
