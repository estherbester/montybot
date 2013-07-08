from collections import deque
from datetime import datetime
from datetime import timedelta

from twisted.internet.task import LoopingCall

# generic defaults
MAX_CALLS = 60
MAX_TIMEOUT = 1  # in hours
CHECK_INTERVAL = 60.0  # in seconds


class Throttler(object):
    throttler_for = None

    def __init__(self, throttler_for,
                 max_calls=MAX_CALLS,
                 max_timeout=MAX_TIMEOUT,
                 interval=CHECK_INTERVAL):

        print "Enabled throttling for %s: max %s per hour" %\
         (throttler_for, max_calls)

        self.throttler_for = throttler_for
        self.max_calls = max_calls
        self.max_timeout = max_timeout
        self.interval = interval

        self.tracker = deque([], max_calls)
        self._init_throttle()

    def track(self, func):
        """
        Decorator function to check the tracker before calling the
        passed-in function. Returns a status message if we have reached
        the threshold.
        """
        def do_tracking(*args):
            if len(self.tracker) < self.tracker.maxlen:
                self.tracker.append(datetime.now())
                return func(*args)

            else:
                return "Hit the limit for %s" % (self.throttler_for,)
        return do_tracking

    def _init_throttle(self):
        self.throttler = LoopingCall(self._check_throttle)
        self.throttler.start(self.interval)

    def _check_throttle(self):
        try:
            # if first item is too recent, leave it. otherwise remove it.
            if self._is_expired(self.tracker[0]):
                self.tracker.popleft()
        except IndexError:
            pass

    def _is_expired(self, item):
        check_time = datetime.now()
        past_length = timedelta(hours=self.max_timeout)
        return past_length > (check_time - item)


if __name__ == '__main__':

    th = Throttler('test', max_calls=5)
    from time import sleep

    @th.track
    def howdy():
        return "a"

    while True:
        sleep(1)
        print howdy()
