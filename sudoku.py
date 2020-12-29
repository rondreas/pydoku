import random
import pdb

DEBUG = False

def print_problem( problem ):
    """ Function to print the problem in nice way. """
    print("\n")
    for index, cell in enumerate(problem):
        print(str(cell).rjust(3), end="")
        if (index + 1) % 9 == 0:
            print("\n")


def save( path, problem ):
    """ Given a path to a file destination, save a list of 81 numbers 0 <= num <= 9. """

    with open(path, 'w') as file_out:
        file_out.write( ''.join( map(str, problem) ) )


def load( path ):
    """ Given a path to a file containing 81 numbers 0 <= num <= 9. Return a list 
    for a sudoku problem. """

    with open(path, 'r') as file_in:
        problem = file_in.read().strip()

        # Return a list where each character is casted into an integer,
        return [int(value) for value in problem]


def attempt( max_tries ):
    """ Attempt creating a sudoku problem with a limited amount of attempts. """

    count = 0
    problem = list()

    for _ in range( max_tries ):
        try:
            problem = create()
            break
        except IndexError:
            # Index errors can be expected, seeing as in create() we attempt picking a random
            # value from a list, and if a faulty sudoku was made, there won't be any values
            # in the list we're looking to pick values from.
            count += 1

    return problem


def remove_candidates( value, candidates, indices ):
    """ Remove value from candidates for given indices. """
    for index in indices:
        if value in candidates[index]:
            candidates[index].remove(value)


def create():
    """ Generate a new sudoku puzzle. """

    problem = list()

    # Generate a list for each cell with all available values.
    candidates = [ [ candidate for candidate in range(1, 10) ] for _ in range(81) ]

    # Initialize a pool of values we can choose from.
    values = [x for x in range(1,10)] * 9

    indices = [ x for x in range(81) ]

    # Iterate over each index in a sudoku problem
    for index in indices:

        # intersection of candidates and values
        value = random.choice(list(set(candidates[index]) & set(values)))

        # Remove value from pool of values,
        values.remove(value)

        problem.append(value)

        # Get indices for row, column and box, and run a set union to get all
        # unique indices we must purge value from.
        row_indices = set(get_row( which_row(index), indices))
        column_indices = set(get_column( which_column(index), indices))
        box_indices = set(get_box( which_box(index), indices))

        remove_candidates(
            value, 
            candidates, 
            list(row_indices|column_indices|box_indices)
        )

    return problem


def is_ambiguous( problem ):
    """ Check if there are more than one solution to the current problem. """

    # A problem must have at least eight digits to not be ambiguous
    if len(set(problem)) < 8:
        return True

    # Also read that if 17 values or less are set, it will be ambiguous
    if (81 - problem.count(0)) <= 17:
        return True

    return False


def reduce( solution ):
    """ Take a sudoku solution, and hide values in cells untill
    problem turns ambigous. """

    problem = [value for value in solution]

    # List indices for cells we will step through
    indices = [ x for x in range(81) ]
    random.shuffle(indices)

    for index in indices:
        tmp = problem.copy()
        tmp[index] = 0
        if is_ambiguous(tmp):
            return problem

        problem = tmp


def which_row( index ):
    """ Return the row for index. """
    return index // 9 + 1


def which_column( index ):
    """ Return the column for index. """
    return index % 9 + 1


def which_box( index ):
    """ Return the box for index. """
    return ((index % 9 // 3 + 1) + (index // 27 * 3))


def get_row( row, problem ):
    """ Return row of a sudoku problem. """
    return problem[ row * 9 - 9 : row * 9 ]


def get_column( column, problem ):
    """ Return column of a sudoku problem. """
    return problem[ column - 1 : 81 : 9 ]


def get_box( box, problem ):
    """ Return box of a sudoku problem. """

    cells = list()

    for index, cell in enumerate(problem):
        if ((index % 9 // 3 + 1) + (index // 27 * 3) ) == box:
            cells.append(cell)

    return cells


def get_candidates( index, problem ):
    """ Given the index of a cell in problem, find all candidates for 
    cell at index. """

    # Find which row, column and box index is associated with.
    row = which_row( index )
    column = which_column( index )
    box = which_box( index )

    # Create a set with values 1 through 9
    candidates = set([num for num in range( 1, 10 )])

    # Find all values in row, column and box using set union
    values = set(get_row( row, problem )) |\
             set(get_column( column, problem )) |\
             set(get_box( box, problem ))

    return list(candidates - values)


def get_all_candidates( problem ):
    """ Given a problem, returns a list with candidates for all cells. """

    candidates = [[] for _ in range(81)]

    for index, cell in enumerate(problem):
        
        # If cell in problem has a value set, continue
        if cell:
            continue
        
        candidates[index] = list(get_candidates(index, problem))

    return candidates


def solve_naked_singles( problem ):
    """ Check each cell in problem, and for any cell with only one
    possible candidate, set the cell value. """
    
    candidates = get_all_candidates( problem )

    for index, cell in enumerate(candidates):

        # If only one possible candidate, set value for problem at index.
        if len(cell) == 1:
            problem[index] = cell.pop()
            if DEBUG:
                print("Solved a naked single at r{}c{}".format(which_row(index), which_column(index)))


def hidden_singles_in_section( section_candidates ):
    """ Check a section for any value occuring only once. If any found, return
    list of values. Otherwise return empty list. """
    value_count = [sum([ candidates.count(value) for candidates in section_candidates ]) for value in range(1,10)]
    # Seeing as enumerate starts at zero, it doesn't perfectly match which number we're looking at
    return [value + 1 for value, count in enumerate(value_count) if count == 1]


def solve_hidden_singles( problem ):
    """ Iterate over each section, if there is a candidate occuring only once in all cells
    for the section, set the cell to candidate. """

    candidates = get_all_candidates( problem )

    # For each row,
    for row in range(1, 10):
        # Get candidates and indices for row,
        row_candidates = get_row( row, candidates )
        row_indices = get_row( row, [x for x in range(81)] )

        # Get list of hidden singles,
        hidden_singles = hidden_singles_in_section( row_candidates )

        # If there is a hidden single, we must iterate over each and 
        # find the value and index to set for our problem.
        for value in hidden_singles:
            for cell_candidates, index in zip(row_candidates, row_indices):

                if value in cell_candidates:
                    problem[index] = value
                    if DEBUG:
                        print("Solved a hidden single at r{}c{}".format(which_row(index), which_column(index)))

    # Do same for other sections, could use some refactoring...
    for column in range(1, 10):

        column_candidates = get_column( column, candidates )
        column_indices = get_column( column, [x for x in range(81)] )

        hidden_singles = hidden_singles_in_section( column_candidates )

        for value in hidden_singles:
            for cell_candidates, index in zip(column_candidates, column_indices):

                if value in cell_candidates:
                    problem[index] = value
                    if DEBUG:
                        print("Solved a hidden single at r{}c{}".format(which_row(index), which_column(index)))

    for box in range(1, 10):

        box_candidates = get_box( box, candidates )
        box_indices = get_box( box, [x for x in range(81)] )
        
        hidden_singles = hidden_singles_in_section( box_candidates )

        for value in hidden_singles:
            for cell_candidates, index in zip(box_candidates, box_indices):

                if value in cell_candidates:
                    problem[index] = value
                    if DEBUG: 
                        print("Solved a hidden single at r{}c{}".format(which_row(index), which_column(index)))


def find_unique_in_sublists( _list ):
    """ Given a list of lists, iterate over each list and find if
    it contains a value that can't be found in the other lists. """
    unique_values = []

    # Iterate and rotate list,
    for index in range( len(_list) ):
        rotated_list = _list[index::] + _list[:index]

        # Using sets, find values in current first, that doesn't occur in others.
        unique_values += list( recursive_flatten(rotated_list[0]) - recursive_flatten(rotated_list[1:]) )

    return unique_values


def recursive_flatten( l ):
    """ Take list l, iterate over each element that is not of type list and
    add to set s. Return set of all unique values in multidimensional list l."""

    s = set()

    for item in l:
        if isinstance( item, list ):
            s.update(recursive_flatten(item))
        else:
            s.add(item)
    
    return s


def flatten( _list ):
    """ Take a list with sublists, and return list of each element in sublists. """
    return [item for sublist in _list for item in sublist]


def _flatten( _list ):
    """ Another method, but using python set() seeing how we can
    do without duplicate values. """
    s = set()
    for sublist in _list:
        s.update(set(sublist))
    return list(s)


def eliminate_candidates( candidates ):
    """ """

    # For each box, see if candidate is in a row/column
    # If found, remove candidate from rest of row/column

    indices = [ index for index in range(81) ]

    for box in range(1, 10):

        box_candidates = get_box( box, candidates )
        box_indices = get_box( box, indices )

        # r1, r2, r3 = [box_candidates[0:3], box_candidates[3:6], box_candidates[6:9]]
        rows = [box_candidates[0:3], box_candidates[3:6], box_candidates[6:9]]

        # Get candidates for each row in box flattned,
        r1, r2, r3 = [ set(x) for x in map( flatten, rows ) ]

        unique_values = find_unique_in_sublists([box_candidates[0:3], box_candidates[3:6], box_candidates[6:9]])


        values = set()
        values.update( r1 - (r2 | r3) )
        values.update( r2 - (r1 | r3) )
        values.update( r3 - (r1 | r2) )

        # rv = list()
        # rv += list(set(flatten(r1)) - (set(flatten(r2))|set(flatten(r3))))
        # rv += list(set(flatten(r2)) - (set(flatten(r1))|set(flatten(r3))))
        # rv += list(set(flatten(r3)) - (set(flatten(r1))|set(flatten(r2))))

        # For each value found, get row, and remove from rest of row ignoring ones contained in box
        for v in unique_values:
            # Store which index value is found at
            value_indices = list()

            # index, candidate for box candidates enumerated.
            for i, c in enumerate(box_candidates):
                # If value in candidate,
                if v in c:
                    # Add index to list for where values are found.
                    value_indices.append(box_indices[i])

            # We only care about the first time we find it, seeing as all should share row number.
            row_number = which_row(value_indices[0])

            # get list of indices for row, excluding current box
            _indices = set(get_row(row_number, indices)) - set(box_indices)

            # for index
            for _i in _indices:
                # sanity check, to see that value is actually in candidate list for index in grid
                if v in candidates[_i]:
                    # Remove value from candidates seeing how we eliminated the possibility of it being there.
                    candidates[_i].remove(v)

        # c1, c2, c3 = [box_candidates[0::3], box_candidates[1::3], box_candidates[2::3]]
        # cv = list()
        # cv += list(c1 - (c2|c3))
        # cv += list(c2 - (c1|c3))
        # cv += list(c3 - (c1|c2))

        # TODO - make sets for r1 r2 r3, c1, c2, c3, then example a - (b|c)
        # how to flatten, flat_list = [item for sublist in list for item in sublist]

    # For each row/column, see if candidate is only in one
    # of the boxes, if so, remove from rest of the box but
    # for the row/column
    for row in range(1, 10):
        row_candidates = get_row( row, candidates )
