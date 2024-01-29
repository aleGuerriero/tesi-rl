from __future__ import annotations

import networkx as nx

from mazeb.graphs.converter import make_graph
from mazeb.models.maze import Maze
from mazeb.models.solution import Solution

def solve(maze: Maze) -> Solution | None:
  try:
    return Solution(
      squares=tuple(
        nx.shortest_path(
          make_graph(maze.squares, maze.width),
          source=maze.start,
          target=maze.target
        )
      )
    )
  except nx.NetworkXException:
    return None
