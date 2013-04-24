#! /usr/bin/env python
# -*- coding: utf-8 -*-
# idea for this stolen from jslabot

# records links posted in the channel

import re
import requests

from BeautifulSoup import BeautifulSoup
from datetime import datetime

LINK_LOG_FILE = 'links_in_channel.txt'


def detect_hyperlinks(irc_message):
    """
    Returns any found, working hyperlinks in an irc message
    """
    # a dirty simple regex from django linkify filter
    regex = re.compile(r'(([a-zA-Z]+)://[^ \t\n\r]+)', re.MULTILINE)
    message_text = irc_message.arguments[0]
    matches = regex.findall(message_text)
    return check_hyperlinks(matches, irc_message.source.nick)


def check_hyperlinks(matches, source):
    """
    Given a list of links, checks to see if the link works. Returns
    a list of metadata strings, one for each link.
    """
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
        """
        We have a url, the user who posted the url, and the time we look up the url
        """
        self.url = url
        self.user = user
        self.timestamp = datetime.strftime(datetime.now(), '%h %d %X')

    def log(self, line):
        with open(LINK_LOG_FILE, 'a') as link_log:
            # should record time link was posted but whatever.
            link_log.write("\r%s" % line)

    def get_page_title(self, page_content):
        """Given a link, scrape the title"""
        soup = BeautifulSoup(page_content)
        return soup.find('title').text.encode('ascii', 'replace')

    def check(self):
        note = "[no content]"
        try:
            site = requests.get(self.url)
            if site.status_code == 200:
		if site.headers['content-type'].startswith('image'):
			note = '[image]'
		else:
			note = self.get_page_title(site.content)
            else:
        	raise requests.exceptions.RequestException("Fetch not successful")
	except requests.exceptions.RequestException:
            note = "[link failed]"
        except AttributeError:
            pass
        finally:
            line = u"%s (%s): %s | %s" % (self.user, self.timestamp, self.url, note)
            self.log(line)
        return u"%s | %s" % (self.url, note)


if __name__ == "__main__":
    #link = Link('http://esthernam.com/', 'estherbester')

    class MockMessage(object):
        class Source(object):
            nick = "MockSource"

        source = Source()
        arguments = ['Test message with hyperlink like http://1.bp.blogspot.com/_OYjskRx08bY/SQcsZcVmI6I/AAAAAAAACtQ/dZhWPhgrLs8/s1600/PhoebeandLaura.jpg',] 

    mock_message = MockMessage()
    print detect_hyperlinks(mock_message)
