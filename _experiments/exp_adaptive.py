#!/usr/bin/env python3
###################################|###|####################################
#   _____                          |   |                                   #
#  |  __ \--.--.----.-----.-----.  |===|  This file is part of Byron, an   #
#  |  __ <  |  |   _|  _  |     |  |___|  evolutionary source-code fuzzer. #
#  |____/ ___  |__| |_____|__|__|   ).(   Version 0.8a1 "Don Juan"         #
#        |_____|                    \|/                                    #
#################################### ' #####################################
# Copyright 2023-24 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0

import logging

import byron

NUM_BITS = 500


@byron.fitness_function
def fitness(genotype):
    """Parametric 1-max"""
    return sum(b == '1' for b in genotype)


def main():
    macro = byron.f.macro('{v}', v=byron.f.array_parameter('01', NUM_BITS + 1))
    top_frame = byron.f.sequence([macro])

    # evaluator = byron.evaluator.PythonEvaluator(fitness, strip_phenotypes=True)
    # evaluator = byron.evaluator.PythonEvaluator(fitness, strip_phenotypes=True, backend='thread_pool')
    evaluator = byron.evaluator.PythonEvaluator(fitness, strip_phenotypes=True, backend='joblib')

    byron.logger.info("main: Using %s", evaluator)

    population = byron.ea.adaptive_ea(
        top_frame, evaluator, max_generation=5000, lambda_=20, mu=10, max_fitness=NUM_BITS, top_n=5, lifespan=100
    )

    print()

    byron.sys.log_operators()


byron.logger.setLevel(level=logging.INFO)

main()
