from testing_board_indexing import generate_board
from .board_indexing import BoardIndexing

class Board:
    def __init__(self):
        board_indexes = BoardIndexing()
        self.cell_indexes = board_indexes.get_cell_indexes()
        self.peer_indexes = board_indexes.get_peer_indexes()

        self._digits = set('123456789')

        # board represented as a string
        self._string_board = ''

        # initial group board
        self._group_board = dict((cell, self._digits) for cell in self.cell_indexes)

        # initial display board
        self._board = {}
        
        
    def set_board(self, board):
        # parse given board and assign group board accordingly
        parsed_board = self._parse_board(board)
        if board and len(board) == 81:
            self._string_board = ''.join(parsed_board)
            self._board = dict(zip(self.cell_indexes, parsed_board))
            self._create_group_board()
        else:
            # board could not be parsed
            return False
        
    
    def _parse_board(self, board):
        if type(board) == str:
            # handle board input as string (e.g. '10020300000400000900020020000003')
            return [cell if cell in self._digits else '0' for cell in board]
        elif type(board) == list:
            # handle board input as 2D array (e.g [[1 ... 9] * 9])
            return [cell if cell in self._digits else '0' for row in board for cell in row]
        elif type(board) == dict:
            # handle board input as dictionary
            return [cell if cell in self._digits else '0' for cell in board.values()]
        else:
            # could not parse board
            return False
    

    def _create_group_board(self):
        for cell_index in self._board:
            cell = self._board[cell_index]
            if cell != '0':
                # get peers
                peers = self.peer_indexes[cell_index]
                for peer in peers:
                    # go to group board
                    self._group_board[peer] = self._group_board[peer] - set(cell)
                    # print(self._group_board[peer])
                
                self._group_board[cell_index] = set(self._board[cell_index])


    def get_board(self):
        return self._board

    def get_group_board(self):
        return self._group_board

    def get_board_string(self):
        return self._string_board

    def get_board_2D(self):
        # convert 1D string array into 2D 9x9 array
        return [[self._string_board[col + (9 * row)] for col in range(9)] for row in range(9)]
    
    def new_board(self):
        self._group_board = dict((cell, self._digits) for cell in self.cell_indexes)
        self.set_board(generate_board())
        pass