#! /usr/bin/env python
import sys
from twisted.internet import reactor

from mainbot import MainBotFactory

# TODO: better way to add plugins
from puppy import PuppyCommandPlugin
from link_log import LinkCheckLogPlugin

if __name__ == "__main__":
    try:
        chan = sys.argv[1]
    except IndexError:
        print "required arg: '#channel'"
    else:
        command_plugins = [PuppyCommandPlugin]
        message_plugins = [LinkCheckLogPlugin]
        reactor.connectTCP('irc.freenode.net',
                            6667,
                            MainBotFactory(str(chan),
                                           command_plugins,
                                           message_plugins))
        reactor.run()

