from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, Flag, auto
from typing import Sequence, List, Dict, Set, Callable, Collection
import byron
from byron.classes import ParameterABC, Macro, ParameterStructuralABC, FrameABC


@dataclass
class RiscvRegistersData:
    type: str
    count: int = field(default=1)
