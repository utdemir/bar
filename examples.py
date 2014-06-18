import time

from bar import Bar

for i in ("block", "shades", "ascii"):
    with Bar(subject="Reticulating splines... ", bar_max=3000, end=True, chars=i) as bar:
        for i in range(3000):
            time.sleep(0.001)
            bar.step()

with Bar(subject="Reticulating splines... ", bar_max=1000000, end=True) as bar:
    for i in range(1000000):
        bar.step()
