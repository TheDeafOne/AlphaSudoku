import random

class BoardGenerator:
    '''
        Manages dataset gets and difficulty bins

        ATTRIBUTES
        _dataset_size: number of rows in the current data set
        _row_char_count: number of characters in each row of the dataset
    '''
    def __init__(self):
        self._dataset_size = 4000000 # number of rows in the dataset
        self._row_char_count = 81 # number of characters in a given row
    

    '''
        Grabs random sudoku board according to given difficulty range

        PARAMS
        difficulty_begin: clue number to begin random board search at (default: 23)
        difficulty_end: clue number to end random board search at (default: 30)

        RETURNS
        random sudoku board containing n clues, where n is in the given range
    '''
    def generate_board(self, difficulty_begin=17, difficulty_end=80):
        # check for invalid clue ranges
        assert difficulty_begin <= difficulty_end
        assert difficulty_begin > 16
        assert difficulty_end < 81

        begin = (80 - difficulty_end) * 62500 + 1
        end = (81 - difficulty_begin) * 62500

        offset = random.randrange(begin, end)
        fileNo = str((offset // 1000000) + 1)
        fileOffset = offset % 1000000
        dataset = open('../data/initial_boards/sudoku_dataset_' + fileNo + '.csv')

        # # jump to random line and return it
        dataset.seek(83 * (fileOffset-1))
        return dataset.readline().strip()
