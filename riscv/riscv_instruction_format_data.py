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
