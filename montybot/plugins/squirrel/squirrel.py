# -*- coding: utf-8 -*-
# idea for this stolen from jslabot
# requires puppybot plugin


from ..metaclass import PluginMetaClass

from ..puppy_plugin.get_puppy import PuppyFetch





class DisruptiveSquirrelPlugin(object):
    __metaclass__ = PluginMetaClass
    name = "SQUIRREL!"

    # TODO: Not sure this is properly done (see metaclass)
    def __init__(self):
        """ Instantiate the squirrel photo fetcher """ 
        pass 

    @classmethod
    def run(cls, user, channel, message, bot_instance):
        """ """
        instance = cls()
        # if it looks like there might be a link we want
        if 'squirrel' in message.lower() and user != bot_instance.nickname:
            bot_instance.handled = True
            instance._run(user, channel, message, bot_instance)

    def _run(self, user, channel, message, bot_instance):
        # get a squirrel pancake
        squirrel_reply = PuppyFetch.get('squirrel')
        bot_instance.msg(channel, squirrel_reply)

if __name__ == "__main__":
    from mock import Mock

    def mock_msg(chan, msg):
        print chan
        print msg
    
    bot_instance = Mock()
    bot_instance.msg = mock_msg
    from ..puppy_plugin.puppy_plugin import PuppyCommandPlugin
    pcp = PuppyCommandPlugin.install(bot_instance)

    DisruptiveSquirrelPlugin.run('test', '#scoobydoo', "no squirrels here", bot_instance)
