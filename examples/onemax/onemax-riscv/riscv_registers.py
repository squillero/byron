from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, Flag, auto
from typing import Sequence, List, Dict, Set, Callable, Collection
import byron
from byron.classes import ParameterABC, Macro, ParameterStructuralABC, FrameABC
from riscv_registers_data import RiscvRegistersData


class RiscvRegisters(RiscvRegistersData, Enum):
    ZERO = "zero"
    RETURN_ADDRESS = "ra"
    STACK_POINTER = "sp"
    GLOBAL_POINTER = "gp"
    THREAD_POINTER = "tp"
    TEMPORARIES = ("t", 7)
    SAVED = ("s", 12)
    ARGUMENTS = ("a", 8)

    def __init__(self, type: str, count=1):
        self._type = type
        self._count = count

    @property
    def register_set(self) -> Set[str]:
        if self._count == 1:
            return {self._type}
        else:
            return set(f"{self._type}{n}" for n in range(self._count))
