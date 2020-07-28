from random import sample
from math import sqrt
from copy import deepcopy
from time import sleep
from puzzleSearch import *

class PuzzleState:
    def __init__(self, nums):
        '''
        Build a puzzle based on the list nums, where 0 represents
        the blank.
        '''
        self.cells = [] # 2D list
        i = 0
        numCol = int(sqrt(len(nums)))
        while i < len(nums):
            row = []
            for col in range(numCol):
                if nums[i] == 0:
                    self.blank = (i // numCol, i % numCol)
                row.append(nums[i])
                i += 1
            self.cells.append(row)

    def isGoal(self):
        '''
        Check if current state is the goal state.
        '''
        i = 0
        for row in range(len(self.cells)):
            for col in range(len(self.cells[row])):
                if i != self.cells[row][col]: return False
                i += 1
        return True

    def legalActions(self):
        '''
        Return a list of legal actions based on current state.
        Actions are represented as "up", "down", "left", "right"
        '''
        actions = []
        row, col = self.blank
        if row != 0: actions.append('down')
        if row != 2: actions.append('up')
        if col != 0: actions.append('right')
        if col != 2: actions.append('left')
        return actions

    def resultOfAction(self, action):
        '''
        Return a new puzzle achieved by taking the action on the
        current state.
        '''
        row, col = self.blank
        newRow, newCol = row, col
        if action == 'up': newRow += 1
        elif action == 'down': newRow -= 1
        elif action == 'left': newCol += 1
        elif action == 'right': newCol -= 1
        newPuzzle = PuzzleState([])
        newPuzzle.cells = deepcopy(self.cells)
        newPuzzle.blank = (newRow, newCol)
        newPuzzle.cells[row][col], newPuzzle.cells[newRow][newCol] = \
            newPuzzle.cells[newRow][newCol], newPuzzle.cells[row][col]
        return newPuzzle

    def numOfMisplacedCells(self):
        '''
        Return the number of cells that are misplaced.
        '''
        i = num = 0
        for row in range(len(self.cells)):
            for col in range(len(self.cells[row])):
                if i != 0 and i != self.cells[row][col]: num += 1
                i += 1
        return num

    def manhattanDistanceToGoal(self):
        '''
        Return the sum of total manhatanDistance between all cells and
        their goal position.
        '''
        current = {}
        i = dis = 0
        for row in range(len(self.cells)):
            for col in range(len(self.cells[row])):
                current[self.cells[row][col]] = (row, col)
        for num, (row, col) in current.items():
            goalRow = num // len(self.cells)
            goalCol = num - goalRow * len(self.cells)
            dis += abs(row - goalRow) + abs(col - goalCol)
        return dis

    def __str__(self):
        '''
        Define the string representation of the state.
        '''
        lines = []
        horizontalLine = ('-' * (len(self.cells) * 5))
        lines.append(horizontalLine)
        for row in self.cells:
            rowLine = '|'
            for col in row:
                if col == 0:
                    col = '  '
                elif col < 10:
                    col = ' ' + col.__str__()
                else:
                    col = col.__str__()
                rowLine = rowLine + ' ' + col.__str__() + ' |'
            lines.append(rowLine)
            lines.append(horizontalLine)
        return '\n'.join(lines)

    # make class instance hashable since search will check membership of state
    def __eq__(self, other):
        for row in range(len(self.cells)):
            if self.cells[row] != other.cells[row]: return False
        return True

    def __hash__(self):
        return hash(str(self.cells))

class puzzleProblem:
    def __init__(self, puzzle):
        self.prob = puzzle

    def getStartState(self):
        '''
        Return the starting state of the problem.
        '''
        return self.prob

    def isGoalState(self, state):
        '''
        Check if the current state is the goal state.
        '''
        return state.isGoal()

    def getSuccessors(self, state):
        '''
        Return a list of successors of current state.
        Representing as a list of 3-tuples (successor, action, cost).
        '''
        successors = []
        for action in state.legalActions():
            successors.append((state.resultOfAction(action), action, 1))
        return successors

def randomPuzzle(data, numOfActions):
    '''
    Perform number of random actions on current state.
    '''
    puzzle = PuzzleState(data)
    for i in range(numOfActions):
        puzzle = puzzle.resultOfAction(sample(puzzle.legalActions(), 1)[0])
    return puzzle

if __name__ == '__main__':
    size = 16 # other sizes alternatively
    nPuzzle = [i for i in range(size)]
    puzzle = randomPuzzle(nPuzzle, 100)
    print(puzzle)
    prob = puzzleProblem(puzzle)
    print('Initialization finished.\n')

    bfs = BFS(prob)
    #ucs = UCS(prob)
    astarMisp = astarMisplaced(prob)
    astarMan = astarManhattan(prob)

    input('Hit Enter to see the solving process...')

    for action in bfs:
        puzzle = puzzle.resultOfAction(action)
        print('After action:', action)
        print(puzzle)
        sleep(1)
        
