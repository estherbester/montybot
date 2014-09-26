# Class that uses Flickr to fetch photos of dogs

from random import randint
from random import choice

import flickr

from .secret_settings import API_KEY
from .secret_settings import API_SECRET
from .secret_settings import TWEET_RESULT

from ..throttler import Throttler
from ..plugin_config import AVAILABLE_COMMANDS
from ..plugin_config import PHOTOS_PER_PAGE
from ..plugin_config import MAX_API_CALLS


# Need the NSID of whatever group you're pulling from
GROUPS = {
    pc.puppy_type: pc.flickr_group_id for pc in AVAILABLE_COMMANDS
}

REPLIES = {
    pc.puppy_type: pc.reply_prefix for pc in AVAILABLE_COMMANDS
}

flickr.API_KEY = API_KEY
flickr.API_SECRET = API_SECRET


class PuppyFetch(object):
    """
    TODO: 

    * make fewer API calls
    * Rename since we don't just get puppies
    """
    reply_string = "{prefix}: {msg}"

    # not going to throttle twitter since this should take care of both.
    throttler = Throttler('flickr', MAX_API_CALLS)

    def __init__(self, puppy_type):
        self.puppy_type = puppy_type
        self.group = flickr.Group(GROUPS[puppy_type])

    @classmethod
    @throttler.track
    def get(cls, puppy_type):
        message = "Sorry, can't get an image =("
        try:
            command = cls(puppy_type)
            prefix = REPLIES[puppy_type]
            print "fetching url"
            result = command._get_flickr_photo()
            photo_url = cls.get_photo_url(result)
            message = command.reply_string.format(prefix=prefix, msg=photo_url)
        except (NameError, KeyError, flickr.FlickrError) as error:
            print "Error in PuppyFetch: %s" % error
        else:
            # TODO: this should not be a blocking call.
            if TWEET_RESULT:
                from .twitterbot import tweet_result, TweetBotError
                try:
                    tweet_result(puppy_type, result)
                except TweetBotError as error:
                    print "Tweetbot error: %s" % error
        return message

    def _get_flickr_photo(self):
        """ 
        a flickr Photo object looks like this::

            photo.id, 
            owner=owner, 
            title=title, 
            ispublic=ispublic,
            isfriend=isfriend, 
            isfamily=isfamily, 
            secret=secret, 
            server=server

        :returns: flickr.photo object 
        """
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
        return photo

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

    @staticmethod
    def get_photo_url(photo):
        """ 
        we default to medium as it works well most times; getLarge and 
        getSmall work too. 
        """
        url = photo.getMedium()
        if url:
            return url
        raise flickr.FlickrError, "No URL found"
        

class FlickrRandomizer(object):
    """
    Given a group of flickr photos, pick a random one.
    * A group could be a set, a user, or a group
    """
    def __init__(self, collection):
        self.collection = collection



if __name__ == '__main__':
    import sys
    try:
        group = sys.argv[1]
        command = PuppyFetch.get(group)
        print command
    except IndexError:
        print "Please specify a group"
