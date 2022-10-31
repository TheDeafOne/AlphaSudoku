from copy import copy
import random as rand

from board_logic import board
from board_logic.board_generator import BoardGenerator
from board_logic.board import Board
from math import exp
class SASolver():
    TEMP_DECAY_FACTOR = 0.95
    MUTATION_PROB = 0.8
    NEIGHBORHOOD = 40
    STARTING_TEMP = 200
    SAME_THRESH = 1000

    def __init__(self):
        self.fitness = 300
        self.temperature = self.STARTING_TEMP
        self.nbhood = self.NEIGHBORHOOD
        self.same_count = 0

        board_generator = BoardGenerator()
        self.board = Board()
        # print()
        self.board.new_board()
        print(self.board.get_board_2D())
        # self.board.set_board(board_generator.generate_board())
        # print(self)
        self.board.display_group_board()
        # print(self.board.get_group_board())
        # print(self.board.get_group_board_2D())
        

    def run(self):
        current_board = self.board
        print("Evaluating fitness...")
        while self.fitness > 10:
            new_fitness = self.fitness_function(current_board)
            if self.fitness == new_fitness:
                self.same_count += 1
            else:
                self.same_count = 0
            if self.same_count > self.SAME_THRESH:
                self.temperature = self.STARTING_TEMP
            self.fitness = new_fitness
            # print("Find neighbor...")
            n_board = self.find_neighbor(current_board, self.nbhood)
            print(f"Evaluating fitness: {self.fitness}...")
            delta_E = self.fitness_function(n_board) - self.fitness
            if delta_E < 0:
                current_board = n_board
            elif rand.random() < exp(-delta_E / self.temperature):
                current_board = n_board
            self.temperature *= self.TEMP_DECAY_FACTOR
            # print(f"Updating temp: {self.temperature}")

        # cycle=1
        # k = 10 # offspring generation factor
        # N = 10 # Number of runs per cycle


        # # self.fitness_function(self.board.get_board_2D())

        # pop_size = self.PARENT_POP_SIZE/cycle

        # # # DEFINE OFFSPRING SIZE
        # offspring_size = pop_size * k

        # # # GENERATE POPULATION
        # # self.generate_population(offspring_size)


        # # while cycle < self.C:
        # while self.fitness > 0 and cycle < self.C:
        #     # DEFINE POP SIZE
        #     # pop_size = self.PARENT_POP_SIZE//cycle

        #     # DEFINE OFFSPRING SIZE
        #     # offspring_size = pop_size * k

        #     # GENERATE POPULATION
        #     population = self.generate_population(offspring_size)

        #     # FOR EACH ITERATION i <= N PERFORM CROSSOVER, EVALUATE POPULATION, AND CHOOSE BEST u SOLUTIONS
        #     for i in range(N):
        #         self.crossover(population)
        #         eval_pop = {board : self.fitness_function(board) for board in population}
        #         sorted_pop = [i for i in sorted(eval_pop, key=eval_pop.get)]
        #         population = sorted_pop[:self.PARENT_POP_SIZE]
        #         fitnesses = [self.fitness_function(i) for i in population]
        #         print(f"AVERAGE FITNESS OF POP = {sum(fitnesses)/len(fitnesses)}")

        #     # top_sols = sorted_pop[0:pop_size]
        #     # print(fitnesses)
        #     # PERFORM MUTATION OVER FEW GOOD SOLUTIONS
        #     self.mutation(population)

        #     # FIND BEST SOLUTION FOR UPDATING GROUP TABLE
        #     self.update_group_table(population[0], population)
        #     print()
        #     self.board.display_group_board()
        #     print()
        #     self.fitness = self.fitness_function(self.board)
        #     print(self.fitness)
        #     # print(f"FITNESS: {self.fitness_function(self.board)}")

        #     cycle += 1 

    # def sort_pop(self, a, b):
        # if self.fitness_function(a) > self.fitness_function(b):
    
    def find_neighbor(self, board:Board, neighborhood: int):
        gt = self.board.get_group_board_2D()
        neighbor = copy(board)
        indices = list(range(1,82))
        for _ in range(neighborhood):
            i = rand.choice(indices)
            r = chr(65+ i // 9)
            c = str(i  % 9 + 1)
            rc = r+c
            if rand.random() < self.MUTATION_PROB:
                # print(rc)
                try:
                    neighbor.set_board_value(rc, rand.choice(gt[i//9][i%9]))
                except Exception as E:
                    # print()
                    pass
        return neighbor

    def update_group_table(self, best_board: Board, boards):
        gt = self.board.get_group_board()
        best_board_board = best_board.get_board()
        board_boards = [b.get_board() for b in boards]
        for i in range(81):
            r = chr(65 + i // 9)
            c = str(i % 9 + 1)
            rc = r+c
            val = best_board_board[rc]
            if val in gt[rc]:
                if sum(1 if val == b[rc] else 0 for b in board_boards) >= self.BEST_SOLS_RATIO * len(board_boards): # FIX THIS PART
                    if rand.random() < self.UPDATE_PROB:
                        self.board.set_board_value(rc, val)


    def mutation(self, boards: list[Board]):
        gt = self.board.get_group_board_2D()
        # print(len(boards))
        for board in boards:
            # s = board.get_board_string()
            for i in range(81):
                r = chr(65+ i // 9)
                c = str(i  % 9 + 1)
                rc = r+c
                if rand.random() < self.MUTATION_PROB:
                    # print(rc)
                    try:
                        board.set_board_value(rc, rand.choice(gt[i//9][i%9]))
                    except Exception as E:
                        # print()
                        pass
                        # print(gt[i//9][i%9])
                        # print(rc)
                        # print(E)
        

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
        for i in range(self.PARENT_POP_SIZE):
            # Generate random board from group table
            board = Board(board=self.get_rand_solution_from_gt(self.board.get_group_board_2D()))
            fitness = self.fitness_function(board)
            # print(f"fitness = {fitness}")
            # print(f"board = {board}")
            population.append(board)

        return population
    
    def gen_board(self):
        return Board(board=self.get_rand_solution_from_gt(self.board.get_group_board_2D()))

    def get_rand_solution_from_gt(self, group_table):
        new_sol = [ [0] * 9 for _ in range(9)]
        for row_idx, row in enumerate(group_table):
            for col_idx, col in enumerate(row):
                if len(col) > 1:
                    choice = rand.choice(col)
                else:
                    # print(col)
                    if len(col) == 0:
                        print(f"col = {col}")
                    try:
                        choice = col[0]
                    except Exception as e:
                        print(e)
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

