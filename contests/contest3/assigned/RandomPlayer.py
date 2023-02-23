import random
from Pente import *

class RandomPlayer(Player):
  def __init__(self, timeLimit):
    Player.__init__(self, timeLimit)
  
  def findMove(self, state):
    actions = state.neighborhood(1)
    if len(actions) == 0:
      actions = state.actions()
    self.setMove(random.choice(actions))
