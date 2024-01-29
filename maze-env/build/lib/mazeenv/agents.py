from __future__ import annotations

from gymnasium import spaces
from abc import ABC, abstractmethod

import numpy as np
import random

AGENT_TYPE = [
  'qagent',
  'sarsa'
]

"""
Learner policy
"""
class Agent(ABC):
  def __init__(
      self,
      state_size,
      action_size,
      learning_rate,
      gamma
  ):
    self.state_size = state_size
    self.action_size = action_size
    self.learning_rate = learning_rate
    self.gamma = gamma
    self.reset_qtable()

  @abstractmethod
  def update():
    pass

  def reset_qtable(self):
    self.Qtable = np.zeros((self.state_size, self.action_size))

class QAgent(Agent):
  
  def __init__(
      self,
      state_size,
      action_size,
      learning_rate,
      gamma
  ):
    super().__init__(
      state_size,
      action_size,
      learning_rate,
      gamma
    )

  def update(self, action, state, reward, next_state):
    delta = reward + self.gamma*max(self.Qtable[next_state]) - self.Qtable[state, action]
    self.Qtable[state, action] += self.learning_rate*delta

class SARSAAgent(Agent):

  def __init__(
      self,
      state_size,
      action_size,
      learning_rate,
      gamma
  ):
    super().__init__(
      state_size,
      action_size,
      learning_rate,
      gamma
    )

  def update(self, state, action, reward, next_state, next_action):
    delta = (
      reward
      + self.gamma*self.Qtable[next_state, next_action]
      - self.Qtable[state, action]
    )
    self.Qtable[state, action] += self.learning_rate*delta
    
"""
Explorer policy
"""

class Explorer(ABC):

  @abstractmethod
  def select():
    pass

class EpsilonGreedy(Explorer):
  
  def __init__(self, epsilon):
    self.epsilon = epsilon

  def select(self, action_space: spaces, state, qtable):
    
    if random.uniform(0, 1)<self.epsilon:
      action = action_space.sample()
    else:
      action = action_space.sample() if np.all(qtable[state])==qtable[state, 0] else np.argmax(qtable[state])

    return action
  
class Greedy(Explorer):

  def select(state, qtable):
    return np.argmax(qtable[state])