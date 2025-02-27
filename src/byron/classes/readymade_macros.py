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

__all__ = ["MacroZero", "Info"]

from datetime import datetime

from byron.classes.macro import Macro
from byron.global_symbols import *
from byron.user_messages import *


class MacroZero(Macro):
    TEXT = (
        "{_comment}"
        + f""" Automagically written by Byron v{__version__}"""
        + f""" on {datetime.today().strftime('%d-%b-%Y')}"""
        + f""" at {datetime.today().strftime('%H:%M:%S')}"""
    )
    EXTRA_PARAMETERS = dict()
    PARAMETERS = dict()

    @property
    def valid(self) -> bool:
        return True

    @property
    def shannon(self) -> list[int]:
        return [hash(self.__class__)]


class Info(Macro):
    TEXT = '''{_comment} * Byron {_byron.byron}
{_comment} * Python {_byron.python}
{_comment} * NetworkX {_byron.nx}
{_comment} * System: {_byron.system}
{_comment} * Machine: {_byron.machine}'''
    PARAMETERS = dict()
    EXTRA_PARAMETERS = dict()

    _parameter_types = dict()

    @property
    def valid(self) -> bool:
        return True

    @property
    def shannon(self) -> list[int]:
        return [hash(self.__class__)]


MacroZero._patch_info()
Info._patch_info()
