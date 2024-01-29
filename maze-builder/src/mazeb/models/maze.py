from dataclasses import dataclass
from typing import Iterator
from functools import cached_property
from pathlib import Path

from mazeb.models.square import Square
from mazeb.models.role import Role
from mazeb.persistence.serializer import dump_squares, load_squares

@dataclass(frozen=True)
class Maze:
  squares: tuple[Square, ...]

  def __post_init__(self) -> None:
    validate_indexes(self)
    validate_rows_columns(self)
    validate_start(self)
    validate_target(self)

  @classmethod
  def load(cls, path: Path) -> 'Maze':
    return Maze(tuple(load_squares(path)))

  def __iter__(self) -> Iterator[Square]:
    return iter(self.squares)
  
  def __getitem__(self, index: int) -> Square:
    return self.squares[index]
  
  def dump(self, path: Path):
    dump_squares(self.width, self.height, self.squares, path)
  
  @cached_property
  def width(self):
    return max(square.column for square in self) + 1
  
  @cached_property
  def height(self):
    return max(square.row for square in self) + 1
  
  @cached_property
  def start(self) -> Square:
    return next(square for square in self if square.role is Role.START)
  
  @cached_property
  def target(self) -> Square:
    return next(square for square in self if square.role is Role.TARGET)
  
def validate_indexes(maze: Maze) -> None:
  assert [square.index for square in maze] == list(
    range(len(maze.squares))
  ), "Wrong square.index"

def validate_rows_columns(maze: Maze) -> None:
  for y in range(maze.height):
    for x in range(maze.width):
      square = maze[y*maze.width + x]
      assert square.row==y, "Wrong square.row"
      assert square.column==x, "Wrong square.column"

def validate_start(maze: Maze) -> None:
  assert 0 < sum(
    1 for square in maze if square.role is Role.START
  ), "Must be at least 1 start state"

def validate_target(maze: Maze):
  assert 0 < sum(
    1 for square in maze if square.role is Role.TARGET
  ), "Must be at least 1 target state"