import struct
import array

from dataclasses import dataclass
from typing import BinaryIO

NUM: bytes = b'MAZE'

@dataclass(frozen=True)
class FileHeader:
  format_version: int
  width: int
  height: int

  @classmethod
  def read(cls, file: BinaryIO) -> "FileHeader":
    assert (
      file.read(len(NUM)) == NUM
    ), "Unknown file type"
    format_version, = struct.unpack("B", file.read(1))
    width, height = struct.unpack("<2I", file.read(2 * 4))
    return cls(format_version, width, height)

  def write(self, file: BinaryIO):
    file.write(NUM)
    file.write(struct.pack('B', self.format_version))
    file.write(struct.pack('<2I', self.width, self.height))

@dataclass(frozen=True)
class FileBody:
  square_values: array.array

  @classmethod
  def read(cls, header: FileHeader, file: BinaryIO) -> "FileBody":
    return cls(
      array.array("B", file.read(header.width * header.height))
    )
  
  def write(self, file: BinaryIO) -> None:
    file.write(self.square_values.tobytes())
