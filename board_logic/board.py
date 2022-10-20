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
        with (
            open("../data/board_indexes/cells.txt") as cells, 
            open("../data/board_indexes/peers.txt") as peers,
            open("../data/board_indexes/units.txt") as units
            ):
            self.cell_indexes = json.load(cells)["cells"]
            self.peer_indexes = json.load(peers)
            self.unit_indexes = json.load(units)
        

        self._digits = '123456789'

        # track length of max group for display purposes
        self._max_group_length = 0

        # board represented as a string
        self._string_board = ''

        # board represented as a 2D array
        self._board_2D = []

        # group board represented as a 2D array (each group is in a list, so technically a 3D array)
        self._group_board_2D = []

        # initial group board
        self._group_board = dict((cell, self._digits) for cell in self.cell_indexes)

        # initial display board
        self._board = {}
        

    def set_board(self, board):
        # parse given board and assign group board accordingly
        parsed_board = self._parse_board(board)
        if parsed_board:
            # update string board, 2d board, dict board, group board, and subgrid values
            self._board = dict(zip(self.cell_indexes, parsed_board))
            self._set_string_board()
            self._set_board_2D()
            if not self._update_group_board():
                # value is causing empty sets at at least one point
                return False
            self._create_group_board_2D()

            return True
        else:
            # board could not be parsed
            return False

    def _set_string_board(self):
        self._string_board = ''.join(list(self._board.values()))


   
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
        else:
            # could not parse board
            return False




    def _set_board_2D(self):
            self._board_2D = [[self._string_board[col + (9 * row)] for col in range(9)] for row in range(9)]


    '''
        Creates group board from current board state
    '''
    def _update_group_board(self):
        # cycle through all possible cell indexes
        for i, cell_index in enumerate(self.cell_indexes):
            cell = self._board[cell_index]
            if cell != '0':
                # cycle through peers and manage group board accordingly
                peers = self.peer_indexes[cell_index]
                for peer in peers:
                    # go to group board and remove cell peer values from group board
                    group = self._group_board[peer].replace(cell,'')
                    self._max_group_length = max(len(group), self._max_group_length)
                    self._group_board[peer] = group
                
                # remove cell value from group board
                self._group_board[cell_index] = self._board[cell_index]

    
    '''
        Creates 2D array representation of group board
    '''
    def _create_group_board_2D(self):
        group_board_2D = [[]]
        for i, cell_index in enumerate(self._group_board):
            group_board_2D[-1].append(list(self._group_board[cell_index]))
            if (i + 1) % 9 == 0 and i != 80:
                group_board_2D.append([])

        self._group_board_2D = group_board_2D           


    '''
        Prints board of variable size
        PARAMS
        width: enum value (small, medium, large) setting the display board width
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
    

    '''
        Prints group board
    '''
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
    
    def new_board(self, difficulty_begin=23, difficulty_end=30):
        self._group_board = dict((cell, self._digits) for cell in self.cell_indexes)
        self.set_board(BoardGenerator().generate_board(difficulty_begin, difficulty_end))
