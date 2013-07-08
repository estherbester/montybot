from datetime import datetime
import requests

from BeautifulSoup import BeautifulSoup


class LinkException(Exception):
    pass


class Link(object):
    # the found link object should have info about the URL, the contents
    # (or at least the head tag), a formatted string description, and timestamp
    url = None
    content = None
    message_format = "{url} {delim} {note}"

    def __init__(self, url):
        """
        We have a url, the user who posted the url, and the time we instantiate the URL        """
        self.url = url
        self.timestamp = datetime.strftime(datetime.now(), '%h %d %X')

    def is_valid(self):
        """ If there is content, the link is considered valid. """
        try:
            self.get_content()
        # Might not need this, I can't remember why I catch this.
        except AttributeError:
            pass
        return self.content is not None

    def get_content(self):
        """ Try to fetch the URL content """
        try:
            response = requests.get(self.url)
        except requests.exceptions.RequestException:
            raise LinkException("Request failed")

        if response.status_code == 200:
            """ we get a lot of images. """
            if self.is_image(response):
                self.content = "[image]"
            else:
                self.content = response.content

    def is_image(self, response):
        return response.headers['content-type'].startswith('image')

    @property
    def text(self):
        """ Create a pretty string for the link. """
        return self.message_format.format(url=self.url,
                                          delim='|',
                                          note=self.page_title)

    @property
    def page_title(self):
        """Given a page, scrape the title"""
        if self.content == "image":
            return self.content
        try:
            soup = BeautifulSoup(self.content)
            return soup.find('title').text.encode('ascii', 'replace')
        except Exception:
            return "[Could not parse content]"

