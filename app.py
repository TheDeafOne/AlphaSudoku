from flask import Flask, render_template
from algorithms import algorithms
from threading import Thread

from algorithms.genetic.hybrid import HybridSolver
from algorithms.csps.csps import CSPS

algos = algorithms.Algos()


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
        csps = algos.csps(board_string)
    return "GOOD"

def run_hybrid_task():
    if hybrid is not None:
        hybrid.run()

def run_csps_task():
    if csps is not None:
        csps.solve()

@app.route('/run/<algorithm>')
def run_hybrid(algorithm):
    if algorithm == "genetic":
        hybrid_thread = Thread(target=run_hybrid_task)
        hybrid_thread.start()
    else:
        hybrid_thread = Thread(target=run_csps_task)
        hybrid_thread.start()
    return "GOOD"

@app.route('/poll/')
def poll_hybrid():
    return hybrid.board.get_board()

if __name__ == '__main__':
    app.run(debug=True)