# TODO: This sucks.
from datetime import datetime
from datetime import timedelta

from collections import deque
from get_puppy import get_puppy
import threading


class Throttler(object):
    max_calls = 80
    throttler_for = None

    def __init__(self, throttler_for):
        self.throttler_for = throttler_for
        self.tracker = deque([], self.max_calls)
        self.check_throttle()

    def check_throttle(self):
        throttler = threading.Timer(60.0, self.dequeue)
        try:
            # if first item is less than an hour, leave it. otherwise
            # remove it.
            if self._is_expired(self.tracker[0]):
                self.tracker.popleft()
        except IndexError:
            pass
        throttler.start()

    def _is_expired(self, item):
        past_hour = timedelta(hours=1)

        return item < (datetime.now() - past_hour)

    def track(self, func):
        if self.tracker.count < self.tracker.maxlen:
            return func()
        else:
            return "Hit the limit for %s" % self.throttler_for,


class PuppyCommandPlugin(object):
    """
    Commands to respond to for puppy links
    """
    name = 'Puppy Commands'

    MAX_CALLS = 80
    throttler = None

    #@throttler.track
    def puppy():
        return "Puppy time! %s" % get_puppy('puppies')

    #@throttler.track
    def corgi():
        return "OMG corgi! %s" % get_puppy('corgies')

    #@throttler.track
    def pug():
        return "Pug for you: %s" % get_puppy('pugs')

    #@throttler.track
    def doxy():
        return "Dachshund time: %s" % get_puppy('doxies')

    commands = {
        'puppy time': puppy,
        'corgi time': corgi,
        'pug please': pug,
        'hotdog': doxy
    }

    @classmethod
    def install(cls):
        #cls.throttler = Throttler('flickr')
        return cls.commands
