import random
import copy
import time

class Pente:
  """11x11 Pente board"""
  
  fullBoard = 2721594159070714665531732635556843091967
  
  def __init__(self):
    self._gameOver = False
    self._winner = 0
    self._turn = 0
    self._positions = (0, 0)
    self._captures = (0, 0)    
    
  def __eq__(self, other):
    if self._positions != other._positions:
      return False
    if self._turn != other._turn:
      return False
    if self._captures != other._captures:
      return False
    if self._gameOver != other._gameOver:
      return False
    if self._winner != other._winner:
      return False
    return True
    
  def __hash__(self):
    return hash( (self._positions, self._captures, self._turn, self._winner, self._gameOver) )
    
  def getTurn(self):
    return self._turn
    
  def getCaptures(self):
    return tuple(self._captures)
    
  def gameOver(self):
    return self._gameOver
    
  def winner(self):
    return self._winner    
    
  def getPosition(self, location):
    for p in range(2):
      if (1 << (12*location[0]+location[1])) & self._positions[p]:
        return p
    return -1
    
  def actions(self):
    if self._turn == 0:
      return [(5,5)]
    elif self._turn == 1:
      return [ (r,c) for r in range(3,8) for c in range(3,8) if (r,c) != (5,5) ]
    
    occupied = self._positions[0] | self._positions[1]
    free = Pente.fullBoard ^ occupied
    
    options = []
    for row in range(11):
      for col in range(11):
        if (1 << (12*row+col)) & free:
          options.append( (row,col) )
          
    random.shuffle(options)
    return options
    
  def result(self, action):
    newState = Pente()
    newState._turn = self._turn + 1
    
    player = self._turn % 2
    positions = [0,0]
    captures = [0,0]
    positions[1-player] = self._positions[1-player]
    captures[player] = self._captures[player]
    captures[1-player] = self._captures[1-player]
    
    positions[player] = self._positions[player] | (1 << (12*action[0] + action[1]))
    for direction in [ (1,0), (-1,0), (0,1), (0,-1), (1,1), (1,-1), (-1,1), (-1,-1) ]:
      if 0 <= action[0] + 3*direction[0] < 11:
        if 0 <= action[1] + 3*direction[1] < 11:
          if self.getPosition((action[0]+direction[0], action[1]+direction[1])) == 1 - player:
            if self.getPosition((action[0]+2*direction[0], action[1]+2*direction[1])) == 1 - player:
              if self.getPosition((action[0]+3*direction[0], action[1]+3*direction[1])) == player:
                amount = (12*(action[0]+direction[0]) + action[1]+direction[1])
                if amount > 0:
                  positions[1-player] ^= 1 << amount
                else:
                  positions[1-player] ^= 1 >> (-amount)                
                amount = (12*(action[0]+2*direction[0]) + action[1]+2*direction[1])
                if amount > 0:
                  positions[1-player] ^= 1 << amount
                else:
                  positions[1-player] ^= 1 >> (-amount)
                captures[player] += 1
    
    newState._captures = tuple(captures)
    newState._positions = tuple(positions)
    
    if newState._captures[player] >= 5 or (player == 0 and newState.patternCount('WWWWW') > 0) or (player == 1 and newState.patternCount('BBBBB') > 0):
      newState._gameOver = True
      newState._winner = player
    elif newState._positions[0] | newState._positions[1] == Pente.fullBoard: 
      newState._gameOver = True
      newState._winner = -1
      
    return newState
      
  def patternCount(self, pattern):
    patterns = set([pattern, pattern[::-1]])
    count = 0
    
    for pattern in patterns:
      for direction in [ (0,1), (1,0), (1,1), (1,-1) ]:
        shiftAmount = 12 * direction[0] + direction[1];
          
        if pattern[0] == 'W':
          current = self._positions[0]
        elif pattern[0] == 'w':
          current = Pente.fullBoard ^ self._positions[0]
        elif pattern[0] == 'B':
          current = self._positions[1]
        elif pattern[0] == 'b':
          current = Pente.fullBoard ^ self._positions[1]
        elif pattern[0] == ' ':
          current = Pente.fullBoard ^ (self._positions[0] | self._positions[1])
        else:
          current = Pente.fullBoard
          
        for c in pattern[1:]:
          current <<= shiftAmount
          current &= Pente.fullBoard
           
          if c == 'W':
            current &= self._positions[0]
          elif c == 'w':
            current &= Pente.fullBoard ^ self._positions[0]
          elif c == 'B':
            current &= self._positions[1]
          elif c == 'b':
            current &= Pente.fullBoard ^ self._positions[1]
          elif c == ' ':
            current &= Pente.fullBoard ^ (self._positions[0] | self._positions[1])

        count += f'{current:b}'.count('1')
        
    return count
    
  def patternLocations(self, pattern):
    patterns = set([pattern, pattern[::-1]])
    locations = []
    
    for pattern in patterns:
      for direction in [ (0,1), (1,0), (1,1), (1,-1) ]:
        shiftAmount = 12 * direction[0] + direction[1]
        offset = 0
          
        if pattern[0] == 'W':
          current = self._positions[0]
        elif pattern[0] == 'w':
          current = Pente.fullBoard ^ self._positions[0]
        elif pattern[0] == 'B':
          current = self._positions[1]
        elif pattern[0] == 'b':
          current = Pente.fullBoard ^ self._positions[1]
        elif pattern[0] == ' ' or pattern[0] == '_':
          current = Pente.fullBoard ^ (self._positions[0] | self._positions[1])
        else:
          current = Pente.fullBoard
          
        for c in pattern[1:]:
          current <<= shiftAmount
          current &= Pente.fullBoard
          offset += 1
           
          if c == 'W':
            current &= self._positions[0]
          elif c == 'w':
            current &= Pente.fullBoard ^ self._positions[0]
          elif c == 'B':
            current &= self._positions[1]
          elif c == 'b':
            current &= Pente.fullBoard ^ self._positions[1]
          elif c == ' ':
            current &= Pente.fullBoard ^ (self._positions[0] | self._positions[1])
          elif c == '_':
            offset = 0
            current &= Pente.fullBoard ^ (self._positions[0] | self._positions[1])

        for row in range(11):
          for col in range(11):
            if (1 << (12*row+col)) & current:
              locations.append( (row - offset*direction[0], col - offset*direction[1]) )
              
    return locations
    
  def numCaptures(self, action):
    if self.getPosition(action) != -1:
      return 0
      
    player = self._turn % 2
    count = 0
    for direction in [ (1,0), (-1,0), (0,1), (0,1), (1,1), (1,-1), (-1,1), (-1,-1) ]:
      if 0 <= action[0] + 3*direction[0] < 11:
        if 0 <= action[1] + 3*direction[1] < 11:
          if self.getPosition((action[0]+direction[0], action[1]+direction[1])) == 1 - player:
            if self.getPosition((action[0]+2*direction[0], action[1]+2*direction[1])) == 1 - player:
              if self.getPosition((action[0]+3*direction[0], action[1]+3*direction[1])) == player:
                count += 1
             
    return count
    
  def neighborhood(self, radius):
    current = self._positions[0] | self._positions[1]
    for d in range(radius):
      current = (current | (current >> 1)) & Pente.fullBoard
      current = (current | (current << 1)) & Pente.fullBoard
      current = (current | (current >> 12)) & Pente.fullBoard
      current = (current | (current << 12)) & Pente.fullBoard
      
    free = current ^ (self._positions[0] | self._positions[1])
    
    options = []
    for row in range(11):
      for col in range(11):
        if (1 << (12*row+col)) & free:
          options.append( (row,col) )
          
    random.shuffle(options)
    return options    
      
  def __str__(self):
    s = f'Turn: {self._turn}\n'
    s += f'White: {self._captures[0]} Black: {self._captures[1]}\n\n'
    s += '  '
    for i in range(11):
      s += chr(ord('A')+i)
    s += '\n'
    s += ' +' + '-'*11 + '+\n'
    for row in range(11):
      s += chr(ord('A') + row)
      s += '|'
      for col in range(11):
        p = self.getPosition((row,col))
        if p == 0:
          s += 'W'
        elif p == 1:
          s += 'B'
        else:
          s += ' '
      s += '|' + chr(ord('A') + row) + '\n'
    s += ' +' + '-'*11 + '+\n'
    s += '  '
    for i in range(11):
      s += chr(ord('A')+i)
    s += '\n'
    return s
    
  def moveToStr(self, action):
    return chr(ord('A') + action[0]) + chr(ord('A') + action[1])
    
  def winningMoves(self):
    options = []
    
    if self._turn % 2 == 0:
      options.extend(self.patternLocations('WWWW_'))
      options.extend(self.patternLocations('WWW_W'))
      options.extend(self.patternLocations('WW_WW'))
      
      for loc in self.patternLocations('WBB_'):
        if self._captures[0] + self.numCaptures(loc) >= 5:
          options.append(loc)      
    else:
      options.extend(self.patternLocations('BBBB_'))
      options.extend(self.patternLocations('BBB_B'))
      options.extend(self.patternLocations('BB_BB'))
      
      for loc in self.patternLocations('BWW_'):
        if self._captures[1] + self.numCaptures(loc) >= 5:
          options.append(loc)

    return options
    
  def blockingMoves(self):
    nullState = copy.deepcopy(self)
    nullState._turn += 1
    
    options = nullState.winningMoves()

    blocking = []
    for a in options:
      r = self.result(a)
      if len(r.winningMoves()) == 0:
        blocking.append(a)
        
    return blocking
    
class Player:
  def __init__(self, timeLimit):
    self._timeLimit = timeLimit
    self._startTime = 0
    self._move = None
    
  def timeRemaining(self):
    if time.time() < self._startTime + self._timeLimit:
      return True
    return False

  def setMove(self, move):
    if self.timeRemaining():
      self._move = move
    
  def getMove(self):
    return self._move

