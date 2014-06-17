import time

from bar import Bar

with Bar(subject="Reticulating splines... ", bar_max=4524, end=True) as bar:
    for i in range(4524):
        time.sleep(0.0005)
        bar.step()
