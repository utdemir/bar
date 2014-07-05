from __future__ import print_function

import time

from bar import Bar

with Bar(subject="%-25s" % "Reticulating splines...", count=3000) as b:
    for i in range(3000):
        time.sleep(0.001)
        b.step()

print()

Timer = Bar(template="{subject} Wait {eta:.0f} seconds more. ({spinner})",
            end="{subject} Done in {seconds:.2f} seconds.",
            chars="braille")

with Timer(subject="%-25s" % "Doing something...    ", count=2000) as b:
    for i in range(2000):
        time.sleep(0.004)
        b.step()

with Timer(subject="%-25s" % "Doing another thing...", count=1000) as b:
    for i in range(1000):
        time.sleep(0.001)
        b.step()

print()

with Bar(subject="%-8s" % "Map.", count=20000) as b:
    list(map(b.watch(lambda i: i**60), range(10000)))
    list(b.map(lambda i: i**120, range(10000)))

print()

for i in ("ascii", "block", "shades"):
    Bar(subject="%-8s" % i, chars=i).map(lambda i: i**1000, range(20000))
