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
# v1 / May 2023 / Squillero (GX)

"""
Methods and constants to create the framework for the individuals.

Notes:
    * As the framework is composed of classes, methods are class factories.
    * Methods are cached, thus multiple calls with equal or equivalent argument return the `same` class. Ie.
      Python operator ``is`` returns ``True``
"""

from byron.classes.readymade_frames import *
from byron.classes.readymade_macros import *

from .bnf import *
from .defaults import *
from .framework import *
from .macro import *
from .parameter import *
from .parameter_structural_global import *
from .parameter_structural_local import *
from .shared import *
from .show_element import *
