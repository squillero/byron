from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, Flag, auto
from typing import Sequence, List, Dict, Set, Callable, Collection
import byron
from byron.classes import ParameterABC, Macro, ParameterStructuralABC, FrameABC
from .riscv_isa_operation_set import RiscvIsaOperationSet, RiscvOperation


class RiscvIsaExtension(RiscvIsaOperationSet):
    pass
    M = (
        "Extension for Integer Multiplication and Division",
        [
            RiscvOperation.MUL,
            RiscvOperation.MULH,
            RiscvOperation.MULHU,
            RiscvOperation.MULHSU,
            RiscvOperation.DIV,
            RiscvOperation.DIVU,
            RiscvOperation.REM,
            RiscvOperation.REMU,
        ],
    )
    M_64 = (
        M[0],
        [
            *M[1],
            *[
                RiscvOperation.MULW,
                RiscvOperation.DIVW,
                RiscvOperation.DIVUW,
                RiscvOperation.REMW,
                RiscvOperation.REMUW,
            ],
        ],
    )
    # A = ("", [])
    # F = ("", [])
    # D = ("", [])
