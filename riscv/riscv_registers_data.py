from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class RiscvRegistersData:
    type: str
    count: int = field(default=1)
