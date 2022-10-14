import copy
class GeneticSolver():
    fitness = 0
    C = 100
    board = list(list())
    group_table = list(list())
    def __init__(self):
        self.board = []
        board_chars = [int(x) for x in "301086504046521070500000001400800002080347900009050038004090200008734090007208103"]
        for i in range(9):
            self.board.append(board_chars[i*9:i*9+9])
        self.group_table = copy.deepcopy(self.board)
        self.print_board()
        self.print_group_table()

    def run(self):
        cycle=0
        self.make_group_table()
        while self.fitness >=0:
            while cycle < self.C:
                pass
                cycle += 1 

    def cost_function(self):
        flattened_list = [item for sublist in self.board for item in sublist]
        for j in range(1, 10):
            for i in range(0, 9):
                self.fitness += self.board[i].count(j)
                col = [item[i] for item in self.board]
                self.fitness += col.count(j)
            self.fitness += self.check_all_blocks(j) 
            self.fitness += abs(flattened_list.count(i)-9)


    def make_group_table(self):
        for row_idx, i in enumerate(self.board):
            possibilities = [p for p in range(1,10)]
            for col_idx, j in enumerate(i):
                 if j == 0:
                    new_list = list(set(possibilities)
                            .difference(self.row_vals(row_idx, col_idx))
                            .difference(self.col_vals(row_idx, col_idx))
                            .difference(self.block_vals(row_idx, col_idx)))
                    self.group_table[row_idx][col_idx] = new_list
    
    def row_vals(self, row, col):
        return set([val for val in self.board[row] if val != 0])

    def col_vals(self, row, col):
        return set([row[col] for row in self.board if row[col] != 0])

    def block_vals(self, row, col):
        start_row = 3*(row//3)
        start_col = 3*(col//3)
        vals = []
        for i in range(start_row, start_row+3):
            vals.extend([j for j in self.board[i][start_col:start_col+3] if j != 0])
        return set(vals)


    def check_all_blocks(self, num):
        val = 0
        for i in range(0,9):
                for j in range(0,9):
                    if self.board[i//3 + j%3][3*(i%3) + j//3] == num:
                        val += 1

    def print_board(self):
        print("BOARD:")
        for i, line in enumerate(self.board):
            for j, val in enumerate(line):
                if j%3 == 0 and j != 0:
                    print(" || ", end="")
                print(val, end="")
            print()
            if (i+1)%3 == 0 and i != 8:
                print("-----------------\n-----------------")
    
    def print_group_table(self):
        max_len = max([len(str(val)) for row in range(len(self.group_table)) for val in self.group_table[row]])
        for i, line in enumerate(self.group_table):
            for j, val in enumerate(line):
                print(str(val).ljust(max_len + 1, " "), end="")
            if (i+1)%3 == 0:
                print()
            print()

Solve = GeneticSolver()

