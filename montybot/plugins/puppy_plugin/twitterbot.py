
import requests

import tweepy
from tweepy.error import TweepError

from .secret_settings import TWITTER_KEY
from .secret_settings import TWITTER_SECRET
from .secret_settings import TWITTER_ACCESS_TOKEN
from .secret_settings import TWITTER_ACCESS_SECRET

class TwitterBot(object):
    """ singleton class that tweets stuff """
    tbot_instance = None
     

    def __init__(self):
        self.api = None
        """ verify we are not rate limiting. """
        self.authenticate()

    def authenticate(self):
        try:

            auth = tweepy.OAuthHandler(TWITTER_KEY, TWITTER_SECRET)
            # TODO: create methods to fetch these in case we don't have direct access
            auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
        except (NameError, TweepError) as error:
            TWEET_RESULT = false
            print "Could not authenticate: %s. Not tweeting" % (error,)
        else:
            self.api = tweepy.API(auth)

    @classmethod
    def get_instance(cls):
        """ 
        return an instance, or if non exists, craete it. 
        a cheapass singleton
        """
        if cls.tbot_instance is None:
            cls.tbot_instance = cls()
        return cls.tbot_instance

    def _send_tweet(self, category, url):
        """
        send the update.
        """
        status_msg = "%s: %s " % (category, url)
        update = self.api.update_status(status_msg)
        print "Tweeted %s" % (update.text,)

    def tweet(self, category,  photo):
        """
        Theory: you can construct a proper flickr link from the photo.
        
        http://www.flickr.com/photos/smemon/5635400338/
        Constructing url by User ID and Photo ID will always work even if user name doesn't.
        :param category: bot category of photo retrieved
        :type category: String
        :param photo: The flickr Photo object. TODO: make more abstract?
        :type photo: flickr.Photo
        """
        flickr_url_format = "http://www.flickr.com/photos/{user_id}/{photo_id}/"

        url = flickr_url_format.format(user_id=photo.owner.id, photo_id=photo.id)
        self._send_tweet(category, url)


def tweet_result(group, result):
    try:
        tbot = TwitterBot.get_instance()
        tbot.tweet(group, result)
    except (TweepError, Exception) as error:
        print error
        raise

if __name__ == "__main__":
    from mock import Mock
    test_group = "pug"
    test_phrase = "http://farm6.static.flickr.com/5141/5599874146_257c95967d_z.jpg"
    mock_photo = Mock()
    mock_photo.owner = "estherbester"
    mock_photo.id = '13895344866'
    tweet_result(test_group, mock_photo)