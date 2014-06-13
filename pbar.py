from __future__ import division
from __future__ import print_function

import sys
import time
import contextlib

class Bar:
    DETAILED = "[{bar}] %{percentage:.2f} ({step}/{bar_max}) {seconds:.0f}s"
    ONLY_TIMER = "{seconds:.0f}s"
    
    _nest_count = 0

    def __init__(self, subject="",
                 bar_max=None, bar_width=20, bar_char='#',
                 bar_template=DETAILED,
                 end=False, end_template="Done in {seconds:.2f} seconds.",
                 indent=False, indent_char=' '):
        self.subject = subject
        self.bar_max = bar_max
        self.bar_width = bar_width
        self.bar_char = bar_char
        self.bar_template = bar_template
        self.end = end
        self.end_template = end_template

        self._step = 0
        self._last_update = 0 
        self._started_at = time.time()
        self._max_length = 0

    def step(self, times=1):
        self._step += times
        self.update_bar()

    def _overwrite(self, line):
        print("\r" + line + ' ' * max(0, self._max_length - len(line)), end="")
        sys.stdout.flush()
        self._max_length = max(self._max_length, len(line))

    def update_bar(self, force=False):
        now = time.time()
        if now - self._last_update < 0.2 and not force:
            return
        self._last_update = now
	
        step = self._step
        bar_max = self.bar_max
        completed = step / bar_max
        bar_count = int(round(completed * self.bar_width))
        bar = (self.bar_char * bar_count) \
                 + ' ' * (self.bar_width - bar_count)
        percentage = completed * 100
        seconds = now - self._started_at

        line = self.subject + self.bar_template.format(**locals())
        self._overwrite(line)

    def __enter__(self):
        self._nest_count += 1
        return self

    def __exit__(self, *args):
        self._nest_count -= 1
        if self.end:
            seconds = time.time() - self._started_at
            self._overwrite(self.subject + self.end_template.format(**locals()))
        print()
