#!/usr/bin/env python3

from sudoku import *
import unittest

class TestSolvers( unittest.TestCase ):

    def setUp( self ):

        # Easier to write the problems as numbers but causes
        # issues in solving as 6 != '6'
        naked_singles_problem = [8, 0, 0, 7, 3, 9, 0, 0, 6,
                                 3, 7, 0, 4, 6, 5, 0, 0, 0,
                                 0, 4, 0, 1, 8, 2, 0, 0, 9,
                                 0, 0, 0, 6, 0, 0, 0, 4, 0,
                                 0, 5, 4, 3, 0, 0, 6, 1, 0,
                                 0, 6, 0, 5, 0, 0, 0, 0, 0,
                                 4, 0, 0, 8, 5, 3, 0, 7, 0,
                                 0, 0, 0, 2, 7, 1, 0, 6, 4,
                                 1, 0, 0, 9, 4, 0, 0, 0, 2]

        hidden_singles_problem = [0, 2, 8, 0, 0, 7, 0, 0, 0,
                                  0, 1, 6, 0, 8, 3, 0, 7, 0,
                                  0, 0, 0, 0, 2, 0, 8, 5, 1,
                                  1, 3, 7, 2, 9, 0, 0, 0, 0,
                                  0, 0, 0, 7, 3, 0, 0, 0, 0,
                                  0, 0, 0, 0, 4, 6, 3, 0, 7,
                                  2, 9, 0, 0, 7, 0, 0, 0, 0,
                                  0, 0, 0, 8, 6, 0, 1, 4, 0,
                                  0, 0, 0, 3, 0, 0, 7, 0, 0]

        locked_candidates_problem_pointing = [9, 8, 4, 0, 0, 0, 0, 0, 0, 
                                              0, 0, 2, 5, 0, 0, 0, 4, 0, 
                                              0, 0, 1, 9, 0, 4, 0, 0, 2, 
                                              0, 0, 6, 0, 9, 7, 2, 3, 0, 
                                              0, 0, 3, 6, 0, 2, 0, 0, 0, 
                                              2, 0, 9, 0, 3, 5, 6, 1, 0, 
                                              1, 9, 5, 7, 6, 8, 4, 2, 3, 
                                              4, 2, 7, 3, 5, 1, 8, 9, 6, 
                                              6, 3, 8, 0, 0, 9, 7, 5, 1]

        locked_candidates_problem_claiming = [7, 6, 2, 0, 0, 8, 0, 0, 1,
                                              9, 8, 0, 0, 0, 0, 0, 0, 6,
                                              1, 5, 0, 0, 0, 0, 0, 8, 7,
                                              4, 7, 8, 0, 0, 3, 1, 6, 9,
                                              5, 2, 6, 0, 0, 9, 8, 7, 3,
                                              3, 1, 9, 8, 0, 0, 4, 2, 5,
                                              8, 3, 5, 0, 0, 1, 6, 9, 2,
                                              2, 9, 7, 6, 8, 5, 3, 1, 4,
                                              6, 4, 1, 9, 3, 2, 7, 5, 8]

        hidden_pair_problem = [0, 4, 9, 1, 3, 2, 0, 0, 0, 
                               0, 8, 1, 4, 7, 9, 0, 0, 0,
                               3, 2, 7, 6, 8, 5, 9, 1, 4,
                               0, 9, 6, 0, 5, 1, 8, 0, 0,
                               0, 7, 5, 0, 2, 8, 0, 0, 0,
                               0, 3, 8, 0, 4, 6, 0, 0, 5,
                               8, 5, 3, 2, 6, 7, 0, 0, 0,
                               7, 1, 2, 8, 9, 4, 5, 6, 3,
                               9, 6, 4, 5, 1, 3, 0, 0, 0]

        hidden_triple_problem = [2, 8, 0, 0, 0, 0, 4, 7, 3,
                                 5, 3, 4, 8, 2, 7, 1, 9, 6,
                                 0, 7, 1, 0, 3, 4, 0, 8, 0,
                                 3, 0, 0, 5, 0, 0, 0, 4, 0,
                                 0, 0, 0, 3, 4, 0, 0, 6, 0,
                                 4, 6, 0, 7, 9, 0, 3, 1, 0,
                                 0, 9, 0, 2, 0, 3, 6, 5, 4,
                                 0, 0, 3, 0, 0, 9, 8, 2, 1,
                                 0, 0, 0, 0, 8, 0, 9, 3, 7]

        self.hidden_quad_problem = [0, 3, 0, 0, 0, 0, 0, 1, 0,
                                    0, 0, 8, 0, 9, 0, 0, 0, 0,
                                    4, 0, 0, 6, 0, 8, 0, 0, 0,
                                    0, 0, 0, 5, 7, 6, 9, 4, 0,
                                    0, 0, 0, 9, 8, 3, 5, 2, 0,
                                    0, 0, 0, 1, 2, 4, 0, 0, 0,
                                    2, 7, 6, 0, 0, 5, 1, 9, 0,
                                    0, 0, 0, 7, 0, 9, 0, 0, 0,
                                    0, 9, 5, 0, 0, 0, 4, 7, 0]

        self.naked_subset_pair_problem = [7, 0, 0, 8, 4, 9, 0, 3, 0,
                                          9, 2, 8, 1, 3, 5, 0, 0, 6,
                                          4, 0, 0, 2, 6, 7, 0, 8, 9,
                                          6, 4, 2, 7, 8, 3, 9, 5, 1,
                                          3, 9, 7, 4, 5, 1, 6, 2, 8,
                                          8, 1, 5, 6, 9, 2, 3, 0, 0,
                                          2, 0, 4, 5, 1, 6, 0, 9, 3,
                                          1, 0, 0, 0, 0, 8, 0, 6, 0,
                                          5, 0, 0, 0, 0, 4, 0, 1, 0]

        self.locked_subset_pair_problem = [0, 5, 0, 1, 3, 4, 6, 0, 0,
                                           0, 9, 0, 6, 5, 2, 1, 3, 8,
                                           0, 3, 0, 8, 7, 9, 0, 4, 0,
                                           2, 1, 5, 0, 0, 3, 0, 0, 6,
                                           0, 8, 0, 2, 6, 1, 3, 5, 0,
                                           3, 6, 0, 0, 8, 5, 9, 2, 1,
                                           0, 4, 0, 0, 2, 7, 0, 1, 3,
                                           0, 7, 3, 0, 0, 6, 0, 0, 0,
                                           0, 2, 0, 3, 0, 8, 7, 6, 0]

        self.xwing_rows_problem = [0, 4, 1, 7, 2, 9, 0, 3, 0,
                                   7, 6, 9, 0, 0, 3, 4, 0, 2,
                                   0, 3, 2, 6, 4, 0, 7, 1, 9,
                                   4, 0, 3, 9, 0, 0, 1, 7, 0,
                                   6, 0, 7, 0, 0, 4, 9, 0, 3,
                                   1, 9, 5, 3, 7, 0, 0, 2, 4,
                                   2, 1, 4, 5, 6, 7, 3, 9, 8,
                                   3, 7, 6, 0, 9, 0, 5, 4, 1,
                                   9, 5, 8, 4, 3, 1, 2, 6, 7]

        self.xwing_columns_problem = [9, 8, 0, 0, 6, 2, 7, 5, 3,
                                      0, 6, 5, 0, 0, 3, 0, 0, 0,
                                      3, 2, 7, 0, 5, 0, 0, 0, 6,
                                      7, 9, 0, 0, 3, 0, 5, 0, 0,
                                      0, 5, 0, 0, 0, 9, 0, 0, 0,
                                      8, 3, 2, 0, 4, 5, 0, 0, 9,
                                      6, 7, 3, 5, 9, 1, 4, 2, 8,
                                      2, 4, 9, 0, 8, 7, 0, 0, 5,
                                      5, 1, 8, 0, 2, 0, 0, 0, 7]

        # Cast each number in the previous problems to a string.
        self.naked_singles_problem = [num for num in naked_singles_problem]
        self.hidden_singles_problem = [num for num in hidden_singles_problem]

        self.locked_candidates_problem_pointing = [num for num in locked_candidates_problem_pointing]
        self.locked_candidates_problem_claiming = [num for num in locked_candidates_problem_claiming]

        self.hidden_pair_problem = [num for num in hidden_pair_problem]
        self.hidden_triple_problem = [num for num in hidden_triple_problem]


    def test_solve_naked_singles( self ):
        """ Attempt solving a given problem using the naked singles method. """

        solve_naked_singles( self.naked_singles_problem )

        # 77th cell is known to be solvable to 6 using this method.
        self.assertEqual( 6, self.naked_singles_problem[77] )


    def test_solve_hidden_singles( self ):
        """ Attempt solving a given problem using the hidden singles method. """

        solve_hidden_singles( self.hidden_singles_problem )

        self.assertEqual( 6, self.hidden_singles_problem[21] )


    # Methods of eliminating candidates


    def test_eliminate_locked_candidates_pointing( self ):
        """ Attempt elimination of candidates using methods where if a value in one box
        has been concluded to reside in a row/column, it can't be elsewhere in same row
        or column. """

        # Get a grid of candidates,
        candidates = get_all_candidates( self.locked_candidates_problem_pointing )

        # Make value 5 is in candidate grid at given cell,
        self.assertIn( 5, candidates[24])

        # Run function to eliminate candidates,
        eliminate_locked_candidates_pointing( candidates )

        # Value 5 should no longer be present in candidates at index 24.
        self.assertNotIn( 5, candidates[24] )


    def test_eliminate_locked_candidates_claiming( self ):
        """ If in a row or column all candidates of certain digit are confined to one block,
        that candidate should be eliminated from all other cells in that block. """
        candidates = get_all_candidates( self.locked_candidates_problem_claiming )
        self.assertIn( 4, candidates[3])
        eliminate_locked_candidates_claiming( candidates )
        self.assertNotIn( 4, candidates[3] )

        
    def test_hidden_subset_pair( self ):
        candidates = get_all_candidates( self.hidden_pair_problem )
        self.assertIn( 6, candidates[44] )
        column_indices = get_column( 9, [ x for x in range(81) ] )
        hidden_subset( candidates, column_indices, 2 )
        self.assertNotIn( 6, candidates[44] )


    def test_hidden_subset_triple( self ):
        candidates = get_all_candidates( self.hidden_triple_problem )
        self.assertIn( 1, candidates[73] )
        self.assertIn( 6, candidates[74] )
        box_indices = get_box( 7, [ x for x in range(81) ] ) 
        hidden_subset( candidates, box_indices, 3 )
        self.assertNotIn( 1, candidates[73] )
        self.assertNotIn( 6, candidates[74] )


    def test_hidden_subset_quad( self ):
        candidates = get_all_candidates( self.hidden_quad_problem )

        eliminate_locked_candidates_pointing( candidates )
        eliminate_locked_candidates_claiming( candidates )

        assert {2, 4, 5, 6, 7, 8, 9} == set(candidates[8]), "We failed to get correct candidates for r1c9"

        column_indices = get_column( 9, [ x for x in range(81) ] ) 
        hidden_subset( candidates, column_indices, 4 )
        assert not {6, 7} <= set(candidates[8]), "6 & 7 are still in {}".format(candidates[8])

    def test_naked_subset_pair( self ):
        candidates = get_all_candidates( self.naked_subset_pair_problem )
        cell_index = which_index( row = 8, column = 2 )
        row_indices = get_row( 8, [ x for x in range(81) ] )

        assert {3, 7} == set( candidates[cell_index] ), "3, 7 != {}".format(candidates[cell_index])

        naked_subset( candidates, row_indices, 2 )

        assert not 3 in candidates[cell_index], "We failed to eliminate the three from r8c2."


    def test_locked_subset_pair( self ):
        candidates = get_all_candidates( self.locked_subset_pair_problem )

        assert {1, 2, 6} == set(candidates[which_index(3, 3)])
        assert {2, 7, 9} == set(candidates[which_index(1, 9)])

        # Get all indices for the sudoku grid,
        # then the important indices for row 3 and box 3
        all_indices = [ x for x in range(81) ]
        indices = list(set(get_row(3, all_indices)) | set(get_box(3, all_indices)))

        naked_subset( candidates, indices, 2 )

        assert {1, 6} == set(candidates[which_index(3, 3)])
        assert {7, 9} == set(candidates[which_index(1, 9)])

    def test_xwing_rows( self ):
        candidates = get_all_candidates( self.xwing_rows_problem )
        result = xwing(candidates)
        self.assertEqual(1, result)
        self.assertNotIn( 5, candidates[which_index(row=4, column=5)])

    def test_xwing_columns( self ):
        candidates = get_all_candidates( self.xwing_columns_problem )
        result = xwing(candidates)
        self.assertEqual(9, result)
