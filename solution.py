import collections

DEBUG = False
assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'


def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a+b for a in A for b in B]

boxes = cross(rows, cols)

# Copied over from lecture code:

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

diagonal_units =  [list([r+c for (r, c) in (zip(list(rows), list(cols)))])]
diagonal_units += [list([r+c for (r, c) in (zip(list(rows), list(reversed(cols))))])]

unitlist = row_units + column_units + square_units + diagonal_units

units = dict((s, [u for u in unitlist if s in u]) for s in boxes) # lookup table
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)  # lookup table

def assert_validity(before, after):
    """
    In case of a contraints validation, we know
    exactly when it happened as an assertion
    error with stack trace will be raised.

    I left it in for the submission, but could be
    disabled for better runtime performance.
    """
    # no box can be empty
    if not (len([box for box in boxes if len(after[box]) == 0]) == 0):
        raise AssertionError

    # every digit must be represented in each unit
    for unit in unitlist:
        for digit in '123456789':
            if not (len([box for box in unit if digit in after[box]]) > 0):
                print("Digit", digit)
                print("Unit", unit)
                print("Before:")
                display(before)
                print("After:")
                display(after)
                raise AssertionError("Every digit must be represented in every unit")


    # A singular value of a box must be unique among its peers's singular values
    # We need to take into account however that the value can still be part
    # of peers that have not been cleaned (with eliminate) yet.
    solved_boxes = [box for box in boxes if len(after[box]) == 1]
    for solved_box in solved_boxes:
        singular_value = after[solved_box]
        for peer in peers[solved_box]:
            if singular_value in after[peer] and len(after[peer]) == 1:
                print("Before:")
                display(before)
                print("After:")
                display(after)
                raise AssertionError("Solved box: %s Peer: %s Digit: %s" % (solved_box, peer, singular_value))

def debug(values, msg = ""):

    if not DEBUG:
        return

    if msg:
        print(msg)

    print("all?",  all(len(values[box]) == 1 for box in boxes))
    print("==0?", sum(len(values[box]) == 0 for box in boxes))
    print("==1?", sum(len(values[box]) == 1 for box in boxes))
    print(">1?", sum(len(values[box]) > 1 for box in boxes))


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    if DEBUG:
       before = values.copy()

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())

    if DEBUG:
        assert_validity(before, values)

    return values

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    grid = ''.join(grid.split())  # remove all whitespaces
    grid_values = ['123456789' if char == '.'  else char for char in grid]

    return dict(zip(boxes, grid_values))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    (Copied verbatim from the provided coded in class)
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    """
    If one digit is chosen for a box, remove that digit from all peer
    """
    debug(values, "before eliminate")
    for box in boxes:
        if len(values[box]) == 1:
            digit = values[box]
            for peer in peers[box]:
                if digit in values[peer]:
                    assert (peer != box)  # FIXME
                    new_val = values[peer].replace(digit, '')
                    values = assign_value(values, peer, new_val)

    debug(values, "after eliminate")

    return values

def only_choice_new(values):

    for unit in unitlist:

        for digit in '123456789':

           locations = [box for box in unit if digit in values[box]]
           if len(locations) == 1:
               values = assign_value(values, locations[0], digit)

    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    for unit in unitlist:
        # find all boxes with two values and collect these two values
        two_digits =  [values[box] for box in unit if len(values[box])==2]
        if not two_digits:
            continue

        # count the number of occurences of the two_digits
        # and if we find two, we have a twin
        twin_digits = [digits for digits, count in collections.Counter(two_digits).items() if count == 2]

        if not twin_digits:
            continue

        # remove values of naked twins in the other values within the same unit
        for box in unit:
            if len(values[box]) > 1: # exclude boxes that have a solution already
                for t in twin_digits:

                    # exclude twins,
                    # they are identified not by identity, but by that they have
                    # the twin values as the exclusive digits
                    if t == values[box]:
                        continue

                    for digit in t:
                        if digit in values[box]: values[box] = values[box].replace(digit,'')
    return values

def only_choice(values):
    """
    If there is only one choice for a digit in a unit chose that
    digit from that occurrence and remove it from its peers
    """
    for unit in unitlist:
        for digit in '123456789':
            occurrences = [box for box in unit if digit in values[box]]
            if len(occurrences) == 1:
                values = assign_value(values, occurrences[0], digit)

    return values

def reduce_puzzle(values):
    """
    This is where our reduction strategies are applied.
    Given that they change the global state and these
    changes may allow for further application of the strategies,
    they are applied repeatedly, unless the strategies do not
    produce any more progress.
    """
    still_progressing = True
    while still_progressing:
        no_of_unsolved_values_before = sum([len(values[box]) for box in boxes])
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        no_of_unsolved_values_after  = sum([len(values[box]) for box in boxes])

        still_progressing = no_of_unsolved_values_before > no_of_unsolved_values_after

    return values

def search(values):
    """
    After the reduce_puzzle removed all values that
    could be elimiated by application of logical reasoning,
    we are now going into a brute force mode and try out
    the remaining digits.

    Trying out a digit may or may not result in a solution.
    We will attempt this in a recursive fashion and will pick
    easier targets first. This means that we look at boxes
    with fewer possible values first.
    """

    values = reduce_puzzle(values)

    if all(len(values[box]) == 1 for box in boxes):
        return values # our job here is done, we have a winner

    if values == False:
        return False

    debug(values)

    _, next_cell = min([(len(values[box]), box) for box in boxes if len(values[box]) > 1])

    assert(next_cell)

    for digit in values[next_cell]:
        new_sudoku = values.copy()
        new_sudoku = assign_value(new_sudoku, next_cell, digit)
        results = search(new_sudoku)
        if results != False:
            return results

    # This should never happen as it would mean we had a next_cell
    # but trying out all "possible" digits didn't lead to a solution

    #assert(False)

    #return False

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    print("oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")


    values = grid_values(grid) # TODO may need to take care of using assign_value during setup
    return search(values)

if __name__ == '__main__':
    diag_sudoku_grid ='''
    2.. ... ...
    ... ..6 2..
    ..1 ... .7.
    ..6 ..8 ...
    3.. .9. ..7
    ... 6.. 4..
    .4. ... 8..
    ..5 2.. ...
    ... ... ..3
    '''

    diag_sudoku_grid2 = '''
        53. .7. ...
        6.. 195 ...
        .98 ... .6.

        8.. .6. ..3
        4.. 8.3 ..1
        7.. .2. ..6

        .6. ... 28.
        ... 419 ..5
        ... .8. .79

        '''
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
