from .board_generator import BoardGenerator
import json

class Board:
    '''
        A class used to manage and represent sudoku boards

        ATTRIBUTES
        _cell_indexes: all indexes of a sudoku board in Letter,Number format (A1 ... I9)
        _peer_indexes: all peers of a given cell
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

        _update_subgrid_values()
            updates subgrid values according to set board values

        new_board(difficulty_begin, difficulty_end)
            generates a new board and updates board
    '''
    def __init__(self):
        with (
            open("../data/board_indexes/cells.txt") as cells, 
            open("../data/board_indexes/peers.txt") as peers,
            open("../data/board_indexes/subgrids.txt") as subgrids
        ):
            self._cell_indexes = json.load(cells)["cells"]
            self._subgrid_indexes = json.load(subgrids)["subgrids"]
            self._peer_indexes = json.load(peers)
        

        self._digits = set('123456789')

        # track length of max group for display purposes
        self._max_group_length = 0

        # list of subgrid values
        self._subgrids = []

        self._groups = {}
        # board represented as a string
        self._string_board = ''

        # board represented as a 2D array
        self._board_2D = []

        # group board represented as a 2D array (each group is in a list, so technically a 3D array)
        self._group_board_2D = []

        self._group_board_2D_map = {}

        # initial group board
        self._group_board = dict((cell, self._digits) for cell in self._cell_indexes)

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
        if parsed_board:
            self._string_board = ''.join(parsed_board)
            self._board_2D = [[self._string_board[col + (9 * row)] for col in range(9)] for row in range(9)]
            self._board = dict(zip(self._cell_indexes, parsed_board))
            self._update_group_board()
            self._update_subgrid_values()
            return True
        else:
            # board could not be parsed
            return False
        
    
    '''
        creates a 1D array representation of a board for common types of boards 
        (string, 1D array, 2D array, and dictionary)

        PARAMS
        board: sudoku board in any common representation

        RETURNS
        array of board values if board could be parsed, False otherwise
    '''
    def _parse_board(self, board):
        if type(board) == str:
            # handle board input as string (e.g. '10020300000400000900020020000003')
            return [cell if cell in self._digits else '0' for cell in board]
        elif type(board) == list:
            if len(board) == 9:
                # handle board input as 2D array (e.g [[1 ... 9] * 9])
                return [cell if cell in self._digits else '0' for row in board for cell in row]
            elif len(board) == 81:
                # handle board input as 1D array
                return board
            elif len(board) == 2:
                return [cell if cell in self._digits else '0' for cell in board[0]]
        elif type(board) == dict:
            # handle board input as dictionary
            return [cell if cell in self._digits else '0' for cell in board.values()]
        elif type(board) == Board:
            return list(board.get_board().values())
        else:
            # could not parse board
            return False


    '''
        Creates group board from current board state
    '''
    def _update_group_board(self):
        # cycle through all possible cell indexes
        for cell_index in self._cell_indexes:
            cell = self._board[cell_index]
            if cell != '0':
                # cycle through peers and manage group board accordingly
                peers = self._peer_indexes[cell_index]
                for peer in peers:
                    # go to group board and remove cell peer values from group board
                    group = self._group_board[peer] - set(cell)
                    self._max_group_length = max(len(group), self._max_group_length)
                    self._group_board[peer] = group
                
                # remove cell value from group board
                self._group_board[cell_index] = set(self._board[cell_index])
        # make 2D group board
        self._create_group_board_2D()

        # get groups
        self._set_groups()

    def set_group_board(self, group_board):
        self._group_board = group_board
        self._set_groups()
    
    def _set_groups(self):
        for cell_index in self._group_board:
            if len(self._group_board[cell_index]) > 1:
                self._groups[cell_index] = self._group_board[cell_index]
    '''
        updates subgrid values according to board
    '''
    def _update_subgrid_values(self):
        self._subgrids = [[self._board[index] for index in row] for row in self._subgrid_indexes]

    '''
        Creates 2D array representation of group board
    '''
    def _create_group_board_2D(self):
        group_board_2D = [[]]
        for i, cell_index in enumerate(self._group_board):
            group_board_2D[-1].append(list(self._group_board[cell_index]))
            # map cell_index to i,j index pair
            self._group_board_2D_map[cell_index] = (len(group_board_2D) - 1, i % 9)
            if (i + 1) % 9 == 0 and i != 80:
                group_board_2D.append([])

        self._group_board_2D = group_board_2D           


    '''
        calls board generator and replaces board with generated board
    '''
    def new_board(self, difficulty_begin=23, difficulty_end=30):
        self._group_board = dict((cell, self._digits) for cell in self._cell_indexes)
        self.set_board(BoardGenerator().generate_board(difficulty_begin, difficulty_end))

    '''
        Get functions for board types and group board
    '''
    def get_board(self):
        return self._board

    def get_group_board(self):
        return self._group_board
    
    def get_group_board_2D(self):
        return self._group_board_2D

    def get_board_string(self):
        return self._string_board

    def get_board_2D(self):
        return self._board_2D
    
    def get_group_board_2D_map(self):
        return self._group_board_2D_map
    
    def get_subgrids(self):
        return self._subgrids

    def get_cell_indexes(self):
        return self._cell_indexes
    
    def get_peer_indexes(self):
        return self._peer_indexes
    
    def get_subgrid_indexes(self):
        return self._subgrid_indexes

    def set_board_value(self, index, value):
        self._board[index] = value
        self._set_board(self._board)


    '''
        display functions
    '''
    def display_board(self, width="medium"):
        space = ""
        partition_multiplier = 0
        if width == "small":
            partition_multiplier = 11
        elif width == "medium":
            partition_multiplier = 23
            space = " "
        elif width == "large":
            partition_multiplier = 35
            space = "  "

        for i, row in enumerate(self._board_2D):
            for j, cell in enumerate(row):
                col_mod = j % 3
                if col_mod == 0 and j != 0:
                    print(space + "|" + space, end="")
                    print(cell, end="")
                else:
                    print(space + cell, end="")
            print()
            if (i + 1) % 3 == 0 and i != 8:
                print("-" * partition_multiplier)
    

    def display_group_board(self):
        for i, row in enumerate(self._group_board_2D):
            for j, val in enumerate(row):
                print("".join(val).ljust(self._max_group_length + 1, " "), end="")
                if (j + 1) % 3 == 0 and j != 8:
                    print("|   ", end="")
            if (i + 1) % 3 == 0 and i != 8:
                print()
                print("-" * (self._max_group_length * 11), end="")
            print()
