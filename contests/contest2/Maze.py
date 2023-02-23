from copy import *
from random import *

class Maze:
  """Stores the PacMan maze"""
  
  def __init__(self):
    """Set up the map."""
    self._size = 11
    self._map = [ 'WWWWWWWWWWW',
                  'W    W    W',
                  'W WW W WW W',
                  'W    S    W',
                  'WW WWWWW WW',
                  'A  WJJJW  B',
                  'WW WWWWW WW',
                  'W         W',
                  'W WW W WW W',
                  'W    W    W',
                  'WWWWWWWWWWW' ]
            
    self._errorDistribution = [0.012280533435671112, 0.018420800153506667, 0.027631200230260004, 0.04144680034539, 0.06217020051808501, 0.0932553007771275, 0.13988295116569127, 0.20982442674853688, 0.13988295116569127, 0.0932553007771275, 0.06217020051808501, 0.04144680034539, 0.027631200230260004, 0.018420800153506667, 0.012280533435671112]


    self._errorDistribution = [ 1.7**i for i in range(6) ]
    
    self._errorDistribution += self._errorDistribution[:-1][::-1]

    s = float(sum(self._errorDistribution))
    for i in range(len(self._errorDistribution)):
      self._errorDistribution[i] /= s
        
    # Calculate the distance in the map between any two locations
    free = set()
    self._dist = dict()
    for x in range(self._size):
      for y in range(self._size):
        loc = (x,y)
        if self.isFree(loc):
          free.add(loc)
          self._dist[(loc,loc)] = 0
    self._free = free
    frontier = set(self._dist.keys())
      
    changed = True
    while changed:
      changed = False
      currentDist = max(self._dist.values())
      for (loc1,loc2) in list(self._dist.keys()):
        if self._dist[(loc1,loc2)] == currentDist:
          for (d,v) in self.safeDirections(loc1).items():
            if v:
              newLoc1 = self.adjacent(loc1,d)
              if not (newLoc1,loc2) in self._dist:
                self._dist[(newLoc1,loc2)] = currentDist + 1
                changed = True
          for (d,v) in self.safeDirections(loc2).items():
            if v:
              newLoc2 = self.adjacent(loc2,d)
              if not (loc1,newLoc2) in self._dist:
                self._dist[(loc1,newLoc2)] = currentDist + 1
                changed = True
                
    # Calculate the distrubtion for noisy distances
    distribution = {}
    maxN = 0
    for d in range(1,2*self._size):
      for i in range(len(self._errorDistribution)):
        n = min(max(1,d+i-len(self._errorDistribution)/2), 2*self._size+2)
        maxN = max(n,maxN)
        distribution[(n,d)] = distribution.get((n,d), 0) + self._errorDistribution[i]
        
    for n in range(maxN+1):
      s = 0
      for ((n2,d),v) in distribution.items():
        if n == n2:
          s += v
          
      for ((n2,d),v) in distribution.items():
        if n == n2:
          distribution[(n,d)] /= s
          
    distribution[(0,0)] = 1.
    self._noisyDistanceProb = distribution
          
  def getSize(self):
    return self._size
    
  def getStart(self):
    """Return the location where PacMan starts in (x,y) format"""
    for r in range(len(self._map)):
      if 'S' in self._map[r]:
        return (self._map[r].index('S'), r)
        
  def getValid(self):
    """Return the set of valid locations for ghosts."""
    return self._free
          
  def isFree(self, location):
    """Check if the location is safe place to move."""
    (c,r) = location
    if not 0 <= c < len(self._map[0]):
      return False
    if not 0 <= r < len(self._map):
      return False
    return self._map[r][c] not in ['W','J']
    
  def inJail(self, location):
    """Check if the location is in jail,"""
    (c,r) = location
    return self._map[r][c] == 'J'
    
  def jailLocation(self, ghostId):
    count = 0
    for c in range(self._size):
      for r in range(self._size):
        if self._map[r][c] == 'J':
          if ghostId == count:
            return (c,r)
          else:
            count += 1
    
  def isWall(self, location):
    """Check if the location is a wall,"""
    (c,r) = location
    return self._map[r][c] == 'W'

  def safeDirections(self, location):
    """Return a dictionary if it's safe to move N, S, E, or W"""
    (c,r) = location
    if self._map[r][c] in ['A','B']:
      return {'N': False, 'S': False, 'E': True, 'W': True}
    else:
      d = {}
      d['N'] = self.isFree((c,r-1))
      d['S'] = self.isFree((c,r+1))
      d['E'] = self.isFree((c+1,r))
      d['W'] = self.isFree((c-1,r))
      return d
      
  def adjacent(self, location, direction):
    """Find the adjacent location.  Requires direction to be valid."""
    (c,r) = location
    if self._map[r][c] == 'A' and direction == 'W':
      return (len(self._map[0])-1,r)
    if self._map[r][c] == 'B' and direction == 'E':
      return (0,r)
    
    if direction == 'N':
      return (c,r-1)
    if direction == 'S':
      return (c,r+1)
    if direction == 'E':
      return (c+1,r)
    if direction == 'W':
      return (c-1,r)
    return 
        
  def manhattanDistance(self, location1, location2):
    """Returns the Manhattan distance between the two locations."""
    d = 1000000000
    w = len(self._map[0])
    for o in [-w,0,w]:
      d = min(d, abs(location1[0]+o-location2[0]) + abs(location1[1]-location2[1]))
    return d
      
  def mazeDistance(self, location1, location2):
    """Returns the length of the shortest path in the maze between the two locations."""
    return self._dist.get( (location1,location2), 1000)

  def noisyDistance(self, location1, location2):
    m = self.manhattanDistance(location1, location2)
    e = randomTerm(self._errorDistribution) - len(self._errorDistribution)/2
    return min(max(1,m+e), 2*self._size+2)
    
  def noisyDistanceProb(self, noisyD, d):
    return self._noisyDistanceProb.get((noisyD,d),0)
    

def randomTerm(coef):
  r = random()
  if isinstance(coef,list):
    for i in range(len(coef)):
      if r < coef[i]:
        return i
      r -= coef[i]
  if isinstance(coef,dict):
    for (k,v) in coef.items():
      if r < v:
        return k
      r -= v
