#! /usr/bin/env python
import sys
from twisted.internet import reactor

from mainbot import MainBotFactory

# TODO: better way to add plugins
from puppy import PuppyCommandPlugin
from link_log import LinkCheckLogPlugin

QUIT_MSG = "go home, you're drunk"


class CreativeQuitPlugin(object):
    name = "Creative quit plugin"

    def __init__(self, bot_instance):
        self.bot_instance = bot_instance

    @classmethod
    def install(cls, bot_instance):
        cls.__init__(bot_instance)
        return {QUIT_MSG: bot_instance.quit}


if __name__ == "__main__":
    try:
        chan = sys.argv[1]
    except IndexError:
        print "required arg: '#channel'"
    else:
        command_plugins = [PuppyCommandPlugin, CreativeQuitPlugin]
        message_plugins = [LinkCheckLogPlugin]
        reactor.connectTCP('irc.freenode.net',
                            6667,
                            MainBotFactory(str(chan),
                                           command_plugins,
                                           message_plugins))
        reactor.run()

