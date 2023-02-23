from Pente import *

import sys
import time

player1name = input('Enter the class name for the first player (e.g. MyPlayer): ')
player2name = input('Enter the class name for the second player (e.g. MyPlayer): ')
timeLimit = int(input('Enter the time limit for each turn: '))

exec(f'from {player1name} import *')
if player1name != 'HumanPlayer':
  exec(f'player1 = {player1name}({timeLimit})')
else:
  exec(f'player1 = {player1name}({1e6})')

exec(f'from {player2name} import *')
if player2name != 'HumanPlayer':
  exec(f'player2 = {player2name}({timeLimit})')
else:
  exec(f'player2 = {player2name}({1e6})')

size = int(input('Enter the width of the graphics window (0 for text mode): '))
if size > 0:
  from Graphics import *
  g = Graphics(size)
else:
  g = None


state = Pente()

moveSequence = []

while not state.gameOver():
  print(state)
  
  if state.getTurn() % 2 == 0:
    player1._startTime = time.time()
    player1.findMove(state)
    move = player1.getMove()
    print(f'White moves {state.moveToStr(move)}\n')
  else:
    player2._startTime = time.time()
    player2.findMove(state)
    move = player2.getMove()
    print(f'Black moves {state.moveToStr(move)}\n')
  state = state.result(move)
  moveSequence.append(move)


  if g is not None:
    g.draw(state)

print(state)
if state.winner() == 0:
  print('White wins!')
elif state.winner() == 1:
  print('Black wins!')
else:
  print("It's a draw")
  
print('Move sequence:', ' '.join([state.moveToStr(m) for m in moveSequence]))
