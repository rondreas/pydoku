import random
from itertools import (
    combinations,
    chain,
)
from collections import Counter
from collections.abc import Iterable
from typing import (
    List,
)

DEBUG = False

def print_problem( problem: List[int] ):
    """ Function to print the problem in nice way. """
    print("\n")
    for index, cell in enumerate(problem):
        print(str(cell).rjust(3), end="")
        if (index + 1) % 9 == 0:
            print("\n")


def save( path: str, problem: List[int] ):
    """ Given a path to a file destination, save a list of 81 numbers 0 <= num <= 9. """

    with open(path, 'w') as file_out:
        file_out.write( ''.join( map(str, problem) ) )


def load( path: str ) -> List[int]:
    """ Given a path to a file containing 81 numbers 0 <= num <= 9. Return a list 
    for a sudoku problem. """

    with open(path, 'r') as file_in:
        problem = file_in.read().strip()

        # Return a list where each character is casted into an integer,
        return [int(value) for value in problem]


def attempt( max_tries: int ) -> List[int]:
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


def remove_candidates( value: int, candidates: List[List[int]], indices: Iterable[int] ) -> int:
    """ Remove value from candidates for given indices. """
    count = 0
    for index in indices:
        if value in candidates[index]:
            count += 1
            candidates[index].remove(value)

            if DEBUG:
                print("Removing {} from candidates in r{}c{}".format(value, which_row( index ), which_column( index )))

    return count


def create() -> List[int]:
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

    # FIXME: not really sure this function works

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

    # TODO: this reduce solutions too much making the sudoku ambiguous

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

    return problem


def which_row( index ):
    """ Return the row for index. """
    return index // 9 + 1


def which_column( index ):
    """ Return the column for index. """
    return index % 9 + 1


def which_box( index ):
    """ Return the box for index. """
    return ((index % 9 // 3 + 1) + (index // 27 * 3))


def which_index( row, column ):
    """ Given a row, column return the index. """
    return row * 9 + column - 10


def get_row( row: int, problem: List ) -> List:
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


def get_all_candidates( problem: List[int] ) -> List[List[int]]:
    """ Given a problem, returns a list with candidates for all cells. """

    candidates = [[] for _ in range(81)]

    for index, cell in enumerate(problem):
        
        # If cell in problem has a value set, continue
        if cell:
            continue
        
        candidates[index] = list(get_candidates(index, problem))

    return candidates


def solve_naked_singles( problem: List[int], candidates=[] ) -> int:
    """ Check each cell in problem, and for any cell with only one
    possible candidate, set the cell value. 
    
    :param list problem: sudoku problem represented by a list with 81 numbers 0..9
    :param list candidates: list of 81 sublists which store candidates for values in cells

    """

    solved_cells = 0
    
    if not candidates:
        candidates = get_all_candidates( problem )

    for index, cell in enumerate(candidates):

        # If only one possible candidate, set value for problem at index.
        if len(cell) == 1:
            problem[index] = cell.pop()
            solved_cells += 1
            if DEBUG:
                print("Solved a naked single at r{}c{}".format(which_row(index), which_column(index)))

    return solved_cells


def hidden_singles_in_section( section_candidates ):
    """ Check a section for any value occuring only once. If any found, return
    list of values. Otherwise return empty list. """
    value_count = [sum([ candidates.count(value) for candidates in section_candidates ]) for value in range(1,10)]
    # Seeing as enumerate starts at zero, it doesn't perfectly match which number we're looking at
    return [value + 1 for value, count in enumerate(value_count) if count == 1]


def solve_hidden_singles( problem: List[int], candidates: List[List[int]] =[] ) -> int:
    """ Iterate over each section, if there is a candidate occuring only once in all cells
    for the section, set the cell to candidate. """

    solved_cells = 0

    if not candidates:
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
                    solved_cells += 1
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
                    solved_cells += 1
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
                    solved_cells += 1
                    if DEBUG: 
                        print("Solved a hidden single at r{}c{}".format(which_row(index), which_column(index)))

    return solved_cells


def eliminate_locked_candidates_pointing( candidates: List[List[int]] = [] ) -> int:
    """ Eliminate candidates unique to row/column inside box, from rest of the row/column 

    We will be juggling two sets of candidates,
      - candidates in the overlap
      - candidates outside the overlap in box

    When one is found to be in the overlap, but not rest of the box, we can
    remove this candidate from the rest of the overlapping section,

    """

    count = 0

    indices = [ index for index in range(81) ]

    for box in range(1, 10):

        box_indices = get_box( box, indices )

        # Get overlapping rows,
        overlapping_rows = { which_row(index) for index in box_indices }

        # For each row overlapping with current box,
        for row in overlapping_rows:

            # get indices for row, 
            row_indices = get_row( row, indices )

            # get indices where row & box overlaps, 
            box_row_indices = set( box_indices ) & set( row_indices )

            # get indices unique to box,
            box_indices_excluding_row = set( box_indices ) - set( row_indices )

            # get indices unique to row,
            row_indices_excluding_box = set( row_indices ) - set( box_indices )

            # Get candidates in the overlap,
            box_row_candidates = { candidate for index in box_row_indices for candidate in candidates[index] }

            # Get candidates outside of overlap,
            box_excluding_row_candidates = { candidate for index in box_indices_excluding_row for candidate in candidates[index] }

            # Get which candidates are in overlap but not in the rest of box,
            for candidate in (box_row_candidates - box_excluding_row_candidates):
                # and remove these from the non-overlapping section
                count += remove_candidates( candidate, candidates, row_indices_excluding_box )

        # Same as above but going over columns this time,
        overlapping_columns = { which_column(index) for index in box_indices }

        for column in overlapping_columns:

            column_indices = get_column( column, indices )

            box_column_indices = set( box_indices ) & set( column_indices )
            box_indices_excluding_column = set( box_indices ) - set( column_indices )
            column_indices_excluding_box = set( column_indices ) - set( box_indices )

            box_column_candidates = { candidate for index in box_column_indices for candidate in candidates[index] }
            box_excluding_column_candidates = { candidate for index in box_indices_excluding_column for candidate in candidates[index] }

            for candidate in (box_column_candidates - box_excluding_column_candidates):
                count += remove_candidates( candidate, candidates, column_indices_excluding_box )

    return count


def eliminate_locked_candidates_claiming( candidates ) -> int:

    count = 0

    indices = [ index for index in range(81) ]

    for row in range(1, 10):
        row_indices = get_row( row, indices )
        row_candidates = get_row( row, candidates )

        overlapping_boxes = { which_box( index ) for index in row_indices }

        for box in overlapping_boxes:

            box_indices = get_box( box, indices )

            overlapping_indices = set( row_indices ) & set( box_indices )
            box_exlusive = set( box_indices ) - set( row_indices )
            row_exlusive = set( row_indices ) - set( box_indices )

            overlapping_candidates = { candidate for index in overlapping_indices for candidate in candidates[index] }
            row_exlusive_candidates = { candidate for index in row_exlusive for candidate in candidates[index] }

            for candidate in ( overlapping_candidates - row_exlusive_candidates ):
                count += remove_candidates( candidate, candidates, box_exlusive )

    for column in range(1, 10):
        column_indices = get_column( column, indices )
        column_candidates = get_column( column, candidates )

        overlapping_boxes = { which_box( index ) for index in column_indices }

        for box in overlapping_boxes:

            box_indices = get_box( box, indices )

            overlapping_indices = set( column_indices ) & set( box_indices )
            box_exlusive = set( box_indices ) - set( column_indices )
            column_exlusive = set( column_indices ) - set( box_indices )

            overlapping_candidates = { candidate for index in overlapping_indices for candidate in candidates[index] }
            column_exlusive_candidates = { candidate for index in column_exlusive for candidate in candidates[index] }

            for candidate in ( overlapping_candidates - column_exlusive_candidates ):
                count += remove_candidates( candidate, candidates, box_exlusive )

    return count


def hidden_subset( candidates, section_indices, depth ) -> int:

    count = 0

    # remove indices without candidates, ie ones with set value,
    candidate_indices = [ index for index in section_indices if candidates[index] ]

    # iterate over all combinations of candidate cells in section
    for subset_indices in combinations(candidate_indices, depth ):

        # get indices for all cells but for the subset
        other_indices = set(candidate_indices) - set(subset_indices)

        # all candidates not in the subset of the section
        other_candidates = { candidate for index in other_indices for candidate in candidates[index] }

        # all candidates in the current subset of section
        subset_candidates = { candidate for index in subset_indices for candidate in candidates[index] }

        subset = subset_candidates - other_candidates
        
        if len(subset) == depth:
            for value in { x for x in range(1, 10) } - subset:
                count += remove_candidates( value, candidates, subset_indices )

    return count


def naked_subset( candidates, section_indices, depth ) -> int:

    count = 0
    
    # remove indices without candidates, ie ones with set value,
    candidate_indices = [ index for index in section_indices if candidates[index] ]

    # iterate over all combinations of candidate cells in section
    for subset_indices in combinations(candidate_indices, depth):

        # get indices for all cells but for the subset
        other_indices = set(candidate_indices) - set(subset_indices)

        # all candidates in the current subset of section
        subset_candidates = { candidate for index in subset_indices for candidate in candidates[index] }

        if len(subset_candidates) == depth:
            for value in subset_candidates:
                count += remove_candidates( value, candidates, other_indices )

    return count


def xwing(candidates: List[List[int]]) -> int:
    count = 0
    all_indices = [x for x in range(81)]

    # first try xwing on rows,
    for i in range(1, 9):
        row = get_row(i, candidates)
        counter = Counter(chain(*row))

        if not 2 in counter.values():
            continue

        columns = {k: [] for k,v in counter.items() if v == 2}
        for fish in columns.keys():
            # find which columns this fish number belongs to,
            for column, cell in enumerate(row):
                if fish not in cell:
                    continue
                columns[fish].append(column+1)

        for j in range(i+1, 10):
            second_row = get_row(j, candidates)
            counter = Counter(chain(*second_row))

            _columns = {k: [] for k,v in counter.items() if v == 2}

            shared_fishes = set(columns.keys()).intersection(set(_columns.keys()))
            if not shared_fishes:
                # print(f"Row {i} and {j} does not share any fishes.")
                continue

            for fish in _columns.keys():
                for column, cell in enumerate(second_row, 1):
                    if fish not in cell:
                        continue
                    _columns[fish].append(column)

            for fish in shared_fishes:
                if not columns.get(fish) == _columns.get(fish):
                    continue

                c = columns.get(fish)
                # get the indices for the columns, but exclude the indices for the rows
                indices = (set(get_column(c[0], all_indices)) | set(get_column(c[1], all_indices))) - (set(get_row(i, all_indices)) | set(get_row(j, all_indices)))
                count += remove_candidates(fish, candidates, indices)

    # same but using columns as base sets,
    for i in range(1, 9):
        first_column = get_column(i, candidates)
        counter = Counter(chain(*first_column))

        if not 2 in counter.values():
            continue  # skip this row as it does not contain any candidate locked to two cells,

        rows = {k: [] for k,v in counter.items() if v == 2}
        for fish in rows.keys():
            # find which columns this fish number belongs to,
            for row, cell in enumerate(first_column):
                if fish not in cell:
                    continue
                rows[fish].append(row+1)

        for j in range(i+1, 10):
            second_column = get_column(j, candidates)
            counter = Counter(chain(*second_column))

            _rows = {k: [] for k,v in counter.items() if v == 2}

            shared_fishes = set(rows.keys()).intersection(set(_rows.keys()))
            if not shared_fishes:
                continue

            for fish in _rows.keys():
                for row, cell in enumerate(second_column, 1):
                    if fish not in cell:
                        continue
                    _rows[fish].append(row)

            for fish in shared_fishes:
                if not rows.get(fish) == _rows.get(fish):
                    continue

                r = rows.get(fish)

                # get the indices for the columns, but exclude the indices for the rows
                indices = (set(get_row(r[0], all_indices)) | set(get_row(r[1], all_indices))) - (set(get_column(i, all_indices)) | set(get_column(j, all_indices)))
                count += remove_candidates(fish, candidates, indices)

    return count


def solve_problem( problem: List[int] ) -> List[int]:
    _problem = [ cell for cell in problem ]
    indices = [x for x in range(81)]
    candidates = get_all_candidates(_problem)

    candidate_count = sum([len(x) for x in candidates])

    # while the problem is not solved,
    # continue any time we solve or eliminate candidates,
    while 0 in _problem:
        q = eliminate_locked_candidates_pointing(candidates)
        if q:
            continue

        if eliminate_locked_candidates_claiming(candidates):
            # print("Locked claiming")
            continue

        _x = 0
        for i in range(9):
            row = get_row(i, indices)
            for j in range(2, 5):
                _x += hidden_subset( candidates, row, j )
                _x += naked_subset( candidates, row, j )

            col = get_row(i, indices)
            for j in range(2, 5):
                _x += hidden_subset( candidates, col, j )
                _x += naked_subset( candidates, col, j )

            box = get_row(i, indices)
            for j in range(2, 5):
                _x += hidden_subset( candidates, box, j )
                _x += naked_subset( candidates, box, j )

        if _x:
            # print(f"{_x} Subset values")
            continue

        if xwing(candidates):
            print("Removed candidates using xwing!")
            continue

        if solve_naked_singles(_problem, candidates):
            candidates = get_all_candidates( _problem )
            continue

        if solve_hidden_singles(_problem, candidates):
            candidates = get_all_candidates( _problem )
            continue

        # we have tried all our elimination techniques and can't seem to eliminate any further values,
        print("Got stuck trying to solve problem")
        break

    return _problem


if __name__ == "__main__":
    # load and attempt to solve a problem,
    problem = load("foo.txt")
    # problem = load("x.txt")
    print_problem(problem)
    solution = solve_problem(problem)
    print_problem(solution)
