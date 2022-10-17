from .board_generator import BoardGenerator
import json

class Board:
    '''
        A class used to manage and represent sudoku boards

        ATTRIBUTES
        cell_indexes: all indexes of a sudoku board in Letter,Number format (A1 ... I9)
        peer_indexes: all peers of a given cell
        _digits: possible sudoku cell values
        _string_board: current board state as a string
        _group_board: current group board state as a dictionary (key: cell index, value: set of possible values)
        _board: current board state as a dictionary (key: cell, value: given value or 0)
        
        METHODS
        set_board(board)
            sets board state and updates group board
        
        _parse_board(board)
            ingests given board and outputs clean board array
        
        _update_group_board():
            updates group board according to the current _board state
    '''
    def __init__(self):
        with open("../data/board_indexes/cells.txt") as cells, open("../data/board_indexes/peers.txt") as peers:
            self.cell_indexes = json.load(cells)["cells"]
            self.peer_indexes = json.load(peers)
        

        self._digits = set('123456789')

        # board represented as a string
        self._string_board = ''

        # initial group board
        self._group_board = dict((cell, self._digits) for cell in self.cell_indexes)

        # initial display board
        self._board = {}
        

    '''
        Sets board dictionary to values found in given board, and assigns groups according to new board state

        PARAMS
        board: sudoku board in any common representation

        RETURNS
        True if the given board could be parsed, False otherwise
    '''  
    def set_board(self, board):
        # parse given board and assign group board accordingly
        parsed_board = self._parse_board(board)
        if board and len(board) == 81:
            self._string_board = ''.join(parsed_board)
            self._board = dict(zip(self.cell_indexes, parsed_board))
            self._update_group_board()
            return True
        else:
            # board could not be parsed
            return False
        
    
    '''
        creates a 1D array representation of a board for common types of boards 
        (string, 1D array, 2D array, and dictionary)

        PARAMS
        board: sudoku board in any common representation
    '''
    def _parse_board(self, board):
        if type(board) == str:
            # handle board input as string (e.g. '10020300000400000900020020000003')
            return [cell if cell in self._digits else '0' for cell in board]
        elif type(board) == list:
            if len(board) == 9:
                # handle board input as 2D array (e.g [[1 ... 9] * 9])
                return [cell if cell in self._digits else '0' for row in board for cell in row]
            else:
                # handle board input as 1D array
                return board
        elif type(board) == dict:
            # handle board input as dictionary
            return [cell if cell in self._digits else '0' for cell in board.values()]
        else:
            # could not parse board
            return False


    '''
        Creates group board from current board state
    '''
    def _update_group_board(self):
        # cycle through all possible cell indexes
        for cell_index in self.cell_indexes:
            cell = self._board[cell_index]
            if cell != '0':
                # cycle through peers and manage group board accordingly
                peers = self.peer_indexes[cell_index]
                for peer in peers:
                    # go to group board and remove cell peer values from group board
                    self._group_board[peer] = self._group_board[peer] - set(cell)
                
                # remove cell value from group board
                self._group_board[cell_index] = set(self._board[cell_index])


    '''
        Get functions for board types and group board
    '''
    def get_board(self):
        return self._board

    def get_group_board(self):
        return self._group_board

    def get_board_string(self):
        return self._string_board

    def get_board_2D(self):
        return [[self._string_board[col + (9 * row)] for col in range(9)] for row in range(9)]
    
    def new_board(self):
        self._group_board = dict((cell, self._digits) for cell in self.cell_indexes)
        self.set_board(BoardGenerator.generate_board())