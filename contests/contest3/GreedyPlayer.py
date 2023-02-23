import random
from Pente import *

class GreedyPlayer(Player):
  def __init__(self, timeLimit):
    Player.__init__(self, timeLimit)
  
  def findMove(self, state):
    actions = state.neighborhood(1)
    if len(actions) == 0:
      actions = state.actions()
      
    player = state.getTurn() % 2
    
    # Make winning move
    for a in actions:
      r = state.result(a)
      if r.gameOver() and r.winner() == player:
        self.setMove(a)
        return
        
    # Block winning moves
    if player == 0:
      blockingLocations = state.patternLocations('_BBBB') + state.patternLocations('B_BBB')
      blockingLocations += state.patternLocations('BB_BB')
      if state.getCaptures()[1] == 4:
        blockingLocations += state.patternLocations('BWW_')
    else:
      blockingLocations = state.patternLocations('_WWWW') + state.patternLocations('W_WWW')
      blockingLocations += state.patternLocations('WW_WW')
      if state.getCaptures()[1] == 4:
        blockingLocations += state.patternLocation('WBB_')
    if len(blockingLocations) > 0:
      self.setMove(blockingLocations[0])
      return        
        
    # Capture a piece
    for a in actions:
      if r.numCaptures(a) > 0:
        self.setMove(a)
        return
        
    # Block a capture
    if player == 0:
      blockingLocations = state.patternLocations('BWW_')
    else:
      blockingLocations = state.patternLocations('WBB_')
    if len(blockingLocations) > 0:
      self.setMove(blockingLocations[0])
      return            
        
    options = []
    for a in actions:
      r = state.result(a)
      h = state.patternCount('bbbbb') - state.patternCount('wwwww')
      if player == 1:
        h = -h
      options.append((h,random.random(), a))
    options.sort()
    
    self.setMove(options[-1][2])
    
