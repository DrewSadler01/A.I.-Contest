from copy import copy
from random import choice, randint

class SlidingTilePuzzle:
  def __init__(self, size):
    self._size = size
    self._initial = tuple(range(size*size))
    self._goal = tuple(range(size*size))
    
  def setInitial(self, initial):
    self._initial = copy(initial)
    
  def getInitial(self):
    return copy(self._initial)
    
  def getGoal(self):
    return copy(self._goal)
    
  def isGoal(self, state):
    for i in range(self._size*self._size):
      if state[i] != i:
        return False
    return True
    
  def actions(self, state):
    emptyTileIndex = state.index(0)
    coords = (emptyTileIndex // self._size, emptyTileIndex % self._size)
    actions = []
    
    if coords[0] > 0:
      actions.append('D')
    if coords[0] < self._size - 1:
      actions.append('U')
    if coords[1] > 0:
      actions.append('R')
    if coords[1] < self._size - 1:
      actions.append('L')
  
    return actions

  def result(self, state, action):
    emptyTileIndex = state.index(0)
    newState = list(state)
    
    if action == 'D':
      newState[emptyTileIndex] = state[emptyTileIndex - self._size]
      newState[emptyTileIndex - self._size] = 0
      return tuple(newState)
    if action == 'U':
      newState[emptyTileIndex] = state[emptyTileIndex + self._size]
      newState[emptyTileIndex + self._size] = 0
      return tuple(newState)
    if action == 'R':
      newState[emptyTileIndex] = state[emptyTileIndex - 1]
      newState[emptyTileIndex - 1] = 0
      return tuple(newState)
    if action == 'L':
      newState[emptyTileIndex] = state[emptyTileIndex + 1];
      newState[emptyTileIndex + 1] = 0;
      return tuple(newState)
    
  def randomState(self, moves=200):
    state = self.getInitial()
    lastAction = ''
    if randint(0,1) == 0:
      moves += 1
    for i in range(moves):
      possibleActions = self.actions(state)
      if lastAction == 'D':
        possibleActions.remove('U')
      elif lastAction == 'U':
        possibleActions.remove('D')
      elif lastAction == 'L':
        possibleActions.remove('R')
      elif lastAction == 'R':
        possibleActions.remove('L')
      action = choice(possibleActions)
      state = self.result(state, action)
      lastAction = action
    return state
    
  def reverse(self, moves):
    reversedMoves = ''
    for m in moves[::-1]:
      reversedMoves += {'U':'D','D':'U','L':'R','R':'L'}[m]
    return reversedMoves

  
