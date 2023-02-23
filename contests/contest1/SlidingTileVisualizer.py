from cs1graphics import *
import time
from copy import *

class SlidingTileVisualizer:
  def __init__(self, size, initial, puzzle, width):
    self._width = width
    self._tileWidth = self._width/size
    self._size = size
    self._initial = initial
    self._puzzle = puzzle
    
    self._canvas = Canvas(self._width, self._width)
    self._canvas.setBackgroundColor('gray')
    self._tiles = [None]
    for i in range(1,size*size):
      t = TextBox(self._tileWidth, self._tileWidth)
      t.setMessage(str(i))
      t.setFontSize(.6*self._tileWidth)
      t.setFillColor('tan')
      t.setBorderColor('black')
      t.setBorderWidth(3)
      t.moveTo(-self._width,-self._width)
      self._tiles.append(t)
      self._canvas.add(t)
      
    self.draw(initial)
      
  def draw(self, state):
    for i in range(self._size*self._size):
      r = i%self._size
      c = i//self._size
      
      t = state[i]
      
      if t > 0:
        self._tiles[t].moveTo((r+.5)*self._tileWidth, (c+.5)*self._tileWidth)
        
  def slide(self,oldState,newState):
    self.draw(oldState)
    for step in range(51):
      for t in range(1,self._size*self._size):
        i1 = oldState.index(t)
        r1 = i1%self._size
        c1 = i1//self._size
        i2 = newState.index(t)
        r2 = i2%self._size
        c2 = i2//self._size
        
        x = .02*(50-step)*r1 + .02*step*r2
        y = .02*(50-step)*c1 + .02*step*c2
        
        self._tiles[t].moveTo((x+.5)*self._tileWidth, (y+.5)*self._tileWidth)
      time.sleep(.005)
    self.draw(newState)    
        
    
  def animate(self, solution):
    current = copy(self._initial)
    for a in solution:
      nextState = self._puzzle.result(current, a)
      self.slide(current,nextState)
      current = nextState
      time.sleep(.5)
