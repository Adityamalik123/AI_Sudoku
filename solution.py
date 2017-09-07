assignments = []


def cross(a, b):
    return [s+t for s in a for t in b]

def diag(a,b):
    return [a[i]+b[i] for i in range(len(a))]

rows='ABCDEFGHI'
cols='123456789'

cols1='987654321'

#boxes are actually the individual square at the intersection of any row and column.

boxes= cross(rows, cols)

diagonal1= diag(rows, cols)
diagonal2= diag(rows, cols1)
#print diagonal1, diagonal2

#Now we'll find the units.. units are actually the complete rows, complete columns and complete 3x3 subsquare. so each unit consists of 9 boxes and there are 27 units in total

row_units= [cross(r, cols) for r in rows]
#print row_units[1]  will give b1, b2, ......
#print row_units will give lists in lists

diags=[diagonal1]+[diagonal2]
#print diags

column_units = [cross(rows, c) for c in cols]
#print column_units

square_units= [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
#print square_units

unitlist= row_units+ column_units+ square_units+ diags
#print unitlist
#complete unit list

#just to understand the meaning of dict----
'''
u1=dict([(1,'ABA'),(2,'ball')])
u2=dict({1:'ABA', 'A':'AD'})
u3=dict(((1,'ABA'),(2,'ball')))
print u2, u1, u3
'''

units= dict((s, [u for u in unitlist if s in u]) for s in boxes)
#print units

#peers are actually the neighbour boxes which are the row , the column and the subsquare.. for any bo there are 20 peers.. 8 row, 8 coluumn, 4 subsquare 
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)
#print peers

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    for unit in unitlist:
        #traverse the values
        value=[values[u] for u in unit]
        #after traversing calculate it...
        val_count=[value.count(v) for v in value]
        #find twin
        twins=[unit[i] for i in range(len(rows)) if len(value[i])==2 and val_count[i]==2]
        #find non-twins
        non_twin=set(unit)- set(twins)        
        for naked in twins:
            for u in values[naked]:
                for t in non_twin:
                    if len(values[t])>1:
                        assign_value(values,t,values[t].replace(u,''))

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
    values = []
    all_digits='123456789'
    for c in grid:
        if c == '.':
            values.append(all_digits)
        elif c in all_digits:
            values.append(c)
    
    assert len(values) == 81, "Input grid must be a string of length 81 (9x9)"
    return dict(zip(boxes, values))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values = assign_value(values, peer, values[peer].replace(digit,''))
    return values

def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            #print unit
            dplaces = [box for box in unit if digit in values[box]]
            '''for box in unit:
                print unit, box
                if digit in values[box]:
                    print digit, box, values[box]
            print dplaces, values[dplaces[0]]'''
            if len(dplaces) == 1:
                values= assign_value(values, dplaces[0], digit)
                #print dplaces, "ADIT", values[dplaces[0]]
    return values

def reduce_puzzle(values):
    stalled= False
    while not stalled:
        solved_values_before= len([box for box in values.keys() if len(values[box])==1])
        values=eliminate(values)
        values=only_choice(values)
        solved_values_after= len([box for box in values.keys() if len(values[box])==1])
        stalled=solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    values=reduce_puzzle(values)
    if values is False:
        return False
    if all(len(values[s])==1 for s in boxes):
        return values
    n,s=min((len(values[s]),s) for s in boxes if len(values[s])>1)
    for value in values[s]:
        new_sudoku= values.copy()
        new_sudoku = assign_value(new_sudoku, s, value)
        attempt=search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return search(grid_values(grid))


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
