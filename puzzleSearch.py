# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

from time import perf_counter
import heapq

class PriorityQueue:
    def  __init__(self):
        self.heap = []
        # avoid crash when the items are comparable
        self.index = 0

    def push(self, item, priority):
        heapq.heappush(self.heap, (priority, self.index, item))
        self.index += 1

    def pop(self):
        return heapq.heappop(self.heap)[-1]

    def isEmpty(self):
        return len(self.heap) == 0

def breadthFirstSearch(problem):
    """
    Find solution to the problem using BFS.
    """
    closed = set()
    result = []
    q = []
    q.insert(0, (problem.getStartState(), []))
    while len(q) > 0:
        (state, path) = q.pop()
        if problem.isGoalState(state):
            return path
        if state not in closed:
            closed.add(state)
            for successor in problem.getSuccessors(state):
                newPath = path + [successor[1]]
                q.insert(0, (successor[0], newPath))
    return result

def nullHeuristic(state, problem=None):
    """
    Null heuristic which returns 0 all the time.
    Same as Uniform Cost Search.
    """
    return 0

def misplacementHeuristic(state, problem):
    '''
    Heursitic based on the number of misplaced cells.
    '''
    return state.numOfMisplacedCells()

def manhattanDistanceHeuristic(state, problem):
    '''
    Heuristic based on manhattan distance between each cell and its goal position.
    '''
    return state.manhattanDistanceToGoal()

def aStarSearch(problem, heuristic=nullHeuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    closed = set()
    result = []
    pq = PriorityQueue()
    pq.push((problem.getStartState(), [], 0), 0)
    while not pq.isEmpty():
        (state, path, cost) = pq.pop()
        if problem.isGoalState(state):
            return path
        if state not in closed:
            closed.add(state)
            for successor in problem.getSuccessors(state):
                newPath = path + [successor[1]]
                newCost = cost + successor[2]
                pq.push((successor[0], newPath, newCost), newCost + heuristic(successor[0], problem))
    return result

def BFS(problem):
    '''
    Find a solution to the problem using Breadth First Search.
    '''
    start = perf_counter()
    bfs = breadthFirstSearch(problem)
    end = perf_counter()
    print('Breadth First Search spent', str(end - start), 'seconds finding solution:')
    print(bfs)
    print('Solution contains', str(len(bfs)), 'actions.\n')
    return bfs

def UCS(problem):
    '''
    Find a solution to the problem using Uniform Cost Search.
    '''
    start = perf_counter()
    ucs = aStarSearch(problem)
    end = perf_counter()
    print('Uniform Cost Search spent', str(end - start), 'seconds finding solution:')
    print(ucs)
    print('Solution contains', str(len(ucs)), 'actions.\n')
    return ucs

def astarMisplaced(problem):
    '''
    Find a solution to the problem using A* with Heuristic based on the number of 
    misplaced cells.
    '''
    start = perf_counter()
    astarMisp = aStarSearch(problem, misplacementHeuristic)
    end = perf_counter()
    print('A* with Heuristic based on the number of misplaced cells spent', \
        str(end - start), 'seconds finding solution:')
    print(astarMisp)
    print('Solution contains', str(len(astarMisp)), 'actions.\n')
    return astarMisp

def astarManhattan(problem):
    '''
    Find a solution to the problem using A* with Heuristic based on manhattan 
    distance between each cell and its goal position.'
    '''
    start = perf_counter()
    astarMan = aStarSearch(problem, manhattanDistanceHeuristic)
    end = perf_counter()
    print('A* with Heuristic based on manhattan distance between' \
         ,'each cell and its goal position spent', str(end - start), 'seconds finding solution:')
    print(astarMan)
    print('Solution contains', str(len(astarMan)), 'actions.\n')
    return astarMan