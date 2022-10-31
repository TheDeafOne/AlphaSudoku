import copy
from email.errors import NonASCIILocalPartDefect
import random as rand
import sys
from board_logic import board
from board_logic.board_generator import BoardGenerator
from board_logic.board import Board
class GeneticSolver():
    C = 1000
    PARENT_POP_SIZE = 20 # has to be bigger than cycle
    OFFSPRING_POP_SIZE = 500
    CROSSOVER_PROB = 0.7
    MUTATION_PROB = 0.3
    UPDATE_PROB = 0.9
    BEST_SOLS_RATIO = .9

    def __init__(self, board=None):
        self.fitness = 100
        # board_generator = BoardGenerator()
        if board:
            self.board = board
        else:
            self.board = Board()
            # print()
            self.board.new_board()
            print(self.board.get_board_2D())
            # self.board.set_board(board_generator.generate_board())
            # print(self)
            self.board.display_group_board()
        
        self.original_group_table = self.board.get_group_board()
        # print(self.board.get_group_board())
        # print(self.board.get_group_board_2D())
        

    def run(self):
        cycle=1
        k = 1 # offspring generation factor
        N = 1 # Number of runs per cycle


        # self.fitness_function(self.board.get_board_2D())

        # pop_size = self.PARENT_POP_SIZE/cycle
        

        # # DEFINE OFFSPRING SIZE
        # offspring_size = pop_size * k

        # # GENERATE POPULATION
        # self.generate_population(offspring_size)


        # while cycle < self.C:
        while self.fitness > 0 and cycle < self.C:
            # DEFINE POP SIZE
            pop_size = self.PARENT_POP_SIZE
            # print(f"pop_size = {pop_size}")
            # DEFINE OFFSPRING SIZE
            offspring_size = pop_size * k
            # print(f"Offspring size = {offspring_size}")

            # GENERATE POPULATION
            population = self.generate_population(offspring_size)
            # print(f"offspring_size")
            # FOR EACH ITERATION i <= N PERFORM CROSSOVER, EVALUATE POPULATION, AND CHOOSE BEST u SOLUTIONS
            for i in range(N):

                # print(f"len population before crossover {len(population)}")
                self.crossover(population)
                # print(f"len population after crossover {len(population)}")

                eval_pop = {board : self.fitness_function(board) for board in population}


                sorted_pop = [i for i in sorted(eval_pop, key=eval_pop.get)]

                population = sorted_pop[:self.PARENT_POP_SIZE]
                # print(len(population))
                fitnesses = [self.fitness_function(i) for i in population]
                # print(f"AVERAGE FITNESS OF POP = {sum(fitnesses)/len(fitnesses)}")
            # PERFORM MUTATION OVER FEW GOOD SOLUTIONS
            self.mutation(population)

            # FIND BEST SOLUTION FOR UPDATING GROUP TABLE
            if self.fitness_function(population[0]) < 1:
                self.board = population[0]
            else:
                self.update_group_table(population[0], population)
            print()
            self.board.display_group_board()
            print()
            # self.board.display_board()
            self.fitness = self.fitness_function(self.board)
            print(self.fitness)
            # print(f"FITNESS: {self.fitness_function(self.board)}")

            cycle += 1 

    # def sort_pop(self, a, b):
        # if self.fitness_function(a) > self.fitness_function(b):
    def update_group_table(self, best_board: Board, boards):
        best_board_board = best_board.get_board()
        # best_board_group_board = best_board.get_group_board()
        # print(best_board_board)
        # best_board.display_board()
        # print("123456789")
        # print(best_board_group_board)
        board_boards = [b.get_board() for b in boards]
        for i in range(81):
            gt = self.board.get_group_board()
            r = chr(65 + i // 9)
            c = str(i % 9 + 1)
            rc = r+c
            val = best_board_board[rc]
            # if not val in peer_vals:
            if val in gt[rc] and val in self.original_group_table[rc]:
                if sum(1 if val == b[rc] else 0 for b in board_boards) >= self.BEST_SOLS_RATIO * len(board_boards): # FIX THIS PART
                    if rand.random() < self.UPDATE_PROB:
                        peer_vals = [gt[index] for index in best_board.peer_indexes[rc]]
                        # print(peer_vals)
                        if not any(peer == set(val) for peer in peer_vals):
                        # print("does this even work")
                            self.board.set_board_value(rc, val)
                            self.board._update_group_board()


    # def delete_repetitions(board: Board):
        # board2d = board.get_board_2D()

        # for idx, row in enumerate(board.get_board_2D()):
            # delete = [val for val in row if row.count(val) > 1]
            # row = [0 if val in delete else val for val in row]
            # board2d[idx] = row
        
        # for idx, 

        # for row_idx, row in enumerate(board.get_board_2D()):
            # for col_idx, val in enumerate(row):
                # if row.count(val) > 1:
                    # board2d[row_idx][col_idx] = 0
                # if 
                    



    def mutation(self, boards: list[Board]):
        # gt = self.board.get_group_board_2D()
        for board in boards:
            for i in range(81):
                r = chr(65+ i // 9)
                c = str(i  % 9 + 1)
                rc = r+c
                if rand.random() < self.MUTATION_PROB:
                    try:
                        board.set_board_value(rc, rand.choice(self.original_group_table[i//9][i%9]))
                    except Exception as E:
                        pass
        

    def crossover(self, population):
        # print(rand.randint(0,len(population)))
        indices = list(range(len(population)))
        pairs = [(indices.pop(rand.randint(0, len(indices) - 1)), indices.pop(rand.randint(0, len(indices) - 1))) for i in range(len(population) // 2)]
        for i_1, i_2 in pairs:
            parent_1 : Board = population[i_1]
            parent_2 : Board = population[i_2]

            s1 = parent_1.get_board_string()
            s2 = parent_2.get_board_string()
            c_p = [rand.random() for i in range(81)]

            n_s1 = ''.join([s1[i] if c_p[i] < self.CROSSOVER_PROB else s2[i] for i in range(81)])
            n_s2 = ''.join([s2[i] if c_p[i] < self.CROSSOVER_PROB else s1[i] for i in range(81)])
            
            population.append(Board(board=n_s1))
            population.append(Board(board=n_s2))


    def generate_population(self, pop_size):
        population = []
        for i in range(pop_size):

            board = Board(board=self.get_rand_solution_from_gt(self.board.get_group_board_2D()))
            print('\n\n\pop board')
            board.display_board()
            population.append(board)


        return population

    def get_rand_solution_from_gt(self, group_table):
        new_sol = [ [0] * 9 for _ in range(9)]
        for row_idx, row in enumerate(group_table):
            for col_idx, col in enumerate(row):
                if len(col) > 1:
                    choice = rand.choice(col)
                else:
                    if len(col) == 0:
                        # print(f"col = {col}")
                        print("stuck in a bad solution, hoping mutation gets us out", end="\r")
                        exit(1)
                    try:
                        choice = col[0]
                    except Exception as e:
                        pass
                        # print(e)
                new_sol[row_idx][col_idx] = choice
        return new_sol

    def fitness_function(self, board: Board):
        board_list = board.get_board_2D()
        sub_grids = board.get_subgrids()
        fitness = 0
        flattened_list = [item for sublist in board_list for item in sublist]
        for j in range(1, 10):
            for i in range(0, 9):
                # print( ((1-board_list[i].count(f"{j}")) ** 2))
                fitness += ((1-board_list[i].count(f"{j}")) ** 2)
                col = [item[i] for item in board_list]
                fitness += ((1-col.count(f"{j}")) ** 2)
                # print(((1-col.count(f"{j}")) ** 2))
                fitness += ((1-sub_grids[i].count(f"{j}")) ** 2)
                # print(((1-sub_grids[i].count(f"{j}")) ** 2))
            fitness += abs(flattened_list.count(f"{i}")-9)
            # print(abs(flattened_list.count(f"{i}")-9))
        # fitness -= 27
        return fitness

    # def check_all_blocks(self, num, board):
    #     val = 0
    #     for i in range(0,9):
    #         for j in range(0,9):
    #             if board[i//3 + j%3][3*(i%3) + j//3] == num:
    #                 val += 1
    #     return val

    # def make_group_table(self):
    #     for row_idx, i in enumerate(self.board):
    #         possibilities = [p for p in range(1,10)]
    #         for col_idx, j in enumerate(i):
    #              if j == 0:
    #                 new_list = list(set(possibilities)
    #                         .difference(self.row_vals(row_idx, col_idx))
    #                         .difference(self.col_vals(row_idx, col_idx))
    #                         .difference(self.block_vals(row_idx, col_idx)))
    #                 self.group_table[row_idx][col_idx] = new_list
    
    # def row_vals(self, row, col, board):
    #     return set([val for val in board[row] if val != 0])

    # def col_vals(self, row, col, board):
    #     return set([row[col] for row in board if row[col] != 0])

    # def block_vals(self, row, col, board):
    #     start_row = 3*(row//3)
    #     start_col = 3*(col//3)
    #     vals = []
    #     for i in range(start_row, start_row+3):
    #         vals.extend([j for j in board[i][start_col:start_col+3] if j != 0])
    #     return set(vals)




    # def print_board(self):
    #     print("BOARD:")
    #     for i, line in enumerate(self.board):
    #         for j, val in enumerate(line):
    #             if j%3 == 0 and j != 0:
    #                 print(" || ", end="")
    #             print(val, end="")
    #         print()
    #         if (i+1)%3 == 0 and i != 8:
    #             print("-----------------\n-----------------")
    
    # def print_group_table(self):
    #     max_len = max([len(str(val)) for row in range(len(self.group_table)) for val in self.group_table[row]])
    #     for i, line in enumerate(self.group_table):
    #         for j, val in enumerate(line):
    #             print(str(val).ljust(max_len + 1, " "), end="")
    #         if (i+1)%3 == 0:
    #             print()
    #         print()

# Solve = GeneticSolver()

