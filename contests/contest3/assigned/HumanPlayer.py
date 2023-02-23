import random
from Pente import *

class HumanPlayer(Player):
  def __init__(self, timeLimit):
    Player.__init__(self, timeLimit)
  
  def findMove(self, state):
    move = None
    while move is None:
      move = input('Enter you move (row first then column, e.g CF): ')
      move = move.upper()
      row = ord(move[0]) - ord('A')
      col = ord(move[1]) - ord('A')
        
      if not 0 <= row < 11: move = None
      if not 0 <= col < 11: move = None
      
      if (row,col) not in state.actions():
        print('Invalid move')
        move = None
      
    self.setMove((row,col))
