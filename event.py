#! /usr/bin/env python
import sys
from twisted.internet import reactor

from mainbot import MainBotFactory

# TODO: better way to add plugins
from creative_quit import CreativeQuitPlugin
from puppy_plugin import PuppyCommandPlugin
from link_log import LinkCheckLogPlugin


def tokenize_channels(raw_str):
    channels = channel_string.split(' ')
    return [str(channel).strip() for channel in channels]

if __name__ == "__main__":
    try:
        channel_string = sys.argv[1]
        channels = tokenize_channels(channel_string)
    except IndexError:
        print "Must indicate channels, separated by spaces in a \
            single quoted string: '#channel1 #channel2'"
    else:
        command_plugins = [PuppyCommandPlugin, CreativeQuitPlugin]
        message_plugins = [LinkCheckLogPlugin]

        reactor.connectTCP('irc.freenode.net',
                            6667,
                            MainBotFactory(channels,
                                           command_plugins,
                                           message_plugins))
        reactor.run()
