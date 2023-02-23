from heapq import *

class PriorityQueue:
  def __init__(self):
    self._queue = []
    
  def push(self, priority, item):
    heappush(self._queue, (priority, item)) 

  def pop(self):
    result = heappop(self._queue)
    return result[0], result[1]
    
  def __len__(self):
    return len(self._queue)
    
