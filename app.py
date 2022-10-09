from flask import Flask, render_template
from algorithms import algorithms

algos = algorithms.Algos()

csps = algos.csps()
csps.run()


# app = Flask(__name__)

# @app.route('/')
# def hello():
#     return render_template('main.html')

# if __name__ == '__main__':
#     app.run(debug=True)