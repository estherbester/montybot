QUIT_MSG = "go home, you're drunk"


class CreativeQuitPlugin(object):
    name = "Creative quit plugin"

    def __init__(self, bot_instance):
        self.bot_instance = bot_instance

    def leave(self, user, channel):
        """
        Wrapper around bot quit, since we have extra args per
        the plugin interface.
        """
        self.bot_instance.leave(channel, reason="Hasta la vista!")

    @classmethod
    def install(cls, bot_instance):
        plugin = cls(bot_instance)
        return {QUIT_MSG: plugin.leave}
