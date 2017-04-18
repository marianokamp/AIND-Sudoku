# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  

A: Apply inference to the problem space.

Given that the search we will later on apply is brute forcing it, at worst trying out all open values,
we will combine that approach with using inference. We use inference to cut down the problem space first (and continuously thereafter).
For simpler Sudokus this should do the trick already. Otherwise we will resort to search to get to a solution, but even then search is an
iterative approach trying out remaining combinations, and benefits from applying inference to new states of the Sudoku.

The inference itself is implemented in only_choice, eliminate and naked_twins. In all of these methods we use our knowledge of the constraints to reason
which of the remaining values can be removed (reduce_puzzle).

Let's illustrate with this question's subject: Naked Twins.
We concentrate on one unit
(more on what a unit is in the answer to the next question) at a time and try to find within the
unit currently observed to find two boxes that only contain exactly two values and exactly
the same in both boxes.

Given the rule that every digit from 1 to 9 can only be used once, it is clear that these digits
must be in either of these two boxes. This by itself doesn't help with the two boxes at hand,
but we can infer that the digits in those two boxes cannot be valid assignments in the remaining
boxes of the **same** unit.

We can therefore remove those digits from all other boxes of the unit.


# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: The structure of the existing code decoupled the representation of a unit from the constraints that can be applied to it.

The code introduced a unit, which is a collection of boxes. The shape of a unit is in general arbitrary, but implicitly needs to be of length 9 as a global constraint is
that all digits from 1 to 9 must occur once and only once in a unit. The layout however is arbitrary. The classic layouts are rows, columns and squares, but it would be
possible as well to lay the boxes out circularly around the center of the Sudoku.

Here the question was about the diagonals. These are represented as two more units, one from top-left to bottom-right and one from top-right to bottom-left.

Adding them to the existing units was the only change necessary.  For the generic logic is only counts that there are 9 boxes, if you look at them from the perspective of a single box there is this single box and eight peers. This is handled by the existing code already.

As all constraints are agnostic to their unit's layout, the existing constraints could be applied as-is, meaning that naked twins can be found as well as the other two methods can be applied.

All existing constraints are automatically propagated. 

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project.
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant, which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command `pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.  You will be prompted for a username and password.  If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login for alternate login instructions.

This process will create a zipfile in your top-level directory named sudoku-<id>.zip.  This is the file that you should submit to the Udacity reviews system.
