from mazeenv.agents import Agent

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