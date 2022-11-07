import time
import sys, os
sys.path.append(os.path.join(sys.path[0], "../"))

from algorithms.genetic.hybrid import HybridSolver
from board_logic.board import Board
from threading import Thread


class ParallelTester:
    def __init__(self):
        self.datapoints = []
        self.threads:list[Thread]= []
    
    def add_datapoint(self, difficulty):
        board = Board()
        board.new_board(difficulty_begin=difficulty, difficulty_end=difficulty)
        h = HybridSolver(board.get_board_string())
        start = time.perf_counter()
        h.run()
        end = time.perf_counter()
        tm = end-start
        self.datapoints.append((difficulty, tm))
    
    def make_thread(self, difficulty):
        t = Thread(target=self.add_datapoint, args=[difficulty])
        self.threads.append(t)
    
    def run_threads(self):
        for thread in self.threads:
            thread.start()
        while len(self.threads) > 0:
            self.threads[0].join()
            self.threads.pop(0)
            print(self.avg_times())
    
    def avg_times(self):
        diff_map = {}
        for diff, t in self.datapoints:
            if diff in diff_map:
                diff_map[diff].append(t)
            else:
                diff_map[diff] = [t]
        return {diff: sum(ts)/len(ts) for diff, ts in diff_map.items()}

if __name__ == "__main__":
    pt = ParallelTester()
    
    for diff in range(80,16,-1):
        for i in range(10):
            pt.make_thread(diff)
        pt.run_threads()
        print(f"{i}th run avg times are: {pt.avg_times()}")



    
