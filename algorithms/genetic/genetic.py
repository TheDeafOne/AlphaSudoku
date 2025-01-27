import copy
from email.errors import NonASCIILocalPartDefect
import random as rand

from board_logic import board
from board_logic.board_generator import BoardGenerator
from board_logic.board import Board
class GeneticSolver():
    C = 100

    # parent population size
    PARENT_POP_SIZE = 20

    # offspring population size
    OFFSPRING_POP_SIZE = 500

    CROSSOVER_PROB = 0.7

    MUTATION_PROB = 0.4
    UPDATE_PROB = 0.3
    BEST_SOLS_RATIO = 0.8

    def __init__(self):
        self.fitness = 100
        board_generator = BoardGenerator()
        self.board = Board()
        self.board.new_board()
        self.board.display_group_board()

    def run(self):
        cycle=1
        k = 10 # offspring generation factor
        N = 10 # Number of runs per cycle


        # self.fitness_function(self.board.get_board_2D())

        pop_size = self.PARENT_POP_SIZE/cycle

        # # DEFINE OFFSPRING SIZE
        offspring_size = pop_size * k

        # # GENERATE POPULATION
        # self.generate_population(offspring_size)



        while self.fitness > 0 and cycle < self.C:
            # DEFINE POP SIZE
            # pop_size = self.PARENT_POP_SIZE//cycle

            # DEFINE OFFSPRING SIZE
            # offspring_size = pop_size * k

            # GENERATE POPULATION
            population = self.generate_population(offspring_size)

            # FOR EACH ITERATION i <= N PERFORM CROSSOVER, EVALUATE POPULATION, AND CHOOSE BEST u SOLUTIONS
            for i in range(N):
                self.crossover(population)
                eval_pop = {board : self.fitness_function(board) for board in population}
                sorted_pop = [i for i in sorted(eval_pop, key=eval_pop.get)]
                population = sorted_pop[:self.PARENT_POP_SIZE]
                fitnesses = [self.fitness_function(i) for i in population]
                print(f"AVERAGE FITNESS OF POP = {sum(fitnesses)/len(fitnesses)}")

            # PERFORM MUTATION OVER FEW GOOD SOLUTIONS
            self.mutation(population)

            # FIND BEST SOLUTION FOR UPDATING GROUP TABLE
            self.update_group_table(population[0], population)
            print()
            self.board.display_group_board()
            print()
            self.fitness = self.fitness_function(self.board)
            print(self.fitness)

            cycle += 1 

    
    def update_group_table(self, best_board: Board, boards):
        """
            Updates the group table probabilistically using the best board as an informant for which cells to fix
        
        """

        # define the best boards, and get important attributes
        gt = self.board.get_group_board()
        best_board_board = best_board.get_board()
        board_boards = [b.get_board() for b in boards]

        # Update the cells one by one
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

        """
            Performs mutation as defined in depth in the paper
        """
        gt = self.board.get_group_board_2D()

        for board in boards:
            for i in range(81):
                r = chr(65 + i // 9)
                c = str(i % 9 + 1)
                rc = r+c

                # pick a random value from the group table probabilistically
                if rand.random() < self.MUTATION_PROB:
                    try:
                        board.set_board_value(rc, rand.choice(gt[i//9][i%9]))
                    except Exception as E:
                        # print()
                        pass
        

    """
        Implements crossover as defined in the paper
    """
    def crossover(self, population):


        # get all the indices
        indices = list(range(len(population)))


        # pair up all the children randomly
        pairs = [(indices.pop(rand.randint(0, len(indices) - 1)), indices.pop(rand.randint(0, len(indices) - 1))) for i in range(len(population) // 2)]
        
        # swap values between the pairs
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
        """
        Creates a population by picking random children from the current group table
        """
        population = []
        for i in range(self.PARENT_POP_SIZE):
            # Generate random board from group table
            board = Board(board=self.get_rand_solution_from_gt(self.board.get_group_board_2D()))
            fitness = self.fitness_function(board)
            population.append(board)

        return population

    
    def get_rand_solution_from_gt(self, group_table):
        """
        Picks a random value from each of the cells that do not have fixed values to generate a random child solution from the gt
        """
        new_sol = [ [0] * 9 for _ in range(9)]
        for row_idx, row in enumerate(group_table):
            for col_idx, col in enumerate(row):
                if len(col) > 1:
                    choice = rand.choice(col)
                else:
                    if len(col) == 0:
                        print(f"col = {col}")
                    try:
                        choice = col[0]
                    except Exception as e:
                        print(e)
                new_sol[row_idx][col_idx] = choice
        return new_sol

    
    def fitness_function(self, board: Board):
        """
        Calculates the fitness of the board using the fitness function defined in the paper
        """
        board_list = board.get_board_2D()
        sub_grids = board.get_subgrids()
        fitness = 0
        flattened_list = [item for sublist in board_list for item in sublist]
        for j in range(1, 10):
            for i in range(0, 9):
                fitness += ((1-board_list[i].count(f"{j}")) ** 2)
                col = [item[i] for item in board_list]
                fitness += ((1-col.count(f"{j}")) ** 2)
                fitness += ((1-sub_grids[i].count(f"{j}")) ** 2)
            fitness += abs(flattened_list.count(f"{i}")-9)
        return fitness

