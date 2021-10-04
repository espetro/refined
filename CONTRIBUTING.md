# Contributing to refined

# Background

* [In this blogpost][blog], you can get an initial idea of what refinement types are
* Our inspiration is a library for refinement types in Scala: https://github.com/fthomas/refined
* Other Python libraries provide similar features, although they are based on different works, such as
[`crosshair`][crosshair], which uses an SMT solver, or [`deal`][deal], which is based on _Design-by-Contract_.

# Development

## Development environment setup

* Use one of the Python versions listed in `.python-version`. I use `pyenv` as
  the Python version manager, and v3.10.0b2 as the Python version.
* Create a virtual environment, and link it to the code editor you're using. I
  use Intellij / PyCharm.
* Once you have it activated, you can run all the unit tests with
  `python3 -m unittest discover tests`

## What can I help with?

For now, you can [get a task from an open issue][issues]. PRs for new functionality are also welcomed, although it's
mandatory to explain / discuss it previously in an issue.

[blog]: https://medium.com/@thejameskyle/type-systems-refinements-explained-26f713c6cc2a
[issues]: https://github.com/espetro/refined/issues
[crosshair]: https://crosshair.readthedocs.io/en/latest/introduction.html
[deal]: https://deal.readthedocs.io/