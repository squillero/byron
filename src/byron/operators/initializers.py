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
# v1 / June 2023 / Squillero (GX)

__all__ = ["random_individual"]

from byron.classes.individual import *
from byron.operators.graph_tools import *
from byron.registry import *
from byron.user_messages import *


@genetic_operator(num_parents=None)
def random_individual(top_frame) -> list[Individual]:
    """Generate a valid random individual to the population."""

    new_root = None
    new_individual = None
    while new_root is None:
        new_individual = Individual(top_frame)
        try:
            new_root = unroll_individual(new_individual, top_frame)
        except ByronOperatorFailure:
            new_root = None
    return [new_individual]
