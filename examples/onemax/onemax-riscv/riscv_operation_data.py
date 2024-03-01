from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, Flag, auto
from typing import Sequence, List, Dict, Set, Callable, Collection
import byron
from byron.classes import ParameterABC, Macro, ParameterStructuralABC, FrameABC
from riscv_instruction_format import RiscvInstructionFormat


@dataclass
class RiscvOperationData:
    op_name: str
    op_format: RiscvInstructionFormat
