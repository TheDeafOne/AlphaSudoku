import random
import csv

class BoardGenerator:
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
        
    def generate_board(self, difficulty_begin=23, difficulty_end=30):
        assert difficulty_begin <= difficulty_end
        assert difficulty_begin > 22
        assert difficulty_end < 31

        end = self._dataset_size - self._bins[difficulty_begin-1]
        begin = self._dataset_size - self._bins[difficulty_end]
        
        offset = random.randrange(begin, end)

        dataset = open('./data/initial_boards/sudoku_dataset.csv')
        
        # jump to random line and return it
        dataset.seek(offset*self._row_char_count)
        dataset.readline()
        return dataset.readline().split(',')
    
    # Don't delete this, it's useful for parsing new datasets
    # def rewrite(self):
    #     file = open('./data/initial_boards/sudoku_dataset.csv','w', newline='')
    #     writer = csv.writer(file)
    #     f = open('./data/initial_boards/sudoku.csv')
    #     reader = csv.reader(f)
        
    #     vals = {}
    #     for line in reader:
    #         if len(line) > 0:
    #             cnt = line[0].count('0')
    #             if cnt in vals:
    #                 vals[cnt].append(line)
    #             else:
    #                 vals[cnt] = [line]

    #     for val in sorted(vals.keys()):
    #         for row in vals[val]:
    #             writer.writerow(row)

    # Do not delete,  it's useful for debugging/reading the file without crashing things
    # def read_sudoku_set(self):
    #     f = open('./data/initial_boards/sudoku_dataset.csv')
    #     reader = csv.reader(f)
    #     cnt = 0
    #     for row in reader:
    #         if cnt % 90000 == 0:
    #             print(len(''.join(row)))
    #             row = row[0]
    #             print(row, row.count('0'))
                
    #         cnt += 1
