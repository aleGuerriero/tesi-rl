from abc import ABC, abstractmethod

import numpy as np

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