import numpy as np
import random

from gymnasium import spaces

class EpsilonGreedy:
  
  def __init__(self, epsilon):
    self.epsilon = epsilon

  def select(self, action_space: spaces, state, qtable):
    
    if random.uniform(0, 1)<self.epsilon:
      action = action_space.sample()
    else:
      action = action_space.sample() if np.all(qtable[state])==qtable[state, 0] else np.argmax(qtable[state])

    return action