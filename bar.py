#-*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys
import time
import threading
import contextlib
import unicodedata

_chars = {
    "block": "  ▏▎▍▌▋▊▉█",
    "shades": " ░▒▓█",
    "ascii": " -=#"
}

class Bar:
    DETAILED = "[{bar}] %{percentage:.2f} ({step}/{bar_max}) Elapsed: {seconds:.0f}s ETA: {eta:.0f}s"
    ONLY_TIMER = "{seconds:.0f}s"

    _nest_count = 0

    def __init__(self, subject="",
                 bar_max=None, bar_width=20, bar_template=DETAILED,
                 end=False, end_template="Done in {seconds:.2f} seconds.",
                 chars="block"):
        self.subject = subject
        self.bar_max = bar_max
        self.bar_width = bar_width
        self.bar_template = bar_template
        self.end = end
        self.end_template = end_template

        self._step = 0
        self._last_update = 0
        self._started_at = time.time()
        self._max_length = 0

        self.timer = None

        self.chars = _chars[chars]

    def step(self, times=1):
        self._step += times
        self.update_bar()

    def cancel(self):
        self.__exit__()

    def _overwrite(self, line):
        print("\r" + line + ' ' * max(0, self._max_length - len(line)), end="")
        sys.stdout.flush()
        self._max_length = max(self._max_length, len(line))

    def _tick(self):
        if self.timer is not None:
            self.update_bar()
        self.timer = threading.Timer(1, self._tick)
        self.timer.start()

    def update_bar(self, force=False):
        now = time.time()
        if now - self._last_update < 0.1 and not force:
            return
        self._last_update = now

        step = self._step
        bar_max = self.bar_max
        completed = step / bar_max
        percentage = completed * 100
        seconds = now - self._started_at

        eta = (seconds / step) * (bar_max - step) if step else 0

        # Progress Bar
        full_bar_count, rem = divmod(completed * self.bar_width, 1)
        bar = int(full_bar_count) * self.chars[-1]
        bar += self.chars[int(rem * len(self.chars))]
        bar += self.chars[0] * (self.bar_width - len(bar))

        line = self.subject + self.bar_template.format(**locals())
        self._overwrite(line)

    def __enter__(self):
        self.update_bar(force=True)
        self._nest_count += 1
        self._tick()
        return self

    def __exit__(self, *args):
        self.timer.cancel()
        self.update_bar(force=True)
        self._nest_count -= 1
        if self.end:
            seconds = time.time() - self._started_at
            self._overwrite(self.subject + self.end_template.format(**locals()))
        print()
