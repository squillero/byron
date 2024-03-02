from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, Flag, auto
from typing import Sequence, List, Dict, Set, Callable, Collection
import byron
from byron.classes import ParameterABC, Macro, ParameterStructuralABC, FrameABC
from riscv_isa_operation_set_data import RiscvIsaOperationSetData, RiscvOperation


class RiscvIsaOperationSet(RiscvIsaOperationSetData, Enum):
    def __init__(self, set_name: str, operations: List[RiscvOperation]):
        self._set_name = set_name
        self._operations = operations

    @property
    def set_name(self):
        return self._set_name

    @property
    def operations(self):
        return self._operations
