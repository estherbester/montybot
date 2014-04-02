#! /usr/bin/env python

import sys
from twisted.internet import reactor

from mainbot import MainBotFactory

# TODO: better way to add plugins
from plugins.creative_quit import CreativeQuitPlugin
from plugins.puppy_plugin.puppy_plugin import PuppyCommandPlugin
from plugins.link_log.link_log import LinkCheckLogPlugin
from plugins.taunt_seanz import TauntSeanPlugin 
from plugins.taunt_seanz import TauntAlbertPlugin 


def _tokenize_channels(raw_str):
    channels = raw_str.split(' ')
    return [str(channel).strip() for channel in channels]


if __name__ == "__main__":
    try:
        channel_string = sys.argv[1]
        channels = _tokenize_channels(channel_string)
    except IndexError:
        print "Must indicate channels, separated by spaces in a \
            single quoted string: '#channel1 #channel2'"
    else:
        command_plugins = [PuppyCommandPlugin, CreativeQuitPlugin]       
        taunt_plugins = [TauntAlbertPlugin, TauntSeanPlugin]
        message_plugins = [LinkCheckLogPlugin]

        reactor.connectTCP('irc.freenode.net',
                            6667,
                            MainBotFactory(channels,
                                           command_plugins,
                                           message_plugins,
                                           taunt_plugins,
										   nickname="puppybot"))
        reactor.run()
