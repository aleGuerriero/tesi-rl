from enum import IntEnum, auto

class Role(IntEnum):
  NONE=0
  START=auto()
  TARGET=auto()
  EXTERIOR=auto()
  WALL=auto()