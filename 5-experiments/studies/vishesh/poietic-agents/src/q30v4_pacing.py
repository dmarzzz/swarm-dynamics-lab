"""Minimum provider-start interval, independent of worker and provider latency."""
import time


class Pacer:
    def __init__(self, clock=time.monotonic, wall=time.time, sleep=time.sleep):
        self.clock, self.wall, self.sleep = clock, wall, sleep
        self.last = None

    def wait(self, deadline):
        while self.last is not None and self.clock() - self.last < 5:
            delay = 5 - (self.clock() - self.last)
            if self.wall() + delay >= deadline:
                raise ValueError('paced_dispatch_deadline')
            self.sleep(delay)
        if self.wall() >= deadline:
            raise ValueError('paced_dispatch_deadline')
        self.last = self.clock()
