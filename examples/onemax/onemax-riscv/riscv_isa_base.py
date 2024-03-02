from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, Flag, auto
from typing import Sequence, List, Dict, Set, Callable, Collection
import byron
from byron.classes import ParameterABC, Macro, ParameterStructuralABC, FrameABC
from riscv_isa_operation_set import RiscvIsaOperationSet, RiscvOperation


class RiscvIsaBase(RiscvIsaOperationSet):
    RV32I = (
        "RV32I",
        [
            RiscvOperation.ADDI,
            RiscvOperation.SLTI,
            RiscvOperation.SLTIU,
            RiscvOperation.ANDI,
            RiscvOperation.ORI,
            RiscvOperation.XORI,
            RiscvOperation.SLLI,
            RiscvOperation.SRLI,
            RiscvOperation.SRAI,
            RiscvOperation.LUI,
            RiscvOperation.AUIPC,
            RiscvOperation.ADD,
            RiscvOperation.SLT,
            RiscvOperation.SLTU,
            RiscvOperation.AND,
            RiscvOperation.OR,
            RiscvOperation.XOR,
            RiscvOperation.SLL,
            RiscvOperation.SRL,
            RiscvOperation.SUB,
            RiscvOperation.SRA,
            # RiscvOperation.NOP,
            RiscvOperation.JAL,
            RiscvOperation.JALR,
            RiscvOperation.BEQ,
            RiscvOperation.BNE,
            RiscvOperation.BLT,
            RiscvOperation.BLTU,
            RiscvOperation.BGE,
            RiscvOperation.BGEU,
        ],
    )
    RV32E = ("RV32E", [])
    RV64I = ("RV64I", [*RV32I[1], *[]])
    RV128I = ("RV128I", [])
