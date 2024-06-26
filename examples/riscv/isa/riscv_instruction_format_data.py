#################################|###|#####################################
#  __                            |   |                                    #
# |  |--.--.--.----.-----.-----. |===| This file is part of Byron v0.8    #
# |  _  |  |  |   _|  _  |     | |___| An evolutionary optimizer & fuzzer #
# |_____|___  |__| |_____|__|__|  ).(  https://pypi.org/project/byron/    #
#       |_____|                   \|/                                     #
################################## ' ######################################
# Copyright 2023-24 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from byron.classes import Macro, ParameterABC, ParameterStructuralABC


@dataclass
class RiscvInstructionFormatData:
    macro_lambda: Callable[
        [
            str,
            ParameterABC,
            ParameterABC | None,
            ParameterABC | None,
            ParameterStructuralABC | None,
        ],
        type[Macro],
    ]
    representation: str
    register_count: int
    immediate_len: None | int = field(default=None)
    is_local_reference: None | bool = field(default=None)
