import networkx as nx

from mazeb.models.maze import Square
from mazeb.models.border import Border

def make_graph(squares: tuple[Square, ...], width) -> nx.DiGraph:
  G = nx.DiGraph()
  for i, node in enumerate(squares):
    #Look right
    if (not node.border & Border.RIGHT) and i+1<len(squares):
      G.add_edge(node, squares[i+1], action=0)
      G.add_edge(squares[i+1], node, action=2)
    #Look down
    if (not node.border & Border.BOTTOM) and i+width<len(squares):
      G.add_edge(node, squares[i + width], action=3)
      G.add_edge(squares[i + width], node, action=1)
  return G