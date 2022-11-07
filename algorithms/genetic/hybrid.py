from cProfile import run
from copy import copy,deepcopy
from math import exp, log
import random as rand

from board_logic import board
from board_logic.board_generator import BoardGenerator
from board_logic.board import Board
class HybridSolver():
    C = 4000
    PARENT_POP_SIZE = 15
    OFFSPRING_POP_SIZE = 200
    CROSSOVER_PROB = 0.7
    MUTATION_PROB = 0.4
    UPDATE_PROB = 0.3
    BEST_SOLS_RATIO = 0.9
    TEMP_DECAY_FACTOR = 0.95
    SA_MUTATION_PROB = 0.8
    NEIGHBORHOOD = 75
    STARTING_TEMP = 1
    TEMP_THRESH_FACTOR = 0.1
    STUCK_THRESHOLD = 60

    def __init__(self, board=None):
        self.fitness = 100
        self.temperature = self.STARTING_TEMP
        self.nbhood = self.NEIGHBORHOOD
        self.same_count = 0
        board_generator = BoardGenerator()
        if board is None:
            self.board = Board()
            # print()
            self.board.new_board()
        else:
            self.board = Board(board=board)
        print(self.board.get_board_2D())
        self.board.display_group_board()
        self.og_board = deepcopy(self.board)
        

    def run(self):
        cycle=1
        k = 5 # offspring generation factor
        N = 5 # Number of runs per cycle
        
        pop_size = self.PARENT_POP_SIZE/cycle

        # # DEFINE OFFSPRING SIZE
        offspring_size = pop_size * k

        # # GENERATE POPULATION
        # self.generate_population(offspring_size)
        stuck_count = 0
        bestest_fitness = 300
        factor = self.C / (10 ** (int(log(self.C, 10)) - 1))
        running_average_fitness = self.fitness

        # while cycle < self.C:
        while self.fitness > 0 and cycle < self.C:
            running_average_fitness += self.fitness
            running_average_fitness /= 2
            running_average_fitness = round(running_average_fitness, 2)
            if cycle % factor == 0:
                print(f"Fitness {running_average_fitness} at cycle {cycle}")
            # DEFINE POP SIZE
            # pop_size = self.PARENT_POP_SIZE//cycle

            # DEFINE OFFSPRING SIZE
            # offspring_size = pop_size * k

            # GENERATE POPULATION
            population = self.generate_population(offspring_size)

            # FOR EACH ITERATION i <= N PERFORM CROSSOVER, EVALUATE POPULATION, AND CHOOSE BEST u SOLUTIONS
            for i in range(N):
                if bestest_fitness == 0:
                    break
                self.crossover(population)
                eval_pop = {board : self.fitness_function(board) for board in population}
                sorted_pop = [i for i in sorted(eval_pop, key=eval_pop.get)]
                population = sorted_pop[:self.PARENT_POP_SIZE]

                # fitnesses = [self.fitness_function(i) for i in population]
                best_fitness = self.fitness_function(population[0])
                if best_fitness == 0:
                    self.board = population[0]
                    self.fitness = 0
                if best_fitness < bestest_fitness:
                    bestest_fitness = best_fitness
                    stuck_count = 0
                else:
                    stuck_count += 1
                # print(f"AVERAGE FITNESS OF POP = {sum(fitnesses)/len(fitnesses)}")
            if self.fitness == 0:
                break
            # top_sols = sorted_pop[0:pop_size]
            # print(fitnesses)
            # PERFORM MUTATION OVER FEW GOOD SOLUTIONS
            if stuck_count < self.STUCK_THRESHOLD:
                self.mutation(population)
            else:
                stuck_count = 0
                bestest_fitness = 300
                self.board = deepcopy(self.og_board)
                print("Doing SA on population.")
                self.mutation_sa(population)

            # FIND BEST SOLUTION FOR UPDATING GROUP TABLE
            self.update_group_table(population[0], population)
            # print()
            # self.board.display_group_board()
            # print()
            if self.fitness > self.fitness_function(self.board):
                stuck_count = 0
            self.fitness = self.fitness_function(self.board)
            print(self.fitness)
            # print(f"FITNESS: {self.fitness_function(self.board)}")

            cycle += 1 
        if self.fitness == 0:
            self.board.display_board()

    # def sort_pop(self, a, b):
        # if self.fitness_function(a) > self.fitness_function(b):
    def update_group_table(self, best_board: Board, boards):
        """
            Updates the group table probabilistically using the best board as an informant for which cells to fix
        
        """

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
        """
            Performs mutation as defined in depth in the paper
        """

        gt = self.board.get_group_board_2D()
        # print(len(boards))
        for board in boards:
            for i in range(81):
                r = chr(65 + i // 9)
                c = str(i % 9 + 1)
                rc = r+c
                if rand.random() < self.MUTATION_PROB:
                    board.set_board_value(rc, rand.choice(gt[i//9][i%9]))

    def mutation_sa(self, boards: list[Board]):
        """
        Performs mutation by performing simulated annealing as described in depth in the paper
        """
        i = 0
        for board in boards:
            if i % int(1 + 10 * i  / len(boards)) == 0: 
                print("*", end="", flush=True)
            temperature = self.STARTING_TEMP
            old_fitness = self.fitness_function(board)
            while temperature > self.STARTING_TEMP * self.TEMP_THRESH_FACTOR and old_fitness > 0:
                og_board = board.get_board()
                old_fitness = self.fitness_function(board)
                delta = self.find_neighbor(board, self.nbhood)
                og = []
                for loc, val in delta:
                    og.append((loc, og_board[loc]))
                    board.set_board_value(loc, val)
                delta_E = self.fitness_function(board) - old_fitness
                if delta_E <= 0:
                    pass
                elif rand.random() < exp(-delta_E / temperature):
                    pass
                else:
                    for loc, val in og:
                        board.set_board_value(loc, val)
                temperature *= self.TEMP_DECAY_FACTOR
        print()
    
    def find_neighbor(self, board:Board, neighborhood: int):
        """
        Python implementation of the neighbor algorithm described in the paper
        """
        gt = self.og_board.get_group_board_2D()
        indices = list(range(81))
        delta_op = []
        for _ in range(neighborhood):
            index = rand.randint(0,len(indices) - 1)
            i = indices.pop(index)
            r = chr(65+ i // 9)
            c = str(i  % 9 + 1)
            rc = r+c
            if rand.random() < self.SA_MUTATION_PROB:
                delta_op.append((rc, rand.choice(gt[i//9][i%9])))
        return delta_op

    
    
    def crossover(self, population):
        """
        Implements crossover as defined in the paper
        """
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
        """
        Creates a population by picking random children from the current group table
        """
        population = []
        for i in range(self.PARENT_POP_SIZE):
            # Generate random board from group table
            board = Board(board=self.get_rand_solution_from_gt(self.board.get_group_board_2D()))
            fitness = self.fitness_function(board)
            # print(f"fitness = {fitness}")
            # print(f"board = {board}")
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
        """
        Calculates the fitness of the board using the fitness function defined in the paper
        """
        board_list = board.get_board_2D()
        # sub_grids = board.get_subgrids()
        col_counts = [{str(i+1): -1 for i in range(9)} for _ in range(9)]
        row_counts = [{str(i+1): -1 for i in range(9)} for _ in range(9)]
        tot_counts = {str(i+1): 0 for i in range(9)}
        fitness = 0
        for r in range(9):
            for c in range(9):
                cell = board_list[r][c]
                if cell == '0': continue
                col_counts[c][cell] += 1
                row_counts[r][cell] += 1
                tot_counts[cell]  += 1
        for i in range(9):
            fitness += sum([count ** 2 for count in col_counts[i].values()])
            fitness += sum([count ** 2 for count in row_counts[i].values()])
        fitness += sum([abs(count - 9) for count in tot_counts.values()])
        
        return fitness

