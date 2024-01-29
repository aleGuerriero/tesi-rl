import array
import pathlib

from typing import Iterator

from mazeb.models.border import Border
from mazeb.models.role import Role
from mazeb.models.square import Square
from mazeb.persistence.file_format import FileBody, FileHeader

FORMAT_VERSION: int = 1

def dump_squares(
    width: int,
    height: int,
    squares: tuple[Square, ...],
    path: pathlib.Path
):
  header, body = serialize(width, height, squares)
  with path.open(mode="wb") as file:
    header.write(file)
    body.write(file)

def load_squares(path: pathlib.Path) -> Iterator[Square]:
  with path.open("rb") as file:
    header = FileHeader.read(file)
    if header.format_version != FORMAT_VERSION:
      raise ValueError("Unsupported file format version")
    body = FileBody.read(header, file)
    return deserialize(header, body)
  
def deserialize(header: FileHeader, body: FileBody) -> Iterator[Square]:
  for index, square_value in enumerate(body.square_values):
    row, column = divmod(index, header.width)
    border, role = decompress(square_value)
    yield Square(index, row, column, border, role)

def decompress(square_value: int) -> tuple[Border, Role]:
  return Border(square_value & 0xf), Role(square_value >> 4)

def serialize(
    width: int,
    height: int,
    squares: [Square, ...]
) -> tuple[FileHeader, FileBody]:
  header = FileHeader(FORMAT_VERSION, width, height)
  body = FileBody(array.array("B", map(compress, squares)))
  return header, body

def compress(square: Square) -> int:
  return (square.role << 4) | square.border.value

