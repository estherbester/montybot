from .metaclass import PluginMetaClass

from random import choice

from .puppy_plugin.secret_settings import API_KEY
from .puppy_plugin.secret_settings import API_SECRET

import puppy_plugin.flickr as flickr
flickr.API_KEY = API_KEY
flickr.API_SECRET = API_SECRET


class TauntSeanPlugin(object):
    __metaclass__ = PluginMetaClass

    name = "Taunt Sean plugin"

    # TODO: Not sure this is properly done (see metaclass)
    def __init__(self, bot_instance):
        self.bot_instance = bot_instance
        self.taunter_name = 'seanz'

    @classmethod
    def run(cls, user, channel, message, bot_instance):
        """ """
        self = cls(bot_instance)

        # if sean is asking
        if self._from_taunter_to_bot(user, message):
            self.bot_instance.handled = True
            self._run(user, channel, message)

    def _from_taunter_to_bot(self, user, message):
        return user.startswith(self.taunter_name) and message.startswith(self.bot_instance.nickname)

    def _run(self, user, channel, message):
        # pick a random image
        url = "http://www.aston-pharma.com/bionic-animals/images/12-bionic-animals/kvcgj7E.jpg"
        self.bot_instance.msg(channel, "%s: is this what you wanted? %s" % (self.taunter_name, url))



class TauntAlbertPlugin(TauntSeanPlugin):
    __metaclass__ = PluginMetaClass

    name = "Taunt Albert plugin"

    # TODO: Not sure this is properly done (see metaclass)
    def __init__(self, bot_instance):
        self.bot_instance = bot_instance
        self.taunter_name = 'hairyasian'

    def _run(self, user, channel, message):

        try:
            # pick a random image
            albert_pic = self._photo_from_set()
                # This could be better
            if albert_pic is None:
                # Since we failed at randomizing just get one from the first
                # page of results
                print "Randomized fetching failed."
                url = ""
            else:
                url = self._get_photo_url(albert_pic)
                print url
            self.bot_instance.msg(channel, "Herro: %s" % url.encode())
        except Exception as error:
            print error

    def _photo_from_set(self):
        set_name = flickr.Photoset('72157643064772885')
        photos = set_name.getPhotos()
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

if __name__=="__main__":
    from mock import Mock
    bot_instance = Mock()
    try:
        bot_instance.msg = Mock(return_value='foo')
        sean_instance = TauntSeanPlugin.run('foo', 'bar', 'message', bot_instance)
        f = TauntAlbertPlugin.run('foo', 'bar', 'message', bot_instance)
    except Exception as error:
        print error
