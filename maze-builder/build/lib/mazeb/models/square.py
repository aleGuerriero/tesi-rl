from dataclasses import dataclass

from mazeb.models.border import Border
from mazeb.models.role import Role

@dataclass(frozen=True)
class Square:
  index: int
  row: int
  column: int
  border: Border
  role: Role = Role.NONE
    