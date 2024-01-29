from __future__ import annotations

import networkx as nx
import numpy as np

from gymnasium import Wrapper, spaces
from functools import cache

from .maze_env import MazeEnv
from mazeb.models.square import Square
from mazeb.models.maze import Maze
from mazeb.graphs.converter import make_graph

class AlgoWrapper(Wrapper):

  def __init__(
      self,
      env: MazeEnv,
      obs_range: int | None = None,
      eps_reward: float | None = 1
  ):
    super().__init__(env)
    self.env = env
    self.maze: Maze = env.unwrapped.maze
    self.eps_reward = eps_reward

    #Spazio delle azioni con i possibili algoritmi
    self.action_space = spaces.Discrete(7)

    self.obs_range = obs_range

  def step(self, action):
    if action < 4:
      obs, _, terminated, truncated, _ = self.env.step(action)
      reward = -(self.obs_range+1)**2
    else:
      source = self.env.unwrapped.agent_pos
      G, target = self._get_graph(source)

      if action==4:
        path, n_nodes = dfs_search(G, source, target)
      elif action==5:
        path, n_nodes = bfs_search(G, source, target)
      elif action==6:
        path, n_nodes = astar_search(G, source, target)

      if path:
        tot_reward = 0
        for act in path:
          obs, step_reward, terminated, truncated, _ = self.env.step(act)
          tot_reward += step_reward
        reward = -n_nodes*self.eps_reward+(tot_reward*(1-self.eps_reward))
      else:
        truncated = True

    if truncated:
      obs = self.env.unwrapped.agent_pos.index
      terminated = False
      reward = -self.maze.width

    return obs, reward, terminated, truncated, {}
  
  @cache
  def _get_graph(self, source: Square):
    if self.obs_range:
      indexes = [(i, j) for i in set(np.clip(range(source.column-self.obs_range, source.column+self.obs_range), 0, self.maze.width-1)) for j in set(np.clip(range(source.row-self.obs_range, source.row+self.obs_range), 0, self.maze.height-1))]
      squares_list = set()
      for x, y in indexes:
        squares_list.add(self.maze[x+y*self.maze.width])
      obs_width = min(self.maze.width, max(ind[0] for ind in indexes)) - max(0, min(ind[0] for ind in indexes)) + 1

      #Generate the graph of connected components from source
      graph = make_graph(sorted(list(squares_list), key=lambda x: x.index), obs_width)
      reachable = set(nx.dfs_preorder_nodes(graph, source))
      G = graph.subgraph(reachable)

      #Looking for a suitable target
      target = source
      min_dist = np.infty
      for node in G:
        dist = manhattan_dist(node, self.maze.target)
        if dist < min_dist:
          min_dist = dist
          target = node

      return G, target
    else:
      return make_graph(self.maze.squares, self.maze.width), self.maze.target

@cache
def dfs_search(G: nx.DiGraph, source: Square, target: Square):
  visited = set()
  stack = [source]
  paths = {source: None}
  n_nodes = 0

  while stack:
    curr_node = stack.pop()
    n_nodes += 1

    if curr_node==target:
      break

    if curr_node not in visited:
      visited.add(curr_node)
      neighbors = list(G.neighbors(curr_node))
      for neighbor in neighbors:
        if neighbor not in visited:
          stack.append(neighbor)
          paths[neighbor] = curr_node
  
  path = []
  while paths[target] is not None:
    path.append(G.get_edge_data(paths[target], target)['action'])
    target = paths[target]
  path.reverse()

  return path, n_nodes

@cache
def bfs_search(G: nx.DiGraph, source: Square, target: Square):
  visited = set()
  queue = [source]
  paths = {source: None}
  n_nodes = 0

  while queue:
    curr_node = queue.pop(0)
    n_nodes += 1
    if curr_node==target:
      break

    if curr_node not in visited:
      visited.add(curr_node)
      neighbors = list(G.neighbors(curr_node))
      for neighbor in neighbors:
        if neighbor not in visited:
          queue.append(neighbor)
          paths[neighbor] = curr_node
  
  path = []
  while paths[target] is not None:
    path.append(G.get_edge_data(paths[target], target)['action'])
    target = paths[target]
  path.reverse()

  return path, n_nodes

@cache
def astar_search(G: nx.DiGraph, source: Square, target: Square):
  n_nodes = 0

  visited = set()
  #queue[0] = h(n)
  queue = [(0, source)]
  paths = {source: None}
  n_nodes = 0

  while queue:
    _, curr_node = queue.pop(0)
    n_nodes += 1
    if curr_node==target:
      break

    if curr_node not in visited:
      visited.add(curr_node)
      neighbors = list(G.neighbors(curr_node))
      for neighbor in neighbors:
        if neighbor not in visited:
          queue.append((manhattan_dist(neighbor, target), neighbor))
          paths[neighbor] = curr_node

      queue.sort(key=lambda x: x[0])

  path = []
  while paths[target] is not None:
    path.append(G.get_edge_data(paths[target], target)['action'])
    target = paths[target]
  path.reverse()

  return path, n_nodes

def manhattan_dist(a: Square, b: Square):
  return np.linalg.norm(
    np.array((a.column, a.row)) - np.array((b.column, b.row)), ord=1
  )
