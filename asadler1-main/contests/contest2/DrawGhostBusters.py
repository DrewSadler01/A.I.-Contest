from cs1graphics import *

from Maze import *

class DrawGhostBusters:
  """Render GhostBusters graphically"""
  
  def __init__(self, maze, scale):
    self._maze = maze
    self._scale = scale
    
    self._canvas = Canvas(self._maze._size*scale, self._maze._size*scale, title='GhostBusters')
    self._canvas.setBackgroundColor('black')
    self._canvas.setAutoRefresh(False)
    
    self._rectangles = {}
    for x in range(self._maze._size):
      for y in range(self._maze._size):
        loc = (x,y)
        if self._maze.isWall(loc):
          r = Rectangle(scale,scale, Point((x+.5)*scale, (y+.5)*scale))
          r.setBorderWidth(0)
          r.setFillColor('tan')
          self._canvas.add(r)
        else:
          r = Rectangle(scale,scale, Point((x+.5)*scale, (y+.5)*scale))
          r.setBorderWidth(0)
          r.setFillColor('black')
          self._rectangles[loc] = r
          self._canvas.add(r)
          
    loc = self._maze.getStart()
    self._pacman = Circle(.4*scale, Point((loc[0]+.5)*scale, (loc[1]+.5)*scale))
    self._pacman.setFillColor('yellow')
    self._canvas.add(self._pacman)
    
    self._circles = []
          
    self._canvas.refresh()
          
  def render(self, pacmanLocation, ghostLocations, noisyDistances, ghostActualLocations):
      
    for x in range(self._maze._size):
      for y in range(self._maze._size):
        loc = (x,y)
        if self._maze.isFree((x,y)):
          color = [0,0,0]
          for i in range(len(ghostLocations)):
            if ghostLocations[i] and max(ghostLocations[i].values()) > 0:
              color[i] = int(255*((ghostLocations[i].get(loc,0)/max(ghostLocations[i].values()))**.2))
          self._rectangles[loc].setFillColor(Color(tuple(color)))

    self._pacman.moveTo((pacmanLocation[0]+.5)*self._scale, (pacmanLocation[1]+.5)*self._scale)
    
    for c in self._circles:
      self._canvas.remove(c)
    self._circles = []
    for i in range(len(noisyDistances)):
      if noisyDistances[i]:
        r = noisyDistances[i] + (i-1)*.2
        c = Polygon()
        c.addPoint(Point(r*self._scale,0))
        c.addPoint(Point(0,r*self._scale))
        c.addPoint(Point(-r*self._scale,0))
        c.addPoint(Point(0,-r*self._scale))
        c.move((pacmanLocation[0]+.5)*self._scale, (pacmanLocation[1]+.5)*self._scale)
        c.setBorderColor( ['red','green','blue'][i] )
        c.setBorderWidth(.1*self._scale)
        self._canvas.add(c)
        self._circles.append(c)
    
    for i in range(len(ghostActualLocations)):
      if self._maze.inJail(ghostActualLocations[i]):
        (x,y) = ghostActualLocations[i]
        c = Circle(.4*self._scale)
        c.moveTo((x+.5)*self._scale, (y+.5)*self._scale)
        c.setFillColor(['red','green','blue'][i])
        self._canvas.add(c)
        self._circles.append(c)
    
    self._canvas.refresh()
