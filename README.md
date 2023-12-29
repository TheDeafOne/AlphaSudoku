# AlphaSudoku
AlphaSudoku is a research project in an effort to analyze and display different algorithms that can solve Sudoku. While traditionally solved with backtracking, because of Sudoku's simplicity, it is possible to reasonably use algorithms such as genetic or harmony search. We explore these and combine them with a variety of other algorithms, creating a full display of classical AI search methods. Some of these algorithms are:
* Backtracking
* Constraint Satisfaction
* AC-3
* Genetic search
* Simulated annealing
Our hope is that by applying these algorithms in a practical setting and visualizing the process, others will be able to better use them elsewhere.

### A Note on Tech
Though it is possible to use any language to implement, analyze, and visualize these algorithms, we found Python to be the most suited to our needs. Additionally, we use Flask, a lightweight web framework to help visualize the algorithms.

### Further Exploration
While we accomplished our initial goal of comparing a standard algorithm against a few non-standard ones, there are plenty of new ways to solve Sudoku. Some of these algorithms are:
- A*
- Hill climbing
- Iterative deepening
- Uniform-cost search

It should be noted that some of these algorithms are effectively useless by themselves, as they get caught in local minima. To avoid this problem, we use probabilistic algorithms like simulated annealing to bump the search state into a solvable path. We discuss this further in our paper.
### Paper
Our research mostly discusses the differences between traditional solutions and our main alternative algorithm, genetic search, but there is also discussion of other algorithms and how they compare.
[Comparison of Non-Deterministic Sudoku Algorithms](comparison_of_nondterministic_algorithms.pdf)
## Installation
To use this project, you'll need a Python version > 3.6. \
You can clone the project using `git clone https://github.com/TheDeafOne/AlphaSudoku.git` \
and install the dependencies using `python -m pip install -r requirements.txt` \
from there you can runn the `app.py` file with `python ./app.py`

## Using the Project
Theres a lot going on here, but the logic of the project can generally be broken down into three parts:
1. Board Logic
2. Algorithms
3. Visualization

Fittingly, board logic and algorithms can be found in their respective directories, but it should be noted that visualization is done through Flask. Because of this, most of the logic pertaining to it is in app.py, templates, and static, but there is some references to it throughout board logic and algorithms. This is so that the program can be run through both a console and a web application.
