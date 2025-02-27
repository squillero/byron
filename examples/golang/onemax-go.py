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

import argparse
import logging

import golang

import byron


@byron.fitness_function(type_=byron.fitness.basic.Scalar)
def dummy_fitness(text):
    return 0.0 + text.count('func ')


def main():
    top_frame = golang.framework()

    # evaluator = byron.evaluator.ScriptEvaluator('./evaluate-all.sh', filename_format="individual{i:06}.go")
    evaluator = byron.evaluator.ParallelScriptEvaluator(
        'go', 'onemax.go', other_required_files=('main.go',), flags=('run',), timeout=300, default_result='-1'
    )
    # evaluator = byron.evaluator.PythonEvaluator(dummy_fitness)

    byron.f.set_global_option('$dump_node_info', True)
    # final_population = byron.ea.vanilla_ea(top_frame, evaluator, max_generation=1_000, mu=50, lambda_=20, max_fitness=64.0)
    final_population = byron.ea.adaptive_ea(
        top_frame, evaluator, max_generation=1_000, mu=50, lambda_=20, max_fitness=64.0
    )

    # byron.logger.info("[b]POPULATION[/b]")
    # max_f = max(i.fitness for i in final_population.individuals)
    # min_f = min(i.fitness for i in final_population.individuals)
    # byron.logger.info(f"* {len(final_population)} individuals ({min_f} – {max_f})")

    for i, I in final_population:
        I.as_lgp(f'final-individual_{I.id}-lgp.png')
        I.as_forest(f'final-individual_{I.id}-structure.png')
        with open(f'final-individual_{I.id}.go', 'w') as out:
            out.write(final_population.dump_individual(i))
        byron.logger.info(f"OneMaxGo: {I.describe(max_recursion=None)}")

    byron.sys.log_operators()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-v',
        '--verbose',
        action='store_const',
        dest='verbose',
        const=2,
        default=1,
        help='use verbose logging (debug messages)',
    )
    parser.add_argument(
        '-q', '--quiet', action='store_const', dest='verbose', const=0, help='be quiet (only log warning messages)'
    )
    args = parser.parse_args()

    if args.verbose == 0:
        byron.logger.setLevel(level=logging.WARNING)
    elif args.verbose == 1:
        byron.logger.setLevel(level=logging.INFO)
    elif args.verbose == 2:
        byron.logger.setLevel(level=logging.DEBUG)

    main()
