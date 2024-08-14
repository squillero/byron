`byron` 🖋
==========

[![Codename](https://img.shields.io/badge/codename-Don_Juan-pink.svg)](https://en.wikipedia.org/wiki/Don_Juan_(poem))
[![PyPI - Status](https://img.shields.io/pypi/status/byron)](https://en.wikipedia.org/wiki/Software_release_life_cycle)
[![GitHub License](https://img.shields.io/github/license/squillero/byron)](https://opensource.org/licenses/)
[![GitHub repo size](https://img.shields.io/github/repo-size/squillero/byron)](https://github.com/squillero/byron)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/byron)](https://www.python.org/)
[![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/squillero/byron/pytest.yml?label=pytest)](https://github.com/squillero/byron/actions)
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fcad-polito-it%2Fbyron.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2Fcad-polito-it%2Fbyron?ref=badge_shield)
[![Documentation Status](https://readthedocs.org/projects/byron/badge/?version=pre-alpha)](https://byron.readthedocs.io/en/pre-alpha/?badge=pre-alpha)
[![PyPI - Version](https://img.shields.io/pypi/v/byron?label=pypi)](https://pypi.org/project/byron/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/byron?label=downloads)](https://pypi.org/project/byron/)

> Build on [MicroGP](https://cad-polito-it.github.io/byron/history) technology

Byron is a source code [fuzzer](https://en.wikipedia.org/wiki/Fuzzing) designed to support assembly and high-level languages. It starts by generating a set of random programs, which are then iteratively improved by an [evolutionary algorithm](https://cad-polito-it.github.io/byron/evolution). Internally, it encodes candidate solutions as [typed](https://rcor.me/papers/typed-graph-theory.pdf), [directed](https://en.wikipedia.org/wiki/Graph_(discrete_mathematics)#Directed_graph) [multigraphs](https://en.wikipedia.org/wiki/Multigraph), and can effectively handle complex, realistic structures containing local and global variables, conditional and looping statements, and subroutines.

Programs can be evaluated using a user-defined Python function or an external tool, such as an interpreter or a simulator. Different types of parallelization are supported out of the box, from simple multithreading to the creation of temporary directories where multiple subprocesses are concurrently [spawned](https://en.wikipedia.org/wiki/Spawn_(computing)).

:package: The Python package is available on [PyPi](https://pypi.org/project/byron/); this repo is only useful if you want to hack the code.

### TL;DR

* Byron is currently in [alpha](https://en.wikipedia.org/wiki/Software_release_life_cycle#Alpha) and under active
  development
* The default branch is always the more stable
* Do not clone experimental branches `exp/*` unless you really know what you are doing
* Follow this [style guide](https://github.com/squillero/style/blob/master/python.md) and keep the code formatted
  with [Ruff](https://docs.astral.sh/ruff/formatter/)
* Follow this [convention](https://github.com/squillero/style/blob/master/git.md) when drafting commit messages
* Write as few lines of code and as many lines of comments as possible (ie. use builtins, exploit generators and list
  comprehension)
* Be [paranoid](https://cad-polito-it.github.io/byron/paranoia) (cit. *"I need someone to show me the things"*)
* Use [pytest](https://docs.pytest.org/) and [Coverage.py](https://coverage.readthedocs.io/) for unit testing (ie. `coverage run --module pytest --all`)
* Use [Ruff](https://docs.astral.sh/ruff/linter/) for linting and [mypy](https://mypy-lang.org/) for type checking
* Use [direnv](https://direnv.net) to patch environment variables
* It may be wise to contact [Giovanni](https://github.com/squillero) before trying to change anything

### Contacts

* [Giovanni Squillero](https://github.com/squillero) [:email:](mailto:giovanni.squillero@polito.it) [:house:](https://staff.polito.it/giovanni.squillero/)
* [Alberto Tonda](https://github.com/albertotonda/) [:email:](mailto:alberto.tonda@inrae.fr) [:house:](https://www.researchgate.net/profile/Alberto_Tonda)

### Main Contributors

<a href="https://github.com/cad-polito-it/byron/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=cad-polito-it/byron" />
</a>

### Licence

Copyright (c) 2023-24 [Giovanni Squillero](https://github.com/squillero)
and [Alberto Tonda](https://github.com/albertotonda/)  
Byron is [free and open-source software](https://en.wikipedia.org/wiki/Free_and_open-source_software), and it is distributed under the permissive [Apache License 2.0](https://opensource.org/license/apache-2-0/).
