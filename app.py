from flask import Flask, render_template
from algorithms import algorithms
from threading import Thread

from algorithms.genetic.hybrid import HybridSolver

algos = algorithms.Algos()

# csps = algos.csps()
# csps.run()
hybrid : HybridSolver = None
hybrid_thread : Thread = None


app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('main.html', chr=chr)

@app.route('/submit/<board_string>')
def submit_board(board_string):
    global hybrid, hybrid_thread
    if hybrid_thread is not None:
        hybrid_thread = None
    hybrid = algos.hybrid(board_string)
    return "GOOD"

def run_hybrid_task():
    if hybrid is not None:
        hybrid.run()

@app.route('/run/')
def run_hybrid():
    hybrid_thread = Thread(target=run_hybrid_task)
    hybrid_thread.start()
    return "GOOD"

@app.route('/poll/')
def poll_hybrid():
    return hybrid.board.get_board()


if __name__ == '__main__':
    app.run(debug=True)