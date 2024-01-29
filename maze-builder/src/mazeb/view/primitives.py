import pygame

from typing import NamedTuple, Protocol

class Primitive(Protocol):
  def draw(self) -> None:
    ...

class Point(NamedTuple):
  x: int
  y: int

  def translate(self, x=0, y=0) -> 'Point':
    return Point(self.x+x, self.y+y)

class Line(NamedTuple):
  start: Point
  end: Point

  def draw(self, surface: pygame.Surface) -> None:
    pygame.draw.line(
      surface=surface,
      color=(255, 255, 255),
      start_pos=(self.start.x, self.start.y),
      end_pos=(self.end.x, self.end.y)
    )
