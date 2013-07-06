import flickr
from random import randint
from random import choice

from secret_settings import API_KEY
from secret_settings import API_SECRET

from throttler import Throttler

flickr.API_KEY = API_KEY
flickr.API_SECRET = API_SECRET
PHOTOS_PER_PAGE = 20

# Need the NSID of whatever group you're pulling from
GROUPS = {
    'corgi': '42653350@N00',
    'pug': '57017533@N00',
    'doxy': '52240151476@N01',
    'puppy': '35034344814@N01'
}


class PupCommand(object):
    reply_string = "{prefix}: {msg}"

    puppies = {
        'puppy': "Puppy lottery!",
        'corgi': "OMG corgi!",
        'pug': "Pug for you",
        'doxy': "Dachshund time"
    }

    throttler = Throttler('flickr')

    def __init__(self, puppy_type):
        self.puppy_type = puppy_type
        self.group = flickr.Group(GROUPS.get(puppy_type, GROUPS['puppy']))

    def __call__(self):
        prefix = self.puppies.get(self.puppy_type, 'puppy')
        link = self.fetch()
        return self.reply_string.format(prefix=prefix, msg=link)

    def fetch(self):
        photo = None
        counter = 1
        while photo is None and counter < 3:
            try:
                random_page = self._select_random_page()
                photo = self._random_photo(random_page)
            except (AttributeError, flickr.FlickrError) as e:
                print "Error: %s" % e
                counter += 1

        # This could be better
        if photo is None:
            # Since we failed at randomizing just get one from the first page of results
            print "Randomized fetching failed. Getting one from the front page"
            photo = self._random_photo(1, 100)
        try:
            return self._get_photo_url(photo)
        except flickr.FlickrError:
            return "Sorry, no puppy for you =("

    def _select_random_page(self, per_page=PHOTOS_PER_PAGE):
        number_of_pages = self.group.poolcount / per_page
        return randint(1, number_of_pages)

    def _random_photo(self, page_number, per_page=PHOTOS_PER_PAGE):
        # Trying to randomize the fetch a bit, limited by the number of photos in the group

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
        command = PupCommand(group)
        print command()
    except IndexError:
        print "Please specify a group"
