import argparse

parser = argparse.ArgumentParser(description='Solve a sliding tile puzzle.')
parser.add_argument('size', type=int, help='Work with a size by size puzzle, e.g size=3, 4 or 5')
parser.add_argument('time', type=int, help='Time limit for finding a solution')
parser.add_argument('--length', '-l', type=int, help='Number of random moves used to generate random puzzle (optional)')
parser.add_argument('--moves', '-m', type=str, help='Moves to generate a particular puzzle (optional)')
parser.add_argument('--graphics', '-g', type=int, help='Display the solution using graphics with specified window size (optional)')
args = parser.parse_args()

from MySolver import *
from SlidingTilePuzzle import *

p = SlidingTilePuzzle(args.size)
if args.moves:
  s = p.getGoal()
  for m in args.moves:
    s = p.result(s,m)
else:
  if args.length:
    s = p.randomState(args.length)
  else:
    s = p.randomState()
p.setInitial(s)
print('Solving puzzle:', s)

solver=MySolver(p, args.time)
moves = solver.solution()

# Check the solution
puzzle = solver.getPuzzle()
state = puzzle.getInitial()
for a in moves:
  state = puzzle.result(state, a)
if puzzle.isGoal(state):
  print('Solution is correct')
else:
  print('Solution is incorrect')

if args.graphics:
  from SlidingTileVisualizer import *
  v = SlidingTileVisualizer(args.size, s, p, args.graphics)
  v.animate(moves)
  
