#! /usr/bin/env python
# -*- coding: utf-8 -*-
# stole from jsla bot the regex to find a url: /(http|ftp|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?/i,

# record links posted in the channel

import re
import requests

from BeautifulSoup import BeautifulSoup
from datetime import datetime

LINK_LOG_FILE = 'links_in_channel.txt'


def detect_hyperlinks(irc_message):
    """
    Returns any found, working hyperlinks
    """
    # a dirty simple regex from django linkify filter
    regex = re.compile(r'(([a-zA-Z]+)://[^ \t\n\r]+)', re.MULTILINE)
    message_text = irc_message.arguments[0].split(":", 1)[1]
    matches = regex.findall(message_text)
    return check_hyperlinks(matches, irc_message.source.nick)


def check_hyperlinks(matches, source):
    found_link = None
    links_to_post = []
    try:
        for match, group1 in matches:
            print "Link found: %s " % match
            found_link = match
            if found_link:
                new_link = Link(found_link, source)
                link_info = new_link.check()
                links_to_post.append(link_info)
    except (TypeError, AttributeError) as error:
        print "Hyperlink borked: %s" % error
    return links_to_post


class Link(object):
    def __init__(self, url, user):
        self.url = url
        self.user = user
        self.timestamp = datetime.strftime(datetime.now(), '%h %d %X')

    def log(self, line):
        with open(LINK_LOG_FILE, 'a') as link_log:
            # should record time link was posted but whatever.
            link_log.write("\r%s" % line)

    def check(self):
        try:
            site = requests.get(self.url)
            if site.status_code == 200:
                soup = BeautifulSoup(site.content)
                note = soup.find('title').text.encode('ascii', 'replace')
            else:
                note = "[link failed]"
        except requests.exceptions.RequestException:
            note = "[link failed]"
        except AttributeError:
            note = "[no content]"
        finally:
            line = u"%s (%s): %s | %s" % (self.user, self.timestamp, self.url, note)
            self.log(line)
        return u"%s | %s" % (self.url, note)


if __name__ == "__main__":
    link = Link('http://github.com', 'estherbester')
    print link.check()
