'''
Exercise6.1: Coding the Solution

Time to code the final solution! Finish the code in the function search, 
which will create a tree of possibilities and traverse it using DFS until it finds a solution for the sudoku puzzle.
'''
#1. utils.py ----------------------------
#1.1 define rows: 
rows = 'ABCDEFGHI'

#1.2 define cols:
cols = '123456789'

#1.3 cross(a,b) helper function to create boxes, row_units, column_units, square_units, unitlist
def cross(a, b):
    return [s+t for s in a for t in b]

#1.4 create boxes
boxes = cross(rows, cols)

#1.5 create row_units
row_units = [cross(r, cols) for r in rows]

#1.6 create column_units
column_units = [cross(rows, c) for c in cols]

#1.7 create square_units for 9x9 squares
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

#1.8 create unitlist for all units
unitlist = row_units + column_units + square_units

#1.9 create peers of a unit from all units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

#1.10 display function receiving "values" as a dictionary and display a 9x9 suduku board
def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def grid_values(grid):
    """Convert grid string into {<box>: <value>} dict with '123456789' value for empties.

    Args:
        grid: Sudoku grid in string form, 81 characters long
    Returns:
        Sudoku grid in dictionary form:
        - keys: Box labels, e.g. 'A1'
        - values: Value in corresponding box, e.g. '8', or '123456789' if it is empty.
    """
    
    dic = {}
    c_index = 0
    for row in rows:
        for col in cols:
            if(grid[c_index] == '.'):
                dic[row+col] = '123456789'
            else:
                dic[row+col] = grid[c_index]
            c_index = c_index+1   
    return dic

#2. function.py ----------------------------
# 2.1 implement eliminate(values)
# from utils import *
def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    for current_box in values:
        current_value = values[current_box]
        new_value = current_value

        if(len(current_value) == 1):
            for peer in peers[current_box]:
                values[peer] = values[peer].replace( current_value,'')

    return values

def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    for current_box in values:
        for group in units[current_box]:
            current_value = values[current_box]
            for key in group:
                if(len(values[key]) > 1 ):
                    for i in range(0, len(values[key])):
                        current_value = current_value.replace( values[key][i], '' )
            if(len(current_value) == 1):
                values[current_box] = current_value
    return values

def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    # use these to check for stucking
    last_unsolved_box = 0
    unsolved_box = count_unsolved_box(values)

    while unsolved_box != 0 and unsolved_box != last_unsolved_box:
        last_unsolved_box = unsolved_box
        values = eliminate(values)        
        values = only_choice(values)
        unsolved_box = count_unsolved_box(values)

    # If at some point, there is a box with no available values, return False.
    if( check_for_empty_box(values) ):
        return False

    return values

def check_for_empty_box(values):
    for key, value in values.items():
        if(len(value) == 0):
            return True
    return False

def count_unsolved_box(values):
    unsolved_box = 0
    for key, value in values.items():
        if(len(value)>1):
            unsolved_box = unsolved_box + 1
    return unsolved_box

def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    # Search and Choose one of the unfilled squares with the fewest possibilities
    # Now use recursion to solve each one of the resulting sudokus, 
    # and if one returns a value (not False), return that answer!
    import copy

    if(reduce_puzzle(values) == False):
        return False

    if(count_unsolved_box(values) == 0):
        return values

    key = find_fewest_box(values)

    for value in values[key]:
        values[key] = value
        try_result = search(copy.deepcopy(values))
        if( try_result != False):
            return try_result
    
    return False

def find_fewest_box(values):
    for min in range (2,9):
        for key in values:
            if( len(values[key]) == min):
                return key
        
#3. Test utils.py ----------------------------  
grid_easy = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
grid_hard = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
values = grid_values(grid_hard)
print("The original Sudoku board is **********************************************")
display(values)

#4. Test function.py ----------------------------  
new_values = search(values)
print("\n")
print("After applying Depth First Search Algorithm *****************")
display(new_values)