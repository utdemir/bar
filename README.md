pbar
----

Configurable progress bars/status monitors for Python console applications.

A little taste of what it currently looks like:

    import time
    from pbar import Bar

    with Bar(subject="Reticulating splines... ", bar_max=4524, end=True) as bar:
        for i in range(4524):
            time.sleep(0.0005)
            bar.step()

![Example](https://raw.github.com/utdemir/pbar/master/example.gif)

TODO

* Upload to PyPI
* Decorator
* Documentation
