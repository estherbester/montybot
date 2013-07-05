#! /usr/bin/env python
# -*- coding: utf-8 -*-
# idea for this stolen from jslabot

# records links posted in the channel

import re

from irc_logger import IRCLogger
from link import Link
from plugin_metaclass import PluginMetaClass

# Configuration is done here
LOG_LINKS = True
LINK_LOG_FILE = 'links_in_channel.txt'


class LinkCheckLogPlugin(object):
    __metaclass__ = PluginMetaClass

    name = "Link checker with log"
    logging_enabled = LOG_LINKS
    logger = None

    def __init__(self):
        """ Instantiates logger if logging is enabled """
        if self.logging_enabled:
            print "Logging is enabled for Link checker"
            self.logger = IRCLogger(LINK_LOG_FILE)

    @classmethod
    def run(cls, user, message, bot_instance):
        """ """
        instance = cls()
        # if it looks like there might be a link we want
        if 'http' in message:
            instance._run(user, message, bot_instance)

    def _run(self, user, message, bot_instance):
        # check for links
        for link in self._scrape_links(user, message):
            # TODO: this sucks.
            bot_instance.msg(bot_instance.factory.channel,
                 link.formatted_string)

    def _scrape_links(self, user, message):
        """ Return any found, working hyperlinks in an irc message. """
        # a dirty simple regex from django linkify filter
        regex = re.compile(r'(([a-zA-Z]+)://[^ \t\n\r]+)', re.MULTILINE)
        matches = regex.findall(message)
        return (link for link in self._check_hyperlinks(matches, user))

    def _check_hyperlinks(self, matches, user):
        """
        Given a list of links, checks to see if the link works. Returns
        a list of metadata strings, one for each link.
        returns: generator of link objects with associated text.
        """
        try:
            for match, group1 in matches:
                if match:
                    print "Link detected: %s" % (match,)
                    new_link = Link(match)
                    if new_link.is_valid():
                        if self.logging_enabled:
                            self.logger.log(new_link, user)
                        yield new_link
        except (TypeError, AttributeError) as error:
            print "Hyperlink borked: %s" % error


if __name__ == "__main__":
    arguments = \
['Test message with hyperlink like http://flickr.com and also http://nytimes.com', ]

    from mock import Mock

    mock_bot = Mock()
    mock_bot.factory = Mock()
    mock_bot.factory.channel = "#scoobydoo"
    mock_bot.msg = Mock(return_value='oo')

    LinkCheckLogPlugin.run('test', arguments[0], mock_bot)

