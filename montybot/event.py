#! /usr/bin/env python

import sys
from twisted.internet import reactor

from mainbot import MainBotFactory

# TODO: better way to add plugins
from plugins.creative_quit import CreativeQuitPlugin
from plugins.puppy_plugin.puppy_plugin import PuppyCommandPlugin
from plugins.link_log.link_log import LinkCheckLogPlugin
from plugins.taunt_user import SeanzResponse 
from plugins.taunt_user import AlbertResponse 

def _tokenize_channels(raw_str):
    channels = raw_str.split(' ')
    return [str(channel).strip() for channel in channels]

def _print_instr():
    print """
    To run this, you need to provide the path to the 
    config file (like irc_credentials.ini). You must 
    also indicate channels, separated by spaces in a 
    single quoted string.

    Example: 
    $ python event.py irc_credentials.ini '#channel1 #channel2'
    """ 

if __name__ == "__main__":
    
    try:
        me, config_file, channel_string = sys.argv
        channels = _tokenize_channels(channel_string)
    except (ValueError, IndexError) as error:
        _print_instr()
    else:
        command_plugins = [PuppyCommandPlugin, CreativeQuitPlugin]       
        taunt_plugins = [SeanzResponse]
        message_plugins = [LinkCheckLogPlugin]

        reactor.connectTCP('irc.freenode.net',
                            6667,
                            MainBotFactory(config_file, 
                                           channels,
                                           command_plugins,
                                           message_plugins,
                                           taunt_plugins,
                                           ))
        reactor.run()
