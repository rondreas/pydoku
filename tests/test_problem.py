#!/usr/bin/env python3

from itertools import chain
from sudoku import *
import unittest

class TestProblem( unittest.TestCase ):

    def setUp( self ):
        self.problem = [x for x in range(81)]

    ###################
    # which_row tests #
    ###################

    def test_get_row_of_index_0( self ):
        self.assertEqual( 1, which_row( 0 ) )

    def test_get_row_of_index_13( self ):
        self.assertEqual( 2, which_row( 13 ) )

    def test_get_row_of_index_26( self ):
        self.assertEqual( 3, which_row( 26 ) )

    def test_get_row_of_index_30( self ):
        self.assertEqual( 4, which_row( 30 ) )

    def test_get_row_of_index_42( self ):
        self.assertEqual( 5, which_row( 42 ) )

    def test_get_row_of_index_46( self ):
        self.assertEqual( 6, which_row( 46 ) )

    def test_get_row_of_index_59( self ):
        self.assertEqual( 7, which_row( 59 ) )

    def test_get_row_of_index_64( self ):
        self.assertEqual( 8, which_row( 64 ) )

    def test_get_row_of_index_79( self ):
        self.assertEqual( 9, which_row( 79 ) )

    ######################
    # which_column tests #
    ######################

    def test_get_column_of_index_72( self ):
        self.assertEqual( 1, which_column( 0 ) )

    def test_get_column_of_index_72( self ):
        self.assertEqual( 2, which_column( 1 ) )

    def test_get_column_of_index_72( self ):
        self.assertEqual( 3, which_column( 2 ) )

    def test_get_column_of_index_72( self ):
        self.assertEqual( 4, which_column( 3 ) )

    def test_get_column_of_index_72( self ):
        self.assertEqual( 5, which_column( 4 ) )

    def test_get_column_of_index_72( self ):
        self.assertEqual( 6, which_column( 5 ) )

    def test_get_column_of_index_72( self ):
        self.assertEqual( 7, which_column( 6 ) )

    def test_get_column_of_index_72( self ):
        self.assertEqual( 8, which_column( 7 ) )

    def test_get_column_of_index_72( self ):
        self.assertEqual( 9, which_column( 8 ) )

    ###################
    # which_box tests #
    ###################

    def test_get_box_of_index_19( self ):
        self.assertEqual( 1, which_box( 19 ) )

    def test_get_box_of_index_4( self ):
        self.assertEqual( 2, which_box( 4 ) )

    def test_get_box_of_index_17( self ):
        self.assertEqual( 3, which_box( 17 ) )

    def test_get_box_of_index_27( self ):
        self.assertEqual( 4, which_box( 27 ) )

    def test_get_box_of_index_32( self ):
        self.assertEqual( 5, which_box( 32 ) )

    def test_get_box_of_index_51( self ):
        self.assertEqual( 6, which_box( 51 ) )

    def test_get_box_of_index_70( self ):
        self.assertEqual( 7, which_box( 70 ) )

    def test_get_box_of_index_70( self ):
        self.assertEqual( 8, which_box( 70 ) )

    def test_get_box_of_index_70( self ):
        self.assertEqual( 9, which_box( 70 ) )

    #####################
    # which_index tests #
    #####################

    def test_get_which_index_row_1_column_1( self ):
        self.assertEqual( 0, which_index( 1, 1 ) )

    def test_get_which_index_row_2_column_1( self ):
        self.assertEqual( 9, which_index( 2, 1 ) )

    def test_get_which_index_row_3_column_9( self ):
        self.assertEqual( 26, which_index( 3, 9 ) )

    def test_get_which_index_row_9_column_9( self ):
        self.assertEqual( 80, which_index( 9, 9 ) )

    #################
    # get_row tests #
    #################

    def test_get_first_row( self ):
        self.assertEqual( [0, 1, 2, 3, 4, 5, 6, 7, 8], get_row( 1, self.problem ) )

    def test_get_second_row( self ):
        self.assertEqual( [9, 10, 11, 12, 13, 14, 15, 16, 17], get_row( 2, self.problem ) )

    def test_get_third_row( self ):
        self.assertEqual( [18, 19, 20, 21, 22, 23, 24, 25, 26], get_row( 3, self.problem ) )

    def test_get_fourth_row( self ):
        self.assertEqual( [27, 28, 29, 30, 31, 32, 33, 34, 35], get_row( 4, self.problem ) )

    def test_get_fifth_row( self ):
        self.assertEqual( [36, 37, 38, 39, 40, 41, 42, 43, 44], get_row( 5, self.problem ) )

    def test_get_sixth_row( self ):
        self.assertEqual( [45, 46, 47, 48, 49, 50, 51, 52, 53], get_row( 6, self.problem ) )

    def test_get_seventh_row( self ):
        self.assertEqual( [54, 55, 56, 57, 58, 59, 60, 61, 62], get_row( 7, self.problem ) )

    def test_get_eighth_row( self ):
        self.assertEqual( [63, 64, 65, 66, 67, 68, 69, 70, 71], get_row( 8, self.problem ) )

    def test_get_ninth_row( self ):
        self.assertEqual( [72, 73, 74, 75, 76, 77, 78, 79, 80], get_row( 9, self.problem ) )

    ####################
    # get_column tests #
    ####################

    def test_get_first_column( self ):
        self.assertEqual( [0, 9, 18, 27, 36, 45, 54, 63, 72], get_column( 1, self.problem ) ) 

    def test_get_second_column( self ):
        self.assertEqual( [1, 10, 19, 28, 37, 46, 55, 64, 73], get_column( 2, self.problem ) ) 

    def test_get_third_column( self ):
        self.assertEqual( [2, 11, 20, 29, 38, 47, 56, 65, 74], get_column( 3, self.problem ) ) 

    def test_get_fourth_column( self ):
        self.assertEqual( [3, 12, 21, 30, 39, 48, 57, 66, 75], get_column( 4, self.problem ) ) 

    def test_get_fifth_column( self ):
        self.assertEqual( [4, 13, 22, 31, 40, 49, 58, 67, 76], get_column( 5, self.problem ) ) 

    def test_get_sixth_column( self ):
        self.assertEqual( [5, 14, 23, 32, 41, 50, 59, 68, 77], get_column( 6, self.problem ) ) 

    def test_get_seventh_column( self ):
        self.assertEqual( [6, 15, 24, 33, 42, 51, 60, 69, 78], get_column( 7, self.problem ) ) 

    def test_get_eighth_column( self ):
        self.assertEqual( [7, 16, 25, 34, 43, 52, 61, 70, 79], get_column( 8, self.problem ) ) 

    def test_get_ninth_column( self ):
        self.assertEqual( [8, 17, 26, 35, 44, 53, 62, 71, 80], get_column( 9, self.problem ) ) 

    ####################
    # get_box tests #
    ####################

    def test_get_first_box( self ):
        self.assertEqual( [0, 1, 2, 9, 10, 11, 18, 19, 20], get_box( 1, self.problem ) ) 

    def test_get_second_box( self ):
        self.assertEqual( [3, 4, 5, 12, 13, 14, 21, 22, 23], get_box( 2, self.problem ) ) 

    def test_get_third_box( self ):
        self.assertEqual( [6, 7, 8, 15, 16, 17, 24, 25, 26], get_box( 3, self.problem ) ) 

    def test_get_fourth_box( self ):
        self.assertEqual( [27, 28, 29, 36, 37, 38, 45, 46, 47], get_box( 4, self.problem ) ) 

    def test_get_fifth_box( self ):
        self.assertEqual( [30, 31, 32, 39, 40, 41, 48, 49, 50], get_box( 5, self.problem ) ) 

    def test_get_sixth_box( self ):
        self.assertEqual( [33, 34, 35, 42, 43, 44, 51, 52, 53], get_box( 6, self.problem ) ) 

    def test_get_seventh_box( self ):
        self.assertEqual( [54, 55, 56, 63, 64, 65, 72, 73, 74], get_box( 7, self.problem ) ) 

    def test_get_eighth_box( self ):
        self.assertEqual( [57, 58, 59, 66, 67, 68, 75, 76, 77], get_box( 8, self.problem ) ) 

    def test_get_ninth_box( self ):
        self.assertEqual( [60, 61, 62, 69, 70, 71, 78, 79, 80], get_box( 9, self.problem ) ) 

    ####################
    ####################

    def test_remove_candidates( self ):
        candidates = [
            [],
            [1,2,6,8,9],
            [4,6,7,8,9],
        ]
        remove_candidates( 8, candidates, [0,1,2] )
        self.assertFalse(8 in chain(*candidates))
