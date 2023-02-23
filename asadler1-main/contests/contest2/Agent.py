from Maze import *
from Ghost import *

from time import *

class Agent:
  def __init__(self, maze):
    self._maze = maze
    self._ghostPredictions = GhostPredictor(maze)
    
    self._startTime = 0.
    self._move = None
    
  def startTimer(self):
    self._move = ' '
    self._startTime = time()
    
  def timeRemaining(self):
    return self._startTime + 5 - time()
    
  def setMove(self, move):
    if self.timeRemaining():
      self._move = move
    
  def getMove(self):
    return self._move
    
  def play(self, pacmanLocation):
    best = ' '
    bestDist = 10000.
    
    options = [ d for d in 'NESW' if self._maze.safeDirections(pacmanLocation)[d] ]
        
    for move in options:
      ghostDist = [0.,0.,0.]
      for i in range(3):
        for (k,v) in self._ghostPredictions.getProbs()[i].items():
          ghostDist[i] += v * self._maze.mazeDistance(self._maze.adjacent(pacmanLocation, move), k)
      if min(ghostDist) < bestDist:
        bestDist = min(ghostDist)
        best = move
        self.setMove(best)
  
  def applyDistances(self, distances, pacmanLocation):
    self._ghostPredictions.applyDistances(distances, pacmanLocation)
    
  def pacmanMoved(self, pacmanLocation, caught):
    self._ghostPredictions.pacmanMoved(pacmanLocation, caught)
    self._ghostPredictions.moveGhosts(pacmanLocation)

  def getProbs(self):
    return self._ghostPredictions.getProbs()

class GhostPredictor:
  def __init__(self, maze):
    self._maze = maze
    
    self._prob = []
    for _ in range(3):
      prob = {}
      total = 0.
      for r in range(maze.getSize()):
        for c in range(maze.getSize()):
          if self._maze.isFree((c,r)) and (c,r) != self._maze.getStart():
            prob[(c,r)] = 1.
            total += 1.
      for k in prob:
        prob[k] /= total
      self._prob.append(prob)
      
  def applyDistances(self, noisyDistances, pacman):
    newProbs = []
    for i in range(3):
      prob = self._prob[i]
      dist = noisyDistances[i]
      
      p2 = { k : v*self._maze.noisyDistanceProb(dist, self._maze.manhattanDistance(pacman, k)) + 1e-6 for (k,v) in prob.items() }

      total = sum(p2.values())
      for k in p2:
        p2[k] /= total
      newProbs.append(p2)
    self._prob = newProbs    
    
  def pacmanMoved(self, pacmanLoc, caught):
    for i in range(3):
      if caught[i]:
        self._prob[i] = { self._maze.jailLocation(i) : 1. }
      else:
        self._prob[i][pacmanLoc] = 0.
      
    
  def moveGhosts(self, pacmanLoc):
    newProbs = []
    for i in range(3):
      prob = self._prob[i]
      p2 = {}
      
      for (k,v) in prob.items():
        options = Ghost(self._maze).moveOptions(k, pacmanLoc)
        for o in options:
          p2[o] = p2.get(o,0) + v/len(options) + 1e-6
          
      p2[pacmanLoc] = 0.
      total = sum(p2.values())
      for k in p2:
        p2[k] /= total
      newProbs.append(p2)
    self._prob = newProbs    
    
  def getProbs(self):
    return self._prob
