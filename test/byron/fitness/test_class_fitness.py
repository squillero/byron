###################################|###|####################################
#   _____                          |   |                                   #
#  |  __ \--.--.----.-----.-----.  |===|  This file is part of Byron, an   #
#  |  __ <  |  |   _|  _  |     |  |___|  evolutionary source-code fuzzer. #
#  |____/ ___  |__| |_____|__|__|   ).(   Version 0.8a1 "Don Juan"         #
#        |_____|                    \|/                                    #
#################################### ' #####################################
# Copyright 2023-24 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0

import byron as byron


class ExampleFitness(byron.classes.fitness.FitnessABC):
    def __init__(self, value: float):
        self.value = value

    def is_fitter(self, other: "ExampleFitness") -> bool:
        return self.value > other.value

    def is_dominant(self, other: "ExampleFitness") -> bool:
        return self.is_fitter(other)

    def is_distinguishable(self, other: "ExampleFitness") -> bool:
        return self.value != other.value

    def _decorate(self) -> str:
        return str(self.value)


def test_is_fitter():
    fitness1 = ExampleFitness(5.0)
    fitness2 = ExampleFitness(3.0)
    assert fitness1.is_fitter(fitness2)
    assert not fitness2.is_fitter(fitness1)


def test_is_dominant():
    fitness1 = ExampleFitness(5.0)
    fitness2 = ExampleFitness(3.0)
    assert fitness1.is_dominant(fitness2)
    assert not fitness2.is_dominant(fitness1)


def test_is_distinguishable():
    fitness1 = ExampleFitness(5.0)
    fitness2 = ExampleFitness(3.0)
    fitness3 = ExampleFitness(5.0)
    assert fitness1.is_distinguishable(fitness2)
    assert not fitness1.is_distinguishable(fitness3)


def test_decorate():
    fitness = ExampleFitness(5.0)
    assert fitness._decorate() == "5.0"


def test_reverse_fitness():
    reversed_fitness = byron.fitness.reverse_fitness(ExampleFitness)
    reversed_fitness1 = reversed_fitness(5.0)
    reversed_fitness2 = reversed_fitness(3.0)

    assert reversed_fitness2.is_fitter(reversed_fitness1)
    assert not reversed_fitness1.is_fitter(reversed_fitness2)

    assert reversed_fitness1 != reversed_fitness2

    assert reversed_fitness1._decorate() == "ᴙ5.0"
    assert reversed_fitness2._decorate() == "ᴙ3.0"
