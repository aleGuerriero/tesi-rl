from dataclasses import dataclass
from typing import Iterator
from functools import reduce

from mazeb.models.square import Square
from mazeb.models.role import Role

@dataclass(frozen=True)
class Solution:
  squares: tuple[Square, ...]

  def __post_init__(self):
    assert self.squares[0].role is Role.START
    assert self.squares[-1].role is Role.TARGET
    reduce(validate_corridor, self.squares)

  def __iter__(self) -> Iterator[Square]:
    return iter(self.squares)
  
  def __getitem__(self, index: int) -> Square:
    return self.squares[index]
  
  def __len__(self) -> int:
    return len(self.squares)
  
def validate_corridor(current: Square, next: Square) -> Square:
  assert any([
    current.row == next.row,
    current.column == next.column
  ]), 'Squares must lie in the same column or row'
  return next