from enum import IntFlag, auto

class Border(IntFlag):
  EMPTY=0
  TOP=auto()
  BOTTOM=auto()
  LEFT=auto()
  RIGHT=auto()

  @property
  def corner(self) -> bool:
    return self in (
      self.TOP | self.RIGHT,
      self.TOP | self.LEFT,
      self.BOTTOM | self.LEFT,
      self.BOTTOM | self.RIGHT
    )
  
  @property
  def dead_end(self) -> bool:
    return bin(self).count('1') == 3
  
  @property
  def intersection(self) -> bool:
    return bin(self).count('1') < 2