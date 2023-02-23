from time import time

class SlidingTileSolver:
  def __init__(self, problem, maxTime):
    self._problem = problem
    self._maxTime = maxTime
    self._time = time()
    self._numExpansions = 0
    
  def timeRemaining(self):
    return time() < self._time + self._maxTime
    
  def solution(self):
    self._time = time()
    moveSequence = self.solve()
    solutionTime = time() - self._time
    
    print('Solution =', moveSequence)
    print('Moves to regenerate puzzle =', self._problem.reverse(moveSequence))
    print('Solution length =', len(moveSequence))
    print('Number of nodes expanded = ', self._numExpansions)
    print('Search time per node =', solutionTime / self._numExpansions)
    print('Search time =', solutionTime)
    
    return moveSequence
    
  def getPuzzle(self):
    return self._problem
    
