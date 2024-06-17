from __future__ import annotations

from .riscv_isa_operation_set import RiscvIsaOperationSet, RiscvOperation


class RiscvIsaCustomOperationSet(RiscvIsaOperationSet):
    BasicOp32 = (
        "Custom set, basic operations 32bit, no jump or branch",
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
        ],
    )
    BasicBranch = (
        "Standard branches",
        [
            RiscvOperation.BEQ,
            RiscvOperation.BNE,
            RiscvOperation.BLT,
            RiscvOperation.BLTU,
            RiscvOperation.BGE,
            RiscvOperation.BGEU,
        ],
    )
    BasicOp64 = ("Custom set, basic operations 64bit", [])
