from mazeenv.agents.agent import Agent

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