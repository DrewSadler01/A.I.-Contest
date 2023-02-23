from SlidingTilePuzzle import *
from SlidingTileSolver import *
from PriorityQueue import *

from math import *

class MySolver(SlidingTileSolver):  
  def __init__(self, problem, maxTime):
    SlidingTileSolver.__init__(self, problem, maxTime)
    
  # You need to redefine this function for your algorithm
  # It is currently using breadth-first search which is very slow
  def solve(self):
    frontier = PriorityQueue()
    frontier.push(0, (0, self._problem.getInitial()))
    seen = set()
    parent = dict()
    
    # Do not remove the timeRemaining check from the while loop
    while len(frontier) > 0 and self.timeRemaining():
      self._numExpansions += 1
      
      priority, (depth, currentState) = frontier.pop()
      seen.add(currentState)
      
      for action in self._problem.actions(currentState):
        resultingState = self._problem.result(currentState, action)
        if self._problem.isGoal(resultingState):
          # Goal reached
          parent[resultingState] = (currentState, action)
          path = ""
          current = resultingState
          while current != self._problem.getInitial():
            (current, action) = parent[current]
            path = action + path
          return path
          
        if resultingState not in seen:
          frontier.push(depth + 1 + self.heuristic(resultingState), (depth+1,resultingState))
          seen.add(resultingState)
          parent[resultingState] = (currentState, action)
          
    return []

  def heuristic(self, state):
    gridLength = sqrt(len(state))
    sum=0
    for index, value in enumerate(state):
      column = index%gridLength
      row = index//gridLength
      goalcol = value%gridLength
      goalrow = value//gridLength
      if value == 0:
        sum+=0
      else:
        sum+=(abs(row-goalrow)+abs(column-goalcol))
    return sum
