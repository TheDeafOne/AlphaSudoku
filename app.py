from flask import Flask, render_template
from algorithms import algorithms
from threading import Thread
from board_logic.board_generator import BoardGenerator
from algorithms.genetic.hybrid import HybridSolver
from algorithms.csps.csps import CSPS

algos = algorithms.Algos()
generator = BoardGenerator()

hybrid : HybridSolver = None
hybrid_thread : Thread = None
csps : CSPS = None
csps_thread : Thread = None


app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('main.html', chr=chr)

@app.route('/submit/<algorithm>/<board_string>')
def submit_board(algorithm, board_string):
    global hybrid, hybrid_thread, csps, csps_thread
    if hybrid_thread is not None:
        hybrid_thread = None
    if csps_thread is not None:
        csps_thread = None
    if algorithm == "genetic":
        hybrid = algos.hybrid(board_string)
    else:
        csps = algos.csps(board_string, True)
    return "GOOD"

def run_hybrid_task():
    if hybrid is not None:
        hybrid.run()

def run_csps_task():
    if csps is not None:
        csps.solve()

@app.route('/run/<algorithm>')
def run(algorithm):
    if algorithm == "genetic":
        hybrid_thread = Thread(target=run_hybrid_task)
        hybrid_thread.start()
    else:
        hybrid_thread = Thread(target=run_csps_task)
        hybrid_thread.start()
    return "GOOD"

@app.route('/poll/<algorithm>')
def poll(algorithm):
    if algorithm == "genetic":
        return hybrid.board.get_board()
    else:
        ret = {}
        board = csps._board
        # if len(csps.solved_board) > 0:

        for el in board:
            if len(board[el]) > 1:
                ret[el] = 0
            else:
                ret[el] = board[el]
        csps._next_step = True
        return ret

# @app.route('/new_board/')
# def new_board():
#     return generator.generate_board()

if __name__ == '__main__':
    app.run(debug=True)