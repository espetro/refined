# refined: refinement type hints in Python

`refined` is a Python 3 library that leverages the gradual type system in Python to constrain types by one or multiple
predicates. In short, you can ensure that the following script won't raise an `IndexError`:

```python
from refined import refined, NonEmptyList
from typing import Generator

@refined
def head_with_tail_generator(ls: NonEmptyList[int]) -> (int, Generator[int]):
    return ls[0], (_ for _ in ls[1:])


if __name__ == '__main__':
    head, tail = head_with_tail_generator([1, 2, 3])
    print(head)
    [print(_) for _ in tail]
```

## Help

See [documentation][docs] for more details.

## Installation

`refined` is available for Python 3.10+:

```shell
pip install -U refined
```

## Contributing

For guidance on setting up a development environment and how to make a contribution to `refined`, see
[Contributing to refined][contributing].

## Acknowledgements

This library is a port of [fthomas' `refined`][scala] Scala library, which, in turn, is a port of
[Nikita Volkov's `refined`][haskell] Haskell library.

Other Python libraries provide similar features, although they are based on different works, such as
[`crosshair`][crosshair], which uses an SMT solver, or [`deal`][deal], which is based on _Design-by-Contract_.

[docs]: #
[contributing]: #
[pep593]: https://www.python.org/dev/peps/pep-0593/
[pep647]: https://www.python.org/dev/peps/pep-0647/
[haskell]: http://nikita-volkov.github.io/refined
[scala]: https://github.com/fthomas/refined
[crosshair]: https://crosshair.readthedocs.io/en/latest/introduction.html
[deal]: https://deal.readthedocs.io/