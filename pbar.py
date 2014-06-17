from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys
import time
import contextlib
import unicodedata

_unicode_eights = [
    "", 
    unicodedata.lookup("LEFT ONE EIGHTH BLOCK"),
    unicodedata.lookup("LEFT ONE QUARTER BLOCK"),
    unicodedata.lookup("LEFT THREE EIGHTHS BLOCK"),
    unicodedata.lookup("LEFT HALF BLOCK"),
    unicodedata.lookup("LEFT FIVE EIGHTHS BLOCK"),
    unicodedata.lookup("LEFT THREE QUARTERS BLOCK"),
    unicodedata.lookup("LEFT SEVEN EIGHTHS BLOCK"),
    unicodedata.lookup("FULL BLOCK")
]

class Bar:
    DETAILED = "[{bar}] %{percentage:.2f} ({step}/{bar_max}) {seconds:.0f}s"
    ONLY_TIMER = "{seconds:.0f}s"
    
    _nest_count = 0

    def __init__(self, subject="",
                 bar_max=None, bar_width=20, 
                 bar_template=DETAILED,
                 end=False, end_template="Done in {seconds:.2f} seconds.",
                 indent=False, indent_char=' '):
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

    def step(self, times=1):
        self._step += times
        self.update_bar()

    def _overwrite(self, line):
        print("\r" + line + ' ' * max(0, self._max_length - len(line)), end="")
        sys.stdout.flush()
        self._max_length = max(self._max_length, len(line))

    def update_bar(self, force=False):
        now = time.time()
        if now - self._last_update < 0.1 and not force:
            return
        self._last_update = now
	
        step = self._step
        bar_max = self.bar_max
        completed = step / bar_max
        full_bar_count, rem = divmod(completed * self.bar_width, 1)
        bar = int(full_bar_count) * _unicode_eights[8]
        bar += _unicode_eights[int(rem * 8)]
        bar += ' ' * (self.bar_width - len(bar))
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
