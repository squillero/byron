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

#############################################################################
# HISTORY
# v1 / July 2023 / Squillero (GX)

from byron.classes.individual import Individual
from byron.classes.population import Population
from byron.randy import rrandom
from byron.user_messages.checks import *


def tournament_selection(population: Population, tournament_size: float = 2) -> Individual:
    assert check_value_range(tournament_size, min_=1)
    candidates = [rrandom.choice(population.individuals) for _ in range(tournament_size)]
    if rrandom.boolean(p_true=tournament_size % 1):
        candidates.append(rrandom.choice(population.individuals))
    return max(candidates, key=lambda i: i.fitness)
