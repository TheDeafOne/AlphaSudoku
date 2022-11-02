from .csps import csps
from .genetic import genetic
from .genetic import hybrid

class Algos:
    def __init__(self):
        pass

    def csps(self, board):
        return csps.CSPS(board)
    
    def hybrid(self, board):
        return hybrid.HybridSolver(board=board)