from datetime import datetime
from datetime import timedelta
import threading

from collections import deque


class Throttler(object):
    max_calls = 80
    max_delta = 1  # in hours
    throttler_for = None

    def __init__(self, throttler_for, max_calls=80):
        self.throttler_for = throttler_for
        self.tracker = deque([], max_calls)
        self.check_throttle()

    def check_throttle(self):
        throttler = threading.Timer(60.0, self.check_throttle)
        try:
            # if first item is less than an hour, leave it. otherwise
            # remove it.
            if self._is_expired(self.tracker[0]):
                self.tracker.popleft()
        except IndexError:
            pass
        throttler.start()

    def _is_expired(self, item):
        #past_hour = timedelta(hours=self.max_delta)
        past_length = timedelta(minutes=1)
        return item < (datetime.now() - past_length)

    def track(self, func):
        print "tracking: %s" % len(self.tracker)

        def do_tracking(*args):
            if len(self.tracker) < self.tracker.maxlen:
                return func(*args)
            else:
                return "Hit the limit for %s" % (self.throttler_for,)
        return do_tracking

if __name__ == '__main__':

    th = Throttler('test', max_calls=5)
    from time import sleep

    @th.track
    def howdy():
        print "a"

    for i in range(23):
        howdy()
