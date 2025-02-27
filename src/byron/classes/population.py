###################################|###|####################################
#   _____                          |   |                                   #
#  |  __ \--.--.----.-----.-----.  |===|  This file is part of Byron, an   #
#  |  __ <  |  |   _|  _  |     |  |___|  evolutionary source-code fuzzer. #
#  |____/ ___  |__| |_____|__|__|   ).(   Version 0.8a1 "Don Juan"         #
#        |_____|                    \|/                                    #
#################################### ' #####################################

# Copyright 2023-24 Giovanni Squillero and Alberto Tonda
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#
# See the License for the specific language governing permissions and
# limitations under the License.

# =[ HISTORY ]===============================================================
# v1 / April 2023 / Squillero (GX)

__all__ = ["Population"]

import logging
from collections.abc import Iterable, Sequence
from copy import copy
from typing import Any, Callable

from byron.classes.fitness import FitnessABC
from byron.classes.individual import Individual
from byron.classes.node import NODE_ZERO
from byron.classes.selement import SElement
from byron.global_symbols import *
from byron.tools.entropy import *
from byron.user_messages import *


class Population(Iterable):
    _top_frame: type[SElement]
    _fitness_function: Callable[[Any], FitnessABC]
    _individuals: list[Individual]
    _memory: set | None
    _generation: int

    def __init__(self, top_frame: type[SElement], extra_parameters: dict | None = None, *, memory: bool = False):
        assert check_valid_types(top_frame, SElement, subclass=True)
        assert extra_parameters is None or check_valid_type(extra_parameters, dict)
        self._top_frame = top_frame
        if extra_parameters is None:
            extra_parameters = dict()
        self._population_extra_parameters = DEFAULT_EXTRA_PARAMETERS | DEFAULT_OPTIONS | extra_parameters
        self._individuals = list()
        self._generation = -1
        if memory:
            self._memory = set()
        else:
            self._memory = None

    @property
    def top_frame(self):
        return self._top_frame

    @property
    def individuals(self) -> list[Individual]:
        return self._individuals

    @property
    def population_extra_parameters(self) -> dict:
        return copy(self._population_extra_parameters)

    @property
    def generation(self):
        return self._generation

    @generation.setter
    def generation(self, value):
        self._generation = value

    def __iter__(self) -> tuple[int, 'Individual']:
        return enumerate(self._individuals)

    @property
    def not_finalized_individuals(self):
        return tuple(filter(lambda x: not x[1].finalized, enumerate(self._individuals)))

    @property
    def finalized_individuals(self):
        return tuple(filter(lambda x: x[1].finalized, enumerate(self._individuals)))

    @property
    def entropy(self):
        # calculate_delta_entropy(i.as_message for i in self._individuals)
        return calculate_entropy(i.as_message for i in self._individuals)

    def __getitem__(self, item):
        return self._individuals[item]

    def __len__(self):
        return len(self._individuals)

    @staticmethod
    def _count_components(i):
        import networkx as nx

        G = nx.MultiDiGraph()
        G.add_edges_from(i.G.edges)
        G.remove_node(NODE_ZERO)
        return sum(1 for _ in nx.weakly_connected_components(G))

    def __iadd__(self, individual: Sequence[Individual]):
        assert check_valid_types(individual, Sequence)
        assert all(check_valid_types(i, Individual) for i in individual)
        assert all(i.run_paranoia_checks() for i in individual)
        self._generation += 1
        for i in individual:
            i.age.birth = self._generation
            i.age.apparent_age = 0
            self._individuals.append(i)
        if self._memory is not None:
            self._memory |= set(individual)
        return self

    def __isub__(self, individual):
        assert check_valid_types(individual, Sequence)
        assert all(check_valid_types(i, Individual) for i in individual)
        assert all(i.valid for i in individual), "ValueError: invalid individual"
        for i in individual:
            try:
                self._individuals.remove(i)
            except ValueError:
                pass
        return self

    def __str__(self):
        return (
            f"{self.__class__.__name__} @ {hex(id(self))} (top frame: {self.top_frame.__name__})"
            + "\n• "
            + "\n• ".join(str(i) for i in self._individuals)
        )

    def dump_individual(self, ind: int | Individual, extra_parameters: dict | None = None) -> str:
        if isinstance(ind, int):
            ind = self.individuals[ind]
        if extra_parameters is None:
            extra_parameters = dict()
        assert extra_parameters is None or check_valid_type(extra_parameters, dict)
        return ind.canonic_representation.dump(self.population_extra_parameters | extra_parameters)
        # return ind.dump(self.population_extra_parameters | extra_parameters)

    def evaluate(self):
        raise NotImplementedError
        whole_pop = [self.dump_individual(i) for i in self.individuals]
        result = self._evaluator._evaluate(whole_pop)
        if logger.level <= logging.DEBUG:
            for i, f in enumerate(result):
                logger.debug(f"evaluate: Individual {i:2d}: {f}")
        for i, f in zip(self.individuals, result):
            i.fitness = f

    def sort(self):
        fronts = list()
        sorted_ = list()
        individuals = set(self._individuals)

        while individuals:
            pareto = set(
                i1
                for i1 in individuals
                if all(i1.fitness == i2.fitness or i1.fitness >> i2.fitness for i2 in individuals)
            )
            fronts.append(pareto)
            individuals -= pareto
            sorted_ += sorted(pareto, key=lambda i: (i.fitness, -i.id))

        self._individuals = sorted_

    def aging(self, step: int = 1, top_n: int = None):
        for i in self._individuals[top_n:]:
            i.aging(step)

    def get_elders(self, lifespan: int, top_n: int = None) -> list[Individual]:
        return [i for i in self._individuals[top_n:] if i.age.apparent_age > lifespan]

    def life_cycle(self, lifespan: int, step: int = 1, top_n: int = None):
        self.aging(step, top_n)
        self -= self.get_elders(lifespan, top_n)
