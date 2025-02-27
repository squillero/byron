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


def test_evaluator_abstract_methods():
    try:
        evaluator = byron.classes.evaluator.EvaluatorABC()
    except TypeError:
        pass
    else:
        assert False, "EvaluatorABC should not be instantiable."

    class MyEvaluator(byron.classes.evaluator.EvaluatorABC):
        def evaluate(self, individuals):
            return [byron.classes.fitness.FitnessABC() for i in individuals]

    evaluator = MyEvaluator()
    assert callable(evaluator.evaluate)
