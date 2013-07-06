from datetime import datetime
from datetime import timedelta
import threading

from collections import deque

MAX_CALLS = 80
MAX_TIMEOUT = 1  # in hours
CHECK_INTERVAL = 60.0  # in seconds


class Throttler(object):
    throttler_for = None

    def __init__(self, throttler_for, max_calls=MAX_CALLS):
        self.throttler_for = throttler_for
        self.tracker = deque([], max_calls)
        self.check_throttle()

    def check_throttle(self):
        throttler = threading.Timer(CHECK_INTERVAL, self.check_throttle)
        try:
            # if first item is too recent, leave it. otherwise remove it.
            if self._is_expired(self.tracker[0]):
                self.tracker.popleft()
        except IndexError:
            pass
        throttler.start()

    def _is_expired(self, item):
        check_time = datetime.now()
        past_length = timedelta(hours=MAX_TIMEOUT)
        return past_length > (check_time - item)

    def track(self, func):

        def do_tracking(*args):
            if len(self.tracker) < self.tracker.maxlen:
                self.tracker.append(datetime.now())
                return func(*args)

            else:
                return "Hit the limit for %s" % (self.throttler_for,)
        return do_tracking

if __name__ == '__main__':

    th = Throttler('test', max_calls=5)
    from time import sleep

    @th.track
    def howdy():
        return "a"

    while True:
        sleep(1)
        print howdy()
