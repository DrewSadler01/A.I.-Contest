import random
from Pente import *

class asadler1(Player):
  def __init__(self, timeLimit):
    Player.__init__(self, timeLimit)
  
  def findMove(self, state):
    depth = 1
    while self.timeRemaining():
      if state.getTurn() % 2 == 0:
        (v, m) = self.maxPlayer(state, depth, -1e6, 1e6)
        self.setMove(m)
      else:
        (v, m) = self.minPlayer(state, depth, -1e6, 1e6)
        self.setMove(m)
      depth += 1

    print(state.moveToStr(m), v)

  def maxPlayer(self, state, depth, alpha, beta):
    if state.gameOver(): 
      w = state.winner()
      if w == 0:
        return (1-1e-6*state.getTurn(),tuple())
      if w == 1:
        return (0+1e-6*state.getTurn(), tuple())
      return (.5,None)

    if depth <= 0: return (self.heuristic(state),tuple())
    
    #actions = state.neighborhood(2)
    actions = self.candidateMoves(state)
    if len(actions) == 0:
      actions = state.actions()
      
    best = (-1e6, tuple())
    for a in actions:
      result = state.result(a)
      (v, m) = self.minPlayer(result, depth-1, alpha, beta)
      
      if v > beta: return (v, a)
      
      best = max(best, (v,a))
      alpha = max(alpha, v)
        
    return best

  def minPlayer(self, state, depth, alpha, beta):
    if state.gameOver():
      w = state.winner()
      if w == 0:
        return (1-1e-6*state.getTurn(),tuple())
      if w == 1:
        return (0+1e-6*state.getTurn(), tuple())
      return (.5,None)

    if depth <= 0: return (self.heuristic(state),tuple())
    
    #actions = state.neighborhood(2)
    actions = self.candidateMoves(state)
    if len(actions) == 0:
      actions = state.actions()
      
    best = (1e6, tuple())
    for a in actions:
      result = state.result(a)
      (v, m) = self.maxPlayer(result, depth-1, alpha, beta)
      
      if v < alpha: return (v, a)
      
      best = min(best, (v,a))
      beta = min(beta, v)
      
    return best
    
  def candidateMoves(self, state):
    
    w = state.winningMoves()
    if len(w) > 0:
      return w
    
    b = state.blockingMoves()
    if len(b) > 0:
      return b
      
    moveValue = {}
    
    # Captures and blocks
    for m in state.patternLocations('BWW_'):
      moveValue[m] = moveValue.get(m, 0) + 256 * (state.getCaptures()[0]+1)
    for m in state.patternLocations('WBB_'):
      moveValue[m] = moveValue.get(m, 0) + 256 * (state.getCaptures()[1]+1)
    
    # Open 3s and blocking
    for m in state.patternLocations(' BBB_w'):
      moveValue[m] = moveValue.get(m, 0) + 1024
    for m in state.patternLocations(' WWW_b'):
      moveValue[m] = moveValue.get(m, 0) + 1024
      
    # Open 2s and blocking
    for m in state.patternLocations(' BB_w'):
      moveValue[m] = moveValue.get(m, 0) + 128
    for m in state.patternLocations(' WW_b'):
      moveValue[m] = moveValue.get(m, 0) + 128

    # Adjacent
    for m in state.patternLocations('B_'):
      moveValue[m] = moveValue.get(m, 0) + 16
    for m in state.patternLocations('W_'):
      moveValue[m] = moveValue.get(m, 0) + 16

    # Two away
    for m in state.patternLocations('B _'):
      moveValue[m] = moveValue.get(m, 0) + 4
    for m in state.patternLocations('W _'):
      moveValue[m] = moveValue.get(m, 0) + 4
      
    options = []
    for (k,v) in moveValue.items():
      options.append((-v + random.random()*1e-4,k))
    random.shuffle(options)
    options.sort()
    if len(options) > 10:
      options = options[:10]
      
    return [ m for (v,m) in options ]
    
    
  def heuristic(self, state):
    h = .5
    if state.getTurn() % 2 == 0:
      h += .05 * state.patternCount('BBBB ') - .025 * state.patternCount('WWWW ')
      h += .2 * state.patternCount(" BBBB ") - .1 * state.patternCount(" WWWW ");
      h += .1 * state.patternCount(" BBB ") - .05 * state.patternCount(" WWW ");
      h += .1 * state.patternCount(" BB B ") - .05 * state.patternCount(" WW W ");
      h += .05 * (state.getCaptures()[0]+1) - .025 * (state.getCaptures()[1]+1);
      h += .006 * state.patternCount(" BB ") - .003 * state.patternCount(" WW ");
      h += .006 * state.patternCount(" B B ") - .003 * state.patternCount(" W W ");
      h += .013* state.patternCount("BWW ") * (state.getCaptures()[0]+1) - .006 * state.patternCount("WBB ") * (state.getCaptures()[1]+1);    
    else:
      h += .025 * state.patternCount('BBBB ') - .05 * state.patternCount('WWWW ')
      h += .1 * state.patternCount(" BBBB ") - .2 * state.patternCount(" WWWW ");
      h += .05 * state.patternCount(" BBB ") - .1 * state.patternCount(" WWW ");
      h += .05 * state.patternCount(" BB B ") - .1 * state.patternCount(" WW W ");
      h += .05 * (state.getCaptures()[0]+1) - .05 * (state.getCaptures()[1]+1);
      h += .003 * state.patternCount(" BB ") - .006 * state.patternCount(" WW ");
      h += .003 * state.patternCount(" B B ") - .006 * state.patternCount(" W W ");
      h += .006* state.patternCount("BWW ") * (state.getCaptures()[0]+1) - .013 * state.patternCount("WBB ") * (state.getCaptures()[1]+1);    
    
    return h
