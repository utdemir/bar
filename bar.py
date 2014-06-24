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

_templates = {
    "detailed": "[{bar}] %{percentage:.2f} ({step}/{max}) Elapsed: {seconds:.0f}s ETA: {eta:.0f}s",
    "timer": "{seconds:.0f}s"
}

class Bar:
    _nest_count = 0

    def __init__(self, subject="",
                 max=None, bar_width=20, template="detailed",
                 end="Done in {seconds:.2f} seconds.",
                 chars="block"):
        self.subject = subject
        self.max = max
        self.bar_width = bar_width
        self.template = _templates[template]
        self.end = end

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
        max = self.max
        completed = step / max
        percentage = completed * 100
        seconds = now - self._started_at

        eta = (seconds / step) * (max - step) if step else 0

        # Progress Bar
        full_bar_count, rem = divmod(completed * self.bar_width, 1)
        bar = int(full_bar_count) * self.chars[-1]
        bar += self.chars[int(rem * len(self.chars))]
        bar += self.chars[0] * (self.bar_width - len(bar))

        line = self.subject + self.template.format(**locals())
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
        if self.end is not None:
            seconds = time.time() - self._started_at
            self._overwrite(self.subject + self.end.format(**locals()))
        print()
