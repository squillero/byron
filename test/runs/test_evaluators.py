###################################|###|####################################
#   _____                          |   |                                   #
#  |  __ \--.--.----.-----.-----.  |===|  This file is part of Byron, an   #
#  |  __ <  |  |   _|  _  |     |  |___|  evolutionary source-code fuzzer. #
#  |____/ ___  |__| |_____|__|__|   ).(   Version 0.8a1 "Don Juan"         #
#        |_____|                    \|/                                    #
#################################### ' #####################################
# Copyright 2023-24 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0

import itertools
import os

import pytest

import byron as byron

NUM_BITS = 100


@byron.fitness_function
def fitness(genotype):
    """Vanilla 1-max"""
    return sum(b == '1' for b in genotype)


@pytest.mark.avoidable
@pytest.mark.filterwarnings("ignore:::byron")
def test_evaluators():
    assert os.path.exists('runs') or os.path.exists('test/runs')
    if os.path.exists('test/runs'):
        os.chdir('test/runs')
    elif os.path.exists('runs'):
        os.chdir('runs')

    macro = byron.f.macro('{v}', v=byron.f.array_parameter('01', NUM_BITS + 1))
    top_frame = byron.f.sequence([macro])

    evaluators = list()
    evaluators.append(byron.evaluator.PythonEvaluator(fitness, strip_phenotypes=True))
    evaluators.append(byron.evaluator.PythonEvaluator(fitness, strip_phenotypes=True, backend='thread_pool'))
    evaluators.append(byron.evaluator.PythonEvaluator(fitness, strip_phenotypes=True, backend='joblib'))
    evaluators.append(byron.evaluator.ScriptEvaluator('./onemax-shell.sh', args=['-f']))
    evaluators.append(byron.evaluator.MakefileEvaluator('genome.dat', required_files=['onemax-shell.sh']))

    populations = list()
    for e in evaluators:
        byron.rrandom.seed(42)
        byron.logger.info("main: Using %s", e)
        populations.append(byron.ea.vanilla_ea(top_frame, e, max_generation=100, lambda_=20, mu=30))
        pass

    for p1, p2 in itertools.combinations(populations, 2):
        for i1, i2 in zip(populations[0], populations[1]):
            assert i1[1].fitness == i2[1].fitness
