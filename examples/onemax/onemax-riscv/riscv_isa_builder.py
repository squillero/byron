from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, Flag, auto
from typing import Sequence, List, Dict, Set, Callable
import byron
from byron.classes import ParameterABC, Macro, ParameterStructuralABC


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


class RiscvInstructionFormat(RiscvInstructionFormatData, Enum):
    R = (
        lambda representation, operands, registers, immediate, label: byron.f.macro(
            representation, op=operands, r1=registers, r2=registers, r3=registers
        ),
        "{op} {r1} {r2} {r3}",
        3,
    )
    I = (
        lambda representation, operands, registers, immediate, label: byron.f.macro(
            representation, op=operands, r1=registers, r2=registers, imm=immediate
        ),
        "{op} {r1}, {r2}, {imm:#x}",
        2,
        12,
    )
    I_5bit = (
        lambda representation, operands, registers, immediate, label: byron.f.macro(
            representation, op=operands, r1=registers, r2=registers, imm=immediate
        ),
        "{op} {r1}, {r2}, {imm:#x}",
        2,
        5,
    )
    S = (
        lambda representation, operands, registers, immediate, label: byron.f.macro(
            representation, op=operands, r1=registers, imm=immediate, r2=registers
        ),
        "{op} {r1}, {imm:#x}, {r2}",
        2,
        12,
    )
    B = (
        lambda representation, operands, registers, immediate, label: byron.f.macro(
            representation, op=operands, r1=registers, r2=registers, label=label
        ),
        "{op} {r1}, {r2}, {label}",
        2,
        12,
        True,
    )
    U = (
        lambda representation, operands, registers, immediate, label: byron.f.macro(
            representation, op=operands, r1=registers, imm=immediate
        ),
        "{op} {r1}, {imm:#x}",
        1,
        20,
    )
    J = (
        lambda representation, operands, registers, immediate, label: byron.f.macro(
            representation, op=operands, label=label
        ),
        "{op} {label}",
        1,
        20,
        False,
    )

    def __init__(
        self,
        macro_lambda: Callable[
            [
                str,
                type[ParameterABC],
                type[ParameterABC] | None,
                type[ParameterABC] | None,
                type[ParameterStructuralABC] | None,
            ],
            type[Macro],
        ],
        representation: str,
        register_count: int,
        immediate_len: None | int = None,
        is_local_reference: None | bool = None,
    ):
        self._macro_lambda = macro_lambda
        self._representation = representation
        self._register_count = register_count
        self._immediate_len = immediate_len
        self._is_local_reference = is_local_reference

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == self.name

    def create_operations_pool(self, operands: Sequence[str], registers: Sequence[str] | None):
        return self._macro_lambda(
            self._representation,
            byron.f.choice_parameter(operands),
            byron.f.choice_parameter(registers) if registers is not None else None,
            byron.f.integer_parameter(0, 2**self._immediate_len) if self._immediate_len is not None else None,
            None
            if self._is_local_reference is None
            else byron.f.local_reference(backward=True, loop=False, forward=True)
            if self._is_local_reference is True
            else byron.f.global_reference(sub, creative_zeal=1, first_macro=True),
        )


@dataclass
class RiscvOperationData:
    op_name: str
    op_format: RiscvInstructionFormat


class RiscvOperation(RiscvOperationData, Enum):
    ADDI = ("ADDI", RiscvInstructionFormat.I)
    SLTI = ("SLTI", RiscvInstructionFormat.I)
    SLTIU = ("SLTIU", RiscvInstructionFormat.I)
    ANDI = ("ANDI", RiscvInstructionFormat.I)
    ORI = ("ORI", RiscvInstructionFormat.I)
    XORI = ("XORI", RiscvInstructionFormat.I)

    SLLI = ("SLLI", RiscvInstructionFormat.I_5bit)
    SRLI = ("SRLI", RiscvInstructionFormat.I_5bit)
    SRAI = ("SRAI", RiscvInstructionFormat.I_5bit)

    LUI = ("LUI", RiscvInstructionFormat.U)
    AUIPC = ("AUIPC", RiscvInstructionFormat.U)

    ADD = ("ADD", RiscvInstructionFormat.R)
    SLT = ("SLT", RiscvInstructionFormat.R)
    SLTU = ("SLTU", RiscvInstructionFormat.R)
    AND = ("AND", RiscvInstructionFormat.R)
    OR = ("OR", RiscvInstructionFormat.R)
    XOR = ("XOR", RiscvInstructionFormat.R)
    SLL = ("SLL", RiscvInstructionFormat.R)
    SRL = ("SRL", RiscvInstructionFormat.R)
    SUB = ("SUB", RiscvInstructionFormat.R)
    SRA = ("SRA", RiscvInstructionFormat.R)

    NOP = ("NOP", RiscvInstructionFormat.I)

    JAL = ("JAL", RiscvInstructionFormat.J)
    JALR = ("JALR", RiscvInstructionFormat.I)

    BEQ = ("BEQ", RiscvInstructionFormat.B)
    BNE = ("BNE", RiscvInstructionFormat.B)
    BLT = ("BLT", RiscvInstructionFormat.B)
    BLTU = ("BLTU", RiscvInstructionFormat.B)
    BGE = ("BGE", RiscvInstructionFormat.B)
    BGEU = ("BGEU", RiscvInstructionFormat.B)

    MUL = ("MUL", RiscvInstructionFormat.R)
    MULH = ("MULH", RiscvInstructionFormat.R)
    MULHU = ("MULHU", RiscvInstructionFormat.R)
    MULHSU = ("MULHSU", RiscvInstructionFormat.R)
    DIV = ("DIV", RiscvInstructionFormat.R)
    DIVU = ("DIVU", RiscvInstructionFormat.R)
    REM = ("REM", RiscvInstructionFormat.R)
    REMU = ("REMU", RiscvInstructionFormat.R)

    MULW = ("MULW", RiscvInstructionFormat.R)
    DIVW = ("DIVW", RiscvInstructionFormat.R)
    DIVUW = ("DIVUW", RiscvInstructionFormat.R)
    REMW = ("REMW", RiscvInstructionFormat.R)
    REMUW = ("REMUW", RiscvInstructionFormat.R)

    def __init__(self, op_name: str, op_format: RiscvInstructionFormat):
        self._op_name = op_name
        self._op_format = op_format

    @property
    def op_name(self):
        return self._op_name

    @property
    def op_format(self):
        return self._op_format


@dataclass
class RiscvIsaOperationSetData:
    set_name: str
    operations: Sequence[RiscvOperation]


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
            RiscvOperation.NOP,
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
    A = ("", [])
    F = ("", [])
    D = ("", [])
    Q = ("", [])


class RiscvIsaCustomOperationSet(RiscvIsaOperationSet):
    BasicOp64 = ("Custom set, basic operations 64bit", [])


@dataclass
class RegistersData:
    type: str
    count: int = field(default=1)


class Registers(RegistersData, Enum):
    ZERO = "zero"
    RA = "ra"
    SP = "sp"
    GP = "gp"
    TP = "tp"
    T = ("t", 7)
    S = ("s", 12)
    A = ("a", 8)

    def __init__(self, type: str, count=None):
        self._type = type
        self._count = count

    @property
    def register_set(self) -> Set[str]:
        if self._count == 1:
            return set(self._type)
        else:
            return set(f"{self._type}{n}" for n in range(self._count))


class RiscvIsaBuilder:
    def __init__(self):
        self._operations: Dict[RiscvInstructionFormat, Set[str]] = dict()
        self._registers = set()

    def set_base_isa(self, base_isa: RiscvIsaBase) -> RiscvIsaBuilder:
        for op in base_isa.operations:
            print(op.name)
            _ = self.add_operation(op)
        return self

    def add_extension(self, extension: RiscvIsaExtension) -> RiscvIsaBuilder:
        for op in extension.operations:
            _ = self.add_operation(op)
        return self

    def add_operation_set(self, op_set: RiscvIsaOperationSet) -> RiscvIsaBuilder:
        for op in op_set.operations:
            _ = self.add_operation(op)
        return self

    def add_operation(self, operation: RiscvOperation) -> RiscvIsaBuilder:
        if operation.op_format not in self._operations:
            self._operations[operation.op_format] = set()
        self._operations[operation.op_format].add(operation.op_name)
        return self

    def add_register_set(self, registers: Registers) -> RiscvIsaBuilder:
        self._registers.update(registers.register_set)
        return self

    def build(self):
        registers = byron.f.choice_parameter(self._registers)
        for operation in self._operations:
            immediate
