from cs1graphics import *

class Graphics:
  def __init__(self, width):
    scale = width/13
    
    self._canvas = Canvas(width, 15*scale)
    self._canvas.setTitle('Pente')
    self._canvas.setBackgroundColor('tan')
    self._canvas.setAutoRefresh(False)
    
    self._turn = Text('Turn: 0')
    self._turn.setFontSize(.85*scale)
    self._turn.moveTo(.5*width, .55*scale)
    self._canvas.add(self._turn)
    
    self._white = Text('White: 0')
    self._white.setFontSize(.85*scale)
    self._white.moveTo(.25*width, 1.5*scale)
    self._canvas.add(self._white)
    
    self._black = Text('Black: 0')
    self._black.setFontSize(.85*scale)
    self._black.moveTo(.75*width, 1.5*scale)
    self._canvas.add(self._black)

    for i in range(11):
      t = Text(chr(ord('A')+i))
      t.setFontSize(.8*scale)
      t.moveTo((1.5+i)*scale, 2.5*scale)
      self._canvas.add(t)
      t = Text(chr(ord('A')+i))
      t.setFontSize(.8*scale)
      t.moveTo((1.5+i)*scale, 14.6*scale)
      self._canvas.add(t)
      t = Text(chr(ord('A')+i))
      t.setFontSize(.8*scale)
      t.moveTo(.5*scale, (3.5+i)*scale)
      self._canvas.add(t)
      t = Text(chr(ord('A')+i))
      t.setFontSize(.8*scale)
      t.moveTo(12.5*scale, (3.5+i)*scale)
      self._canvas.add(t)
      
    for i in range(11):
      l = Path()
      l.setBorderWidth(.01*scale)
      l.addPoint(Point(1*scale,(3.5+i)*scale))
      l.addPoint(Point(12*scale,(3.5+i)*scale))
      self._canvas.add(l)
      l = Path()
      l.setBorderWidth(.01*scale)
      l.addPoint(Point((1.5+i)*scale,3*scale))
      l.addPoint(Point((1.5+i)*scale,14*scale))
      self._canvas.add(l)
      
    self._pieces = []
    for row in range(11):
      l = []
      for col in range(11):
        c = Circle(.45*scale)
        c.moveTo((1.5+col)*scale, (3.5+row)*scale)
        c.setBorderWidth(0)
        self._canvas.add(c)
        l.append(c)
      self._pieces.append(l)
      
    self._canvas.refresh()

  def draw(self, state):
    self._turn.setMessage(f'Turn: {state.getTurn()}')
    self._white.setMessage(f'White: {state.getCaptures()[0]}')
    self._black.setMessage(f'Black: {state.getCaptures()[1]}')
    
    for r in range(11):
      for c in range(11):
        p = state.getPosition((r,c))
        if p == 0:
          self._pieces[r][c].setFillColor('white')
        elif p == 1:
          self._pieces[r][c].setFillColor('black')
        else:
          self._pieces[r][c].setFillColor('transparent')
    
    self._canvas.refresh()
