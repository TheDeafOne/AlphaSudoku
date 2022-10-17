import random

class BoardGenerator:
    '''
        Manages dataset gets and difficulty bins

        ATTRIBUTES
        _dataset_size: number of rows in the current data set
        _row_char_count: number of characters in each row of the dataset
        _bins: dictionary of board locations in dataset. key: No. clues, value: location in dataset
    '''
    def __init__(self):
        self._dataset_size = 413422 # number of rows in the dataset
        self._row_char_count = 165 # number of characters in a given row

        # key: number of clues, value: number of boards in dataset
        self._bins = {
            30: 208498, 
            29: 118817, 
            28: 56760, 
            27: 21546, 
            26: 6304, 
            25: 1297, 
            24: 182, 
            23: 18, 
            22: 0  # end value for bin edges
            }
    

    '''
        Grabs random sudoku board according to given difficulty range

        PARAMS
        difficulty_begin: clue number to begin random board search at (default: 23)
        difficulty_end: clue number to end random board search at (default: 30)

        RETURNS
        random sudoku board containing n clues, where n is in the given range
    '''
    def generate_board(self, difficulty_begin=23, difficulty_end=30):
        # check for invalid clue ranges
        assert difficulty_begin <= difficulty_end
        assert difficulty_begin > 22
        assert difficulty_end < 31

        end = self._dataset_size - self._bins[difficulty_begin-1]
        begin = self._dataset_size - self._bins[difficulty_end]
        
        offset = random.randrange(begin, end)

        dataset = open('../data/initial_boards/sudoku_dataset.csv')
        
        # jump to random line and return it
        dataset.seek(offset*self._row_char_count)
        dataset.readline()
        return dataset.readline().split(',')