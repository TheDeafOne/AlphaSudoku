import copy
from email.errors import NonASCIILocalPartDefect
import random as rand
from board_logic import board

from board_logic.board_generator import BoardGenerator
from board_logic.board import Board
class GeneticSolver():
    C = 2
    PARENT_POP_SIZE = 5
    OFFSPRING_POP_SIZE = 500
    CROSSOVER_PROB = 0.7
    MUTATION_PROB = 0.4

    def __init__(self):
        self.fitness = 0
        board_generator = BoardGenerator()
        self.board = Board()
        self.board.set_board(board_generator.generate_board())
        self.board.display_group_board()
        # print(self.board.get_group_board())
        # print(self.board.get_group_board_2D())
        

    def run(self):
        cycle=1
        k = 5 # offspring generation factor
        N = 15 # Number of runs per cycle


        self.fitness_function(self.board.get_board_2D())

        pop_size = self.PARENT_POP_SIZE/cycle

        # DEFINE OFFSPRING SIZE
        offspring_size = pop_size * k

        # GENERATE POPULATION
        self.generate_population(offspring_size)


        # while self.fitness >=0:
            # while cycle < self.C:
                # DEFINE POP SIZE
                # pop_size = self.PARENT_POP_SIZE/cycle

                # # DEFINE OFFSPRING SIZE
                # offspring_size = pop_size * k

                # # GENERATE POPULATION
                # self.generate_population(offspring_size)


                # FOR EACH ITERATION i <= N PERFORM CROSSOVER, EVALUATE POPULATION, AND CHOOSE BEST u SOLUTIONS

                # PERFORM MUTATION OVER FEW GOOD SOLUTIONS

                # FIND BEST SOLUTION FOR UPDATING GROUP TABLE


                # 
                # pass
                # cycle += 1 


    def generate_population(self, pop_size):
        population = []
        for i in range(self.PARENT_POP_SIZE):
            # Generate random board from group table
            board = Board(board=self.get_rand_solution_from_gt(self.board.get_group_board_2D()))
            fitness = self.fitness_function(board.get_board_2D())
            print(f"fitness = {fitness}")
            print(f"board = {board}")
            population.append(board)

        return population

    def get_rand_solution_from_gt(self, group_table):
        new_sol = [ [0] * 9 for _ in range(9)]
        for row_idx, row in enumerate(group_table):
            for col_idx, col in enumerate(row):
                if len(col) > 1:
                    choice = rand.choice(col)
                else:
                    choice = col[0]
                new_sol[row_idx][col_idx] = choice
        return new_sol

    def fitness_function(self, board):
        board_list = board
        fitness = 0
        flattened_list = [item for sublist in board_list for item in sublist]
        for j in range(1, 10):
            for i in range(0, 9):
                fitness += board_list[i].count(f"{j}")
                col = [item[i] for item in board_list]
                fitness += col.count(f"{j}")
            fitness += self.check_all_blocks(f"{j}", board_list) 
            fitness += abs(flattened_list.count(f"{i}")-9)
            fitness -= 27
        return fitness

    def check_all_blocks(self, num, board):
        val = 0
        for i in range(0,9):
            for j in range(0,9):
                if board[i//3 + j%3][3*(i%3) + j//3] == num:
                    val += 1
        return val

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

