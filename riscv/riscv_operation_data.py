from __future__ import annotations

from dataclasses import dataclass
from .riscv_instruction_format import RiscvInstructionFormat


@dataclass
class RiscvOperationData:
    op_name: str
    op_format: RiscvInstructionFormat
