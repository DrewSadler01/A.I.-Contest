from Pente import *

import time

moveSequence = input('Enter the move sequence: ')
delay = int(input('Enter the time delay (0 to wait for user input): '))
size = int(input('Enter the width of the graphics window (0 for text mode): '))
if size > 0:
  from Graphics import *
  g = Graphics(size)
else:
  g = None

state = Pente()
print(state)
if delay > 0:
  time.sleep(delay)
else:
  input('Hit enter to continue')
  
for m in moveSequence.strip().split():
  a = ( ord(m[0]) - ord('A'), ord(m[1]) - ord('A') )
  state = state.result(a)
  
  if state.getTurn() % 2 == 0:
    print(f'White moves {m}')
  else:
    print(f'Black moves {m}')
    
  print()
  print(state)
  
  if g is not None:
    g.draw(state)
  
  if delay > 0:
    time.sleep(delay)
  else:
    input('Hit enter to continue')

if state.winner() == 0:
  print('White wins!')
elif state.winner() == 1:
  print('Black wins!')
else:
  print("It's a draw")
