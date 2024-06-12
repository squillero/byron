[![Codename](https://img.shields.io/badge/codename-Don_Juan-pink.svg)](https://en.wikipedia.org/wiki/Don_Juan_(poem))
[![GitHub License](https://img.shields.io/github/license/squillero/byron)](https://opensource.org/licenses/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/byron)](https://www.python.org/)
[![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/cad-polito-it/byron/pytest.yml?label=tests)
](https://github.com/cad-polito-it/byron/actions)
[![Documentation Status](https://readthedocs.org/projects/byron/badge/?version=pre-alpha)](https://byron.readthedocs.io/en/pre-alpha/?badge=pre-alpha)
[![GitHub last commit (alpha)](https://img.shields.io/github/last-commit/cad-polito-it/byron/alpha?label=last+github+commit)](https://github.com/cad-polito-it/byron/pulse)
![PyPI - Downloads](https://img.shields.io/pypi/dm/byron?label=downloads)

Byron is a generic [optimizer](https://en.wikipedia.org/wiki/Engineering_optimization) designed to support source code [fuzzing](https://en.wikipedia.org/wiki/Fuzzing), either in assembly or in higher level languages. It starts by generating a set of random programs, which are then iteratively improved by an [evolutionary algorithm](https://cad-polito-it.github.io/byron/evolution). It can handle quite complex structures including subroutines, local and global variables, jumps, conditionals, and loops.

Test programs [do not need to be *designed*](https://evolution.berkeley.edu/), but merely *evaluated* using an external tool, such as an interpreter or a simulator. Different types of parallelization are supported out of the box, from simple multithreading to the creation of temporary directories where multiple subprocesses are concurrently [spawned](https://en.wikipedia.org/wiki/Spawn_(computing)).

**⚠️ Byron is currently in [alpha](https://en.wikipedia.org/wiki/Software_release_life_cycle#Alpha) and under active development**

## Installation

As simple as

```
pip install --upgrade byron
```

A few dependencies can enhance Byron functionalities, but are not strictly required. You can get them all with

```
pip install --upgrade "byron[full]"
```

## Documentation

None yet, but some HOWTO's and examples [are available](https://github.com/cad-polito-it/byron/tree/alpha/examples) in the development repo.

## Contacts

* Giovanni Squillero — <giovanni.squillero@polito.it>
* Alberto Tonda — <alberto.tonda@inrae.fr>

## License

Copyright (c) 2023-24 [Giovanni Squillero](https://github.com/squillero) and [Alberto Tonda](https://github.com/albertotonda/)  
Byron is [free and open-source software](https://en.wikipedia.org/wiki/Free_and_open-source_software), and it is distributed under the permissive [Apache License 2.0](https://opensource.org/license/apache-2-0/).
