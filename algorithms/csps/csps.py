'''
    A constraint satisfaction problem solver
'''
from time import sleep
from .ac3 import AC3

class CSPS:
    '''
        backtracking algorithm for sudoku
    '''
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
        
        for value in group_board[sm_group_index]:
            solution = self.search(self.remove_value(group_board.copy(), sm_group_index, value))
            if solution:
                return solution
        return False


    '''
        removes value from group at cell index and propagates according to remaining group values

        PARAMS
        group_board: current board state in backtracking stack
        cell_index: index of cell being set (e.g. A1)
        value: value being value being removed
    '''
    def remove_value(self, group_board, cell_index, value):
        # remove value from group and get remaining values
        group = group_board[cell_index].replace(value, '')

        # check that all possible next values are valid solutions
        for group_value in group:
            if not self.propagate(group_board, cell_index, group_value):
                return False
        return group_board
    

    '''
        runs ac3 on current board with new set value

        PARAMS
        group_board: current board state in backtracking stack
        cell_index: index of cell being set (e.g. A1)
        value: value being propagated on
        
        (group_board[A1] = 123 and value = 1, new group_board[A1] = 23, then run propagation on that)

        RETURNS
        propagated_board: if ac3 was successful, False otherwise
    '''
    def propagate(self, group_board, cell_index, value):
        # remove value from group at cell_index and set group board at cell index to new group
        group_board[cell_index] = group_board[cell_index].replace(value,'')

        # set up ac3 propagation and run on new group_board
        ac3 = AC3(group_board)
        propagated_board = ac3.ac3()

        if propagated_board:
            return propagated_board
        return False # ac3 found an inconsistency