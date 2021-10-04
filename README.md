<h1 align="center">
    refined: refinement type hints in Python
</h1>

<p align="center">
    <a href="https://github.com/espetro/refined/actions?query=workflow%3ATest+event%3Apush+branch%3Amaster" target="_blank">
        <img src="https://github.com/espetro/refined/workflows/Test/badge.svg?event=push&branch=master" alt="Tests">
    </a>
    <a href="https://pypi.org/project/refined" target="_blank">
        <img src="https://img.shields.io/pypi/v/refined?color=%2334D058&label=pypi%20package" alt="Package version">
    </a>
</p>

`refined` is a Python 3 library that leverages the gradual type system in Python to constrain types by one or multiple
predicates. In short, you can ensure that the following script won't raise an `IndexError`:

```python
from refined import refined, NonEmptyList
from typing import Generator

@refined
def head_with_tail_generator(ls: NonEmptyList[int]) -> (int, Generator[int]):
    return ls[0], (_ for _ in ls[1:])


if __name__ == '__main__':
    head, tail = head_with_tail_generator([])  # this call raises a RefinementTypeException
    print(head)
    [print(_) for _ in tail]
```

## Help

See [documentation][docs] for more details.

## Installation

`refined` is available for Python 3.7+:

```shell
pip install -U refined
```

## Contributing

For guidance on setting up a development environment and how to make a contribution to `refined`, see
[Contributing to refined][contributing].

## Acknowledgements

This library is a port of [fthomas' `refined`][scala] Scala library, which, in turn, is a port of
[Nikita Volkov's `refined`][haskell] Haskell library.

[docs]: https://github.com/espetro/refined/wiki
[contributing]: https://github.com/espetro/refined/blob/master/CONTRIBUTING.md
[pep593]: https://www.python.org/dev/peps/pep-0593/
[pep647]: https://www.python.org/dev/peps/pep-0647/
[haskell]: http://nikita-volkov.github.io/refined
[scala]: https://github.com/fthomas/refined