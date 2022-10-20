'''
    A constraint satisfaction problem solver
'''
from time import sleep
from .ac3 import AC3
from board_logic.board import Board
from copy import deepcopy

class CSPS:
    def __init__(self, board):
        self._board = board.get_group_board()
        self.peer_indexes = board.peer_indexes
        self.unit_indexes = board.unit_indexes
        self.cell_indexes = board.cell_indexes
        self._constraints = [(index, peer) for index in self.peer_indexes for peer in self.peer_indexes[index]]
        # self._ac3 = AC3({},self._constraints)
        # self._good_board = Board()
        self.solved_board = {}
    

    def solve(self): 
        if len(self.solved_board) == 0:
            self.solved_board = self.search(self._board)
        return self.solved_board


    def search(self, values):
        if values is False:
            return False ## Failed earlier

        if all(len(values[s]) == 1 for s in self.cell_indexes):
            return values ## Solved!

        ## Chose the unfilled square s with the fewest possibilities
        _,s = min((len(values[s]), s) for s in self.cell_indexes if len(values[s]) > 1)
        return self.some(self.search(self.assign(values.copy(), s, d))
                    for d in values[s])

    def assign(self, values, s, d):
        other_values = values[s].replace(d, '')
        if all(self.eliminate(values, s, d2) for d2 in other_values):
            return values
        else:
            return False


    def eliminate(self, values, s, d):
        if d not in values[s]:
            return values ## Already eliminated
        values[s] = values[s].replace(d,'')
        ## (1) If a square s is reduced to one value d2, then eliminate d2 from the peers.
        if len(values[s]) == 0:
            return False ## Contradiction: removed last value
        elif len(values[s]) == 1:
            d2 = values[s]
            if not all(self.eliminate(values, s2, d2) for s2 in self.peer_indexes[s]):
                return False
        ## (2) If a unit u is reduced to only one place for a value d, then put it there.
        for u in self.unit_indexes[s]:
            dplaces = [s for s in u if d in values[s]]
            if len(dplaces) == 0:
                return False ## Contradiction: no place for this value
            elif len(dplaces) == 1:
                # d can only be in one place in unit; assign it there
                if not self.assign(values, dplaces[0], d):
                    return False
        return values
    
    def some(self, seq):
        for e in seq:
            if e: 
                return e
        return False

        
        
        