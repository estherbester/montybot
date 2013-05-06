#! /usr/bin/env python
# -*- coding: utf-8 -*-

import irc.bot
import irc.strings
from irc.client import ip_numstr_to_quad
from irc.client import ip_quad_to_numstr

from get_puppy import get_puppy
from get_puppy import FLICKR_GROUP 
from get_puppy import PUG_GROUP 

from link_log import detect_hyperlinks


class MontyBot(irc.bot.SingleServerIRCBot):
    def __init__(self, channel, nickname, server, port=6667, check_links=False):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.channel = channel
        self.check_links = check_links

    def post_link(self, c, link_info):
        c.privmsg(self.channel, link_info)

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        c.join(self.channel)

    def on_privmsg(self, c, e):
        self.do_command(e, e.arguments[0])

    def on_pubmsg(self, c, e):
        msg = e.arguments[0]
        # to help us see if message begins with a nick (which would be a[0])
        # a[1] would be the rest of the message
        a = msg.split(":", 1)
        if len(a) > 1:
            if self.is_myself(a[0]):
                self.do_command(e, a[1].strip())
            else:
                # if it looks like there might be a link we want
                if self.check_links and 'http' in msg:
                    # check for links
                    working_links = detect_hyperlinks(e)
                    for link_data in working_links:
                        self.post_link(c, link_data)
        return

    def is_myself(self, message_first_part):
        my_nickname = irc.strings.lower(self.connection.get_nickname())
        #return irc.strings.lower(message_first_part) == my_nickname
        return my_nickname in irc.strings.lower(message_first_part)

    def on_dccmsg(self, c, e):
        c.privmsg("You said: " + e.arguments[0])

    def on_dccchat(self, c, e):
        if len(e.arguments) != 2:
            return
        args = e.arugments[1].split()
        if len(args) == 4:
            try:
                address = ip_numstr_to_quad(args[2])
                port = int(args[3])
            except ValueError:
                return
            self.dcc_connect(address, port)

    def do_command(self, e, cmd):
        nick = e.source.nick
        c = self.connection

        if cmd == 'disconnect':
            self.disconnect()
        elif cmd == 'go away':
            self.die()
        elif 'puppy time' in cmd.lower():
            puppy_url = get_puppy(FLICKR_GROUP)
            c.privmsg(self.channel, "Puppy time! " + puppy_url)
        elif 'pug please' in cmd.lower():
            puppy_url = get_puppy(PUG_GROUP)
            c.privmsg(self.channel, "Pug for you " + puppy_url)
        elif cmd == 'dcc':
            dcc = self.dcc_listen()
            c.ctcp("DCC", nick, "CHAT chat %s %d" % (
                ip_quad_to_numstr(dcc.localaddress), dcc.localport))
        else:
            c.notice(nick, "Not understood: " + cmd)


def main():
    import sys
    print sys.argv
    if len(sys.argv) < 4:
        print "Usage: montybot <server[:port]> \"<channel>\" <nickname> <detect_links? True|False>"
        sys.exit(1)

    s = sys.argv[1].split(":", 1)
    server = s[0]
    if len(s) == 2:
        try:
            port = int(s[1])
        except ValueError:
            print "Error: erroneous port."
            sys.exit(1)
    else:
        port = 6667
    channel = sys.argv[2]
    nickname = sys.argv[3]
    if sys.argv[4] == "True":
        check_links = True
    else:
        check_links = False

    bot = MontyBot(channel, nickname, server, port, check_links)
    bot.start()


if __name__ == "__main__":
    main()
