import flickr

from collections import namedtuple

from random import randint
from random import choice

from secret_settings import API_KEY
from secret_settings import API_SECRET

from throttler import Throttler

PuppyCommand = namedtuple('PuppyCommand', ['puppy_type',
                                           'command',
                                           'flickr_group_id',
                                           'reply_prefix'])

GENERIC = PuppyCommand('puppy', 'puppy lottery', '35034344814@N01', "Puppy lottery!")
PUG = PuppyCommand('pug', 'pug please', '57017533@N00', "Pug for you")
CORGI = PuppyCommand('corgi', 'corgi time', '42653350@N00', "OMG corgi!")
DOXY = PuppyCommand('doxy', 'hotdog', '52240151476@N01', "Dachshund time")

AVAILABLE_COMMANDS = [GENERIC, PUG, CORGI, DOXY]

flickr.API_KEY = API_KEY
flickr.API_SECRET = API_SECRET
PHOTOS_PER_PAGE = 20
MAX_API_CALLS = 60


# Need the NSID of whatever group you're pulling from
GROUPS = {
    pc.puppy_type: pc.flickr_group_id for pc in AVAILABLE_COMMANDS
}

REPLIES = {
    pc.puppy_type: pc.reply_prefix for pc in AVAILABLE_COMMANDS
}


class PuppyFetch(object):
    reply_string = "{prefix}: {msg}"

    throttler = Throttler('flickr', MAX_API_CALLS)

    def __init__(self, puppy_type):
        self.puppy_type = puppy_type
        self.group = flickr.Group(GROUPS[puppy_type])

    @classmethod
    @throttler.track
    def get(cls, puppy_type):
        try:
            command = cls(puppy_type)
            prefix = REPLIES[puppy_type]
            result = command._get_url()
        except KeyError, flickr.FlickrError:
            result = "Sorry, no puppy for you =("
        return command.reply_string.format(prefix=prefix, msg=result)

    def _get_url(self):
        photo = None
        counter = 1
        while photo is None and counter < 3:
            try:
                random_page = self._select_random_page()
                photo = self._select_random_photo(random_page)
            except (AttributeError, flickr.FlickrError) as e:
                print "Error: %s" % e
                counter += 1

        # This could be better
        if photo is None:
            # Since we failed at randomizing just get one from the first
            # page of results
            print "Randomized fetching failed. Getting one from the front page"
            photo = self._select_random_photo(1, 100)
        return self._get_photo_url(photo)

    def _select_random_page(self, per_page=PHOTOS_PER_PAGE):
        """ Pick a page, any page. """
        number_of_pages = self.group.poolcount / per_page
        return randint(1, number_of_pages)

    def _select_random_photo(self, page_number, per_page=PHOTOS_PER_PAGE):
        # Trying to randomize the fetch a bit, limited by the number of photos
        # in the group
        photos = self.group.getPhotos(per_page=per_page,
                                      page=page_number)
        return choice(photos)

    def _get_photo_url(self, photo, size="Medium"):
        method = 'flickr.photos.getSizes'
        data = flickr._doget(method, photo_id=photo.id)
        return self._get_resized(data, size)
        raise flickr.FlickrError, "No URL found"

    def _get_resized(self, data, size):
        for psize in data.rsp.sizes.size:
            if psize.label == size:
                return psize.source


if __name__ == '__main__':
    import sys
    try:
        group = sys.argv[1]
        command = PuppyFetch.get(group)
        print command
    except IndexError:
        print "Please specify a group"
