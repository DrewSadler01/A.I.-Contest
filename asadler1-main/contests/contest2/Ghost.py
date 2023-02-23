from random import *

class Ghost:
  """Base class for representing a ghost."""
  
  def __init__(self, maze):
    self._maze = maze
    
    self._location = None
    while self._location is None:
      r = randint(0, self._maze._size)
      c = randint(0, self._maze._size)
      
      if self._maze.isFree((c,r)) and (c,r) != self._maze.getStart():
        self._location = (c,r)
        
  def inJail(self):
    return self._location in [(4,5),(5,5),(6,5)]
    
  def getLocation(self):
    return self._location
    
  def setLocation(self, loc):
    self._location = loc
    
  def moveOptions(self, loc, pacmanLocation):
    pacmanDist = self._maze.mazeDistance(loc, pacmanLocation)
    
    safe = self._maze.safeDirections(loc)
    options = []
    for d in 'NESW':
      if safe[d]:
        adj = self._maze.adjacent(loc, d)
        if pacmanDist > 10:
          options.append(adj)
        elif self._maze.mazeDistance(adj, pacmanLocation) > pacmanDist :
          options.append(adj)
          
    if len(options) > 0:
      return options
    return [loc]    
    
  def move(self, ghostLoc, pacmanLocation):
    options = self.moveOptions(ghostLoc, pacmanLocation)
    return options[randint(0,len(options)-1)]
