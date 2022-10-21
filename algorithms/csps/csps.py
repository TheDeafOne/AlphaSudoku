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
        self.solved_board = {}
    

    def solve(self): 
        if len(self.solved_board) == 0:
            self.solved_board = self.search(self._board)
        return self.solved_board


    def search(self, group_board):
        if group_board is False:
            return False

        if all(len(group_board[cell_index]) == 1 for cell_index in self.cell_indexes):
            return group_board

        _,sm_group_index = min((len(group_board[cell_index]), cell_index) for cell_index in self.cell_indexes if len(group_board[cell_index]) > 1)
        
        for d in group_board[sm_group_index]:
            solution = self.search(self.set_value(group_board.copy(), sm_group_index, d))
            if solution:
                return solution
        return False

    def set_value(self, group_board, cell_index, value):
        other_values = group_board[cell_index].replace(value, '')
        if all(self.propagate(group_board, cell_index, d2) for d2 in other_values):
            return group_board
        else:
            return False
        
    def propagate(self, group_board, cell_index, value):
        if value not in group_board[cell_index]:
            return group_board
        group_board[cell_index] = group_board[cell_index].replace(value,'')
        ac3 = AC3(group_board)
        solution = ac3.ac3()
        if solution:
            return solution
        return False