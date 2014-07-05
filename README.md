# bar [![PyPI version](https://badge.fury.io/py/bar.svg)](http://badge.fury.io/py/bar)


Configurable progress bars/status monitors for Python console applications.

A little taste of what it currently looks like: https://asciinema.org/a/10643

## Features

* Ease of usage, thanks to with statement
* Just uses ASCII control characters and Unicode, not curses etc.
* Fully customizable templates
* Dynamically updating progress bar and spinners
* Ability to show elapsed and estimated times
* Python 2 and 3 compatible

## Usage

### Simple Usage

    import time
    from bar import Bar

    with Bar("Reticulating splines...", count=3000) as b:
        for i in range(3000):
            time.sleep(0.001)
            b.step()

You can see `examples.py` for detailed examples.

### Parameters

* **subject** (*Default: ""*): Subject of the bar, see *template* parameter.
* **count**: Steps to complete. Will be used when showing progress bars and ETA calculation.
* **end** (*Default: None*): Text to show instead of *template* when process completes.
* **progressbar_width**: (*Default: -1*) Width of the progress bar. Expands to the whole line when negative.
* **chars** (*Default: "block"*): Chars used on progress bar. You can use the  predefined characters below, or specify your own string.

        "block": "  ▏▎▍▌▋▊▉█",
        "shades": " ░▒▓█",
        "braille": " ⡀⡄⡆⡇⣇⣧⣷⣿",
        "ascii": " -=#"
  
* **spinner** (*Default: "fish"*): You can use the predefined ones below, or specify your own(should support `len` and integer indexing). Will be shown with 2 FPS.

        "simple": ("*----", "-*---", "--*--", "---*-",
                   "----*", "---*-", "--*--", "-*---"),
        "fish": (">))'>    ", " >))'>   ", "  >))'>  ", "   >))'> ",
                 "    <'((<", "   <'((< ", "  <'((<  ", " <'((<   ")

* **template** (*Default: "detailed"*): The bar itself, using Python's standart string formatting syntax. You can use the  predefined templates below, or specify your own.

        "detailed": "{subject} [{progressbar}] %{percentage:.2f} Elapsed: {seconds:.0f}s ETA: {eta:.0f}s",
        "timer": "{seconds:.0f}s"

    Allowed variables:
    * **subject**
    * **spinner**
    * **progressbar**
    * **step**: The current step
    * **count**: The maximum step count
    * **remaining_steps**: count - step
    * **completed**: step / count (as float)
    * **percentage**: completed * 100 (as float)
    * **seconds**: Seconds elapsed (as float)
    * **eta**: Estimated completion (as float)

### Helper methods

* **bar.watch(f)**: Returns a wrapper to `f` to call `bar.step` after completion.

* **bar.map(f, *iterables)**: Maps `f` over `iterables` while stepping the bar.

        def map(self, f, *iterables):
            return map(self.watch(f), *iterables)

* **Bar.map(f, *iterables)**: Creates a bar to show progress of `map`. *iterables* should support `len`. **Warning:** This function is eager on both Python 2 and Python 3 and always returns `list`.

* **bar.cancel()**: Stops updating the bar, useful for debugging.

### Constraints

* You shouldn't print anything or modify standart output anyhow when a bar is in progress.
* You shouldn't nest bars, or use multiple bars in the same time.
* You can't `step` a bar from a different process.

## TODO

* Use as a decorator
* Allow nesting
* Smarter ETA measurement
* Use any `iterable` instead of indexable objects on spinners
