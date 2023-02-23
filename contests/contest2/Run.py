from DrawGhostBusters import *
from Maze import *
from Ghost import *
from Agent import *

import argparse

parser = argparse.ArgumentParser(description='Catch all of the ghosts.')
parser.add_argument('--graphics', '-g', type=int, help='Display the solution using graphics with specified window size (optional)')
args = parser.parse_args()


maze = Maze()
if args.graphics:
  graphics = DrawGhostBusters(maze, args.graphics//maze.getSize())
else:
  graphics = None


pacman = maze.getStart()
ghosts = [Ghost(maze).getLocation() for _ in range(3)]
caught = [False, False, False]
agent = Agent(maze)

score = 0
numCaught = 0
turn = 0
while numCaught<3 and turn < 50:
  turn += 1
  print()
  print('Turn', turn)
  distances = [ maze.noisyDistance(pacman, g) for g in ghosts ]
  if graphics: graphics.render(pacman, agent.getProbs(), distances, ghosts)
  
  agent.applyDistances(distances, pacman)
  agent.play(pacman)
  move = agent.getMove()

  if len(move) > 0 and move in 'NESW' and maze.safeDirections(pacman)[move]:
    pacman = maze.adjacent(pacman, move)
    
  caught = [ pacman == g for g in ghosts ]
  for i in range(3):
    if caught[i]:
      numCaught += 1
      ghosts[i] = maze.jailLocation(i)
  
  agent.pacmanMoved(pacman, caught)
  if graphics: graphics.render(pacman, agent.getProbs(), [], ghosts)
  
  score = 100*numCaught - turn
  print('Score =', score)
