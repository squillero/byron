from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence
from .riscv_operation import RiscvOperation


@dataclass
class RiscvIsaOperationSetData:
    set_name: str
    operations: Sequence[RiscvOperation]
