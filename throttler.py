from datetime import datetime
from datetime import timedelta
import threading

from collections import deque


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

if __name__ == '__main__':
    pass
