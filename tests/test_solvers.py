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


        # Cast each number in the previous problems to a string.
        self.naked_singles_problem = [num for num in naked_singles_problem]
        self.hidden_singles_problem = [num for num in hidden_singles_problem]
        self.locked_candidates_problem_pointing = [num for num in locked_candidates_problem_pointing]
        self.locked_candidates_problem_claiming = [num for num in locked_candidates_problem_claiming]

    def test_solve_naked_singles( self ):
        """ Attempt solving a given problem using the naked singles method. """

        solve_naked_singles( self.naked_singles_problem )

        # 77th cell is known to be solvable to 6 using this method.
        self.assertEqual( 6, self.naked_singles_problem[77] )

    def test_solve_hidden_singles( self ):
        """ Attempt solving a given problem using the hidden singles method. """

        solve_hidden_singles( self.hidden_singles_problem )

        self.assertEqual( 6, self.hidden_singles_problem[21] )

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

