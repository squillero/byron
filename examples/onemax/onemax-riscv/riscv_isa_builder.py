from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, Flag, auto
from typing import Sequence, List, Dict, Set, Callable, Collection
import byron
from byron.classes import ParameterABC, Macro, ParameterStructuralABC, FrameABC
from riscv_instruction_format import RiscvInstructionFormat
from riscv_isa_base import RiscvIsaBase
from riscv_isa_extension import RiscvIsaExtension
from riscv_isa_operation_set import RiscvIsaOperationSet
from riscv_operation import RiscvOperation
from riscv_registers import RiscvRegisters
from riscv_isa import RiscvIsa


class RiscvIsaBuilder:
    def __init__(self):
        self._operations: Dict[RiscvInstructionFormat, Set[str]] = dict()
        self._registers: Set[str] = set()

    def set_base_isa(self, base_isa: RiscvIsaBase) -> RiscvIsaBuilder:
        for op in base_isa.operations:
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

    def add_register_set(self, registers: RiscvRegisters) -> RiscvIsaBuilder:
        self._registers.update(registers.register_set)
        return self

    def build(self) -> RiscvIsa:
        return RiscvIsa(self._operations, self._registers)
