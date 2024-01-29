from random import choice
from pathlib import Path

from mazeb.models.square import Square
from mazeb.models.border import Border
from mazeb.models.maze import Maze
from mazeb.models.role import Role

from mazeb.view.render import preview

from mazeb.persistence.serializer import dump_squares

class MazeBuilder:

  def __init__(self, width, height) -> None:
    self.width = width
    self.height = height
  
  def gen_maze(self):
    self.squares = [Square(row*self.width+col, row, col, Border.TOP | Border.BOTTOM | Border.LEFT | Border.RIGHT) for row in range(self.height) for col in range(self.width)]
    self.squares[0] = Square(0, 0, 0, Border.TOP | Border.BOTTOM | Border.LEFT | Border.RIGHT, Role.START)
    
    for i in range(self.height):

      if i == self.height-1:
        for j in range(self.width-2):
          self.remove_walls(self.squares[i*self.width + j], self.squares[i*self.width + j+1])
        break

      for j in range(self.width):
        if j == self.width-1:
          self.remove_walls(self.squares[i*self.height + j], self.squares[(i+1)*self.height + j])
          continue

        remove_bottom = choice([True, False])
        if remove_bottom:
          self.remove_walls(self.squares[i*self.height + j], self.squares[(i+1)*self.height + j])
        else:
          self.remove_walls(self.squares[i*self.width + j], self.squares[i*self.width + j+1])

        remove_extra = choice([True, False, False, False])
        if remove_extra and i!=0:
          self.remove_walls(self.squares[i*self.height + j], self.squares[(i-1)*self.height + j])
        elif remove_extra and j!=0:
          self.remove_walls(self.squares[i*self.width + j], self.squares[i*self.width + j-1])

    self.squares[-1] = Square(self.squares[-1].index, self.squares[-1].row, self.squares[-1].column, self.squares[-1].border, Role.TARGET)

    return Maze(squares=self.squares)

  #Getting unvisited neighbours
  def get_neighbours(self, square: Square):
    neighbours = []
    for direction in [(0, -1), (-1, 0), (0, 1), (1, 0)]:
      x, y = square.column + direction[0], square.row + direction[1]
      neighbour = self.check_cell(x, y)
      if neighbour and neighbour.index not in self.visited:
        neighbours.append(neighbour)
    return neighbours
    
  def check_cell(self, x, y):
    if x < 0 or x > self.width-1 or y < 0 or y > self.height-1:
      return False
    return self.squares[y*self.width + x]
  
  def remove_walls(self, current: Square, next: Square):
    dx = current.column - next.column
    curr_border = current.border
    next_border = next.border
    if dx == 1:
      curr_border &= ~Border.LEFT
      next_border &= ~Border.RIGHT
    elif dx == -1:
      curr_border &= ~Border.RIGHT
      next_border &= ~Border.LEFT
    dy = current.row - next.row
    if dy == 1:
      curr_border &= ~Border.TOP
      next_border &= ~Border.BOTTOM
    elif dy == -1:
      curr_border &= ~Border.BOTTOM
      next_border &= ~Border.TOP

    self.squares[current.index] = Square(current.index, current.row, current.column, curr_border, current.role)
    self.squares[next.index] = Square(next.index, next.row, next.column, next_border, next.role)

def main():
  import argparse

  parser = argparse.ArgumentParser()
  parser.add_argument(
    'width',
    type=int
  )
  parser.add_argument(
    'height',
    type=int
  )

  args = parser.parse_args()

  builder = MazeBuilder(args.width, args.height)
  maze = builder.gen_maze()

  preview(maze)

  ans = input('Save maze? Y/n ')
  if not ans=='n':
    folder_name = input('Insert file name: ')
    folder_path = Path(folder_name)
    folder_path.mkdir(parents=True, exist_ok=True)
    src = folder_path / Path('src')
    src.mkdir(parents=True, exist_ok=True)
    file_name = folder_name + '.maze'
    path = src / Path(file_name)
    dump_squares(maze.width, maze.height, maze.squares, path)
    print(f'Saved as {file_name}')

if __name__=='__main__':
  main()