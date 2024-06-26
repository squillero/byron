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

from .riscv_isa_operation_set import RiscvIsaOperationSet, RiscvOperation


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
