# !/usr/bin/env python3
###################################|###|####################################
#   _____                          |   |                                   #
#  |  __ \--.--.----.-----.-----.  |===|  This file is part of Byron, an   #
#  |  __ <  |  |   _|  _  |     |  |___|  evolutionary source-code fuzzer. #
#  |____/ ___  |__| |_____|__|__|   ).(   Version 0.8a1 "Don Juan"         #
#        |_____|                    \|/                                    #
#################################### ' #####################################
# Copyright 2023-24 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0

import pytest

import byron as byron


@byron.fitness_function
def fitness(genotype: str):
    """Vanilla 1-max"""
    return sum(b == '1' for b in genotype)


@pytest.mark.filterwarnings("ignore:::byron")
def test_onemax():
    macro = byron.f.macro('{v}', v=byron.f.array_parameter('01', 50))
    frame = byron.f.sequence([macro])

    # sequential evaluator
    evaluator = byron.evaluator.PythonEvaluator(fitness, strip_phenotypes=True)

    # seed 42
    byron.rrandom.seed(42)
    reference_population = byron.ea.vanilla_ea(frame, evaluator, mu=10, max_generation=10)

    # seed not 42 (result should be !=)
    other_population = byron.ea.vanilla_ea(frame, evaluator, mu=10, max_generation=10)
    assert any(r[1].fitness != o[1].fitness for r, o in zip(reference_population, other_population))

    # seed 42 again (result should be ==)
    byron.rrandom.seed(42)
    other_population = byron.ea.vanilla_ea(frame, evaluator, mu=10, max_generation=10)
    assert all(r[1].fitness == o[1].fitness for r, o in zip(reference_population, other_population))

    # multi-thread parallel evaluator & seed 42 (result should be ==)
    evaluator = byron.evaluator.PythonEvaluator(fitness, strip_phenotypes=True, max_workers=None, backend='thread_pool')
    byron.rrandom.seed(42)
    other_population = byron.ea.vanilla_ea(frame, evaluator, mu=10, max_generation=10)
    assert all(r[1].fitness == o[1].fitness for r, o in zip(reference_population, other_population))

    # multi-process parallel evaluator & seed 42 (result should be ==)
    evaluator = byron.evaluator.PythonEvaluator(fitness, strip_phenotypes=True, max_workers=None, backend='joblib')
    byron.rrandom.seed(42)
    other_population = byron.ea.vanilla_ea(frame, evaluator, mu=10, max_generation=10)
    assert all(r[1].fitness == o[1].fitness for r, o in zip(reference_population, other_population))
