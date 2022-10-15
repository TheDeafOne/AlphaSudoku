import random
import csv

class BoardGenerator:
    def __init__(self):
        self._dataset_size = 9000000 # number of rows in the dataset
        self._row_char_count = 165 # number of characters in a given row

        # TODO make more uniform difficulty bins
        self._bins = {
            # hard
            4: 8,
            5: 19,
            6: 44,
            7: 116,
            8: 219,
            9: 407,
            10:	689,
            11:	1145,
            12:	1787,
            13:	2831,
            14:	4221,
            15:	6143,
            16:	8762,
            17:	12346,
            # semi-hard
            18:	17171,
            19:	23729,
            20:	32134,
            21:	43262,
            22:	57638,
            23:	75965,
            24:	99382,
            25:	129128,
            # medium
            26:	167046,
            27:	215023,
            28:	274142,
            29:	347726,
            30:	438006,
            31:	548200,
            32:	681285,
            33:	842069,
            34:	1035163,
            35:	1263725,
            36:	1533344,
            37:	1848603,
            38:	2212785,
            39:	2628705,
            # easy
            40:	3099521,
            41:	3623097,
            42:	4196429,
            43:	4810686,
            44:	5452894,
            45:	6103704,
            46:	6738043,
            47:	7329120,
            48:	7847627,
            49:	8271822,
            50:	8586578,
            51:	8795076,
            52:	8913893,
            53:	8970653,
            54:	8992199,
            55:	8998503,
            56:	8999800,
            57:	8999982,
            58:	9000000
        }

    def generate_board(self, difficulty_begin, difficulty_end):
        # get offset
        begin = self._dataset_size - self._bins[difficulty_end]
        end = self._dataset_size - self._bins[difficulty_begin]
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
