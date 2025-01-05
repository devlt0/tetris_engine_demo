import unittest
import io
import numpy as np
from tetris import (
    Tetris_Shape,
    Tetris_Grid,
    process_batches,
    shape_Q, shape_I, shape_T, shape_Z
)

class TestTetrisGrid(unittest.TestCase):
    def setUp(self):
        self.grid = Tetris_Grid(given_max_height=10)

    def test_grid_initialization(self):
        self.assertEqual(self.grid.grid_max_height, 10)
        self.assertEqual(self.grid.cur_height, 0)
        self.assertEqual(len(self.grid.drop_history), 0)

    def test_reset_grid(self):
        self.grid.drop_piece_in("Q0")
        self.grid.reset_grid()
        self.assertEqual(self.grid.cur_height, 0)
        self.assertEqual(len(self.grid.drop_history), 0)
        np.testing.assert_array_equal(self.grid.grid, np.zeros((10, 10)))

    def test_get_shape_from_letter(self):
        q_shape = self.grid.get_shape_from_letter("Q")
        self.assertEqual(q_shape.max_height, 2)
        self.assertEqual(q_shape.max_width, 2)

        with self.assertRaises(Exception):
            self.grid.get_shape_from_letter("X")

    def test_drop_piece_basic(self):
        self.grid.drop_piece_in("Q0")
        self.assertEqual(self.grid.get_update_grid_height(), 2)
        self.assertEqual(len(self.grid.drop_history), 1)

    def test_remove_full_rows(self):
        self.grid.drop_piece_in("I0")
        self.grid.drop_piece_in("I0")
        self.grid.drop_piece_in("I4")
        self.grid.drop_piece_in("I4")
        initial_height = self.grid.get_update_grid_height()
        self.assertEqual(initial_height, 2)
        self.grid.drop_piece_in("Q8")
        self.grid.remove_full_rows()
        final_height = self.grid.get_update_grid_height()
        self.assertEqual(final_height, 0)

class TestProcessBatches(unittest.TestCase):
    def test_small_input(self):
        input_data = "Q0\nI0,I4,Q8\n"
        input_stream = io.StringIO(input_data)
        results = process_batches(input_stream, show_gui=False)
        self.assertEqual(results, [2, 1])

    def test_empty_input(self):
        input_stream = io.StringIO("")
        results = process_batches(input_stream, show_gui=False)
        self.assertEqual(results, [])


    def test_given_examples(self):
        '''
        # "Q0" -> 2
        # "I0,I4,Q8" -> 1
        # "T1,Z3,I4" -> 4
        # "Q0,I2,I6,I0,I6,I6,Q2,Q4" -> 3
        '''
        input_stream = io.StringIO("I0,I4,Q8\nq0\nQ0,I2,I6,I0,I6,I6,Q2,Q4\nT1,Z3,I4")
        results = process_batches(input_stream, show_gui=False)
        self.assertEqual(results, [1,2,3,4])

    def test_given_example_row_removed(self):
        input_stream = io.StringIO("I0,I4,Q8")
        results = process_batches(input_stream, show_gui=False)
        self.assertEqual(results, [1])

    def test_given_example_single_pc(self):
        input_stream = io.StringIO("Q8")
        results = process_batches(input_stream, show_gui=False)
        self.assertEqual(results, [2])

    def test_given_example_floating_pc(self):
        input_stream = io.StringIO("Q0,I2,I6,I0,I6,I6,Q2,Q4")
        results = process_batches(input_stream, show_gui=False)
        self.assertEqual(results, [3])

    def test_given_example_stacking(self):
        input_stream = io.StringIO("T1,Z3,I4")
        results = process_batches(input_stream, show_gui=False)
        self.assertEqual(results, [4])


    def test_invalid_moves(self):
        input_data = "X0\nQ0\n"  # X is invalid
        input_stream = io.StringIO(input_data)
        results = process_batches(input_stream, show_gui=False)
        self.assertEqual(len(results), 2)  # Should still process valid moves

    def test_partial_chunks(self):
        # Create a long input string that will span multiple chunks
        long_input = ("Q4," * 50 + "I0," * 100 + "I6,"*100) * 100
        input_stream = io.StringIO(long_input)
        results = process_batches(input_stream, show_gui=False, chunk_size=100)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], 0)

if __name__ == '__main__':
    unittest.main()