import numpy as np
import tkinter as tk
import sys
from traceback import print_exc



class Tetris_Shape:
    def __init__(self, representation_2d):
        self.repr_2d    = representation_2d   # starting from bottom left, going right, up left, then right
        self.np_repr    = np.array(self.repr_2d)
        self.max_height, self.max_width = self.np_repr.shape



shape_Q = Tetris_Shape(representation_2d=[[1,1], [1,1]])
shape_Z = Tetris_Shape(representation_2d=[[0,1,1], [1,1,0]])
shape_S = Tetris_Shape(representation_2d=[[1,1,0], [0,1,1]])
shape_T = Tetris_Shape(representation_2d=[[0,1,0], [1,1,1]])
shape_I = Tetris_Shape(representation_2d=[[1,1,1,1]])
shape_L = Tetris_Shape(representation_2d=[[1,1], [1,0], [1,0]])
shape_J = Tetris_Shape(representation_2d=[[1,1], [0,1], [0,1]])

# grid max width 10, max height 100
# if row full, like tetris, should be removed- but only when row is completely full
# do not need to account for shape rotation [though would be nice option to have]
# input list of comma separated values where letter followed by number,
#  letter represents shape [q,z,s,t,i,l,j] and # represents left most col of shape [0->9]


# 'Your program does not need to validate the file format and can assume that there will be no illegal inputs in the file"
# large file or rather specifically large line sizes require different handling
#  need to maintain state until line is complete, could be as simple as choosing when to reset and keeping old grid status to build on,
#   then just cycle thru chunks as needed, when end of line, chk height of grid, reset, repeat

class Tetris_Grid:
    def __init__(self, given_max_height=100):
        self.grid_max_height = given_max_height
        self.grid = np.zeros((given_max_height, 10), dtype=int)

        self.cur_height = 0
        self.drop_history = []
        self.valid_shapes = ["Q", "Z", "S", "T", "I", "J", "L"]
        self.valid_range_min = 0
        self.valid_range_max = 9

    def reset_grid(self):
        self.grid = np.zeros((self.grid_max_height, 10), dtype=int)
        self.cur_height = 0
        self.drop_history = []

    def get_update_grid_height(self):
        temp_height = 0
        for row in range(self.grid_max_height - 1, -1, -1):
            if np.any(self.grid[row, :] == 1):
                temp_height = row + 1
                break

        self.cur_height = temp_height

        return self.cur_height


    def get_shape_from_letter(self, given_letter:str="")->Tetris_Shape:
        matching_shape = None
        formatted_letter = given_letter.strip().upper()
        shape_map = {
            "Q": shape_Q,
            "Z": shape_Z,
            "S": shape_S,
            "T": shape_T,
            "I": shape_I,
            "J": shape_J,
            "L": shape_L
        }
        matching_shape = shape_map.get(formatted_letter, None)
        if matching_shape is None:
            raise Exception(f"Invalid letter shape provided {given_letter} formatted to {formatted_letter}, valid selection is {self.valid_shapes}")
        return matching_shape


    def drop_piece_in(self, raw_shape_leftcol: str = ''):

        raw_letter = raw_shape_leftcol[0]
        int_leftcol = int(raw_shape_leftcol[1])
        self.drop_history.append( (raw_letter, int_leftcol) )
        letter_shape = self.get_shape_from_letter(given_letter=raw_letter)

        # NumPy's broadcasting to which row piece goes to
        is_falling = False
        drop_row = None

        for row in range(self.grid_max_height - letter_shape.max_height, -1, -1):
            try:
                if np.all((self.grid[row:row + letter_shape.max_height, int_leftcol:int_leftcol + letter_shape.max_width] + letter_shape.np_repr) <= 1):
                    drop_row = row
                    is_falling = True
                elif is_falling:
                    break
            except ValueError as val_err:
                print(val_err)
                print_exc()

        # NumPy array slicing and addition to place piece
        if drop_row is not None:
            self.grid[drop_row:drop_row + letter_shape.max_height, int_leftcol:int_leftcol + letter_shape.max_width] += letter_shape.np_repr


    def remove_full_rows(self):
        rows_to_remove = np.where(np.all(self.grid == 1, axis=1))[0]

        if rows_to_remove.size > 0:
            num_rows_to_remove = rows_to_remove.size
            self.grid = np.delete(self.grid, rows_to_remove, axis=0)

            empty_rows = np.zeros((num_rows_to_remove, self.grid.shape[1]), dtype=int)
            self.grid = np.vstack((self.grid, empty_rows))


    def process_line_of_moves(self, raw_cs_text_line:str=''):
        list_of_moves = []
        resulting_height = -2
        try:
            list_of_moves = raw_cs_text_line.split(',')
            list_of_moves = [move.strip().upper() for move in list_of_moves]
            list_of_moves = [move for move in list_of_moves if move not in ("", None)] # just in case of spare comma doesn't crash program

            for cur_move in list_of_moves:
                if len(cur_move) == 2:
                    self.drop_piece_in(cur_move)
                    self.remove_full_rows()
                else:
                    print(f"Invalid move found {cur_move}")
                #print(self.get_update_grid_height())
            resulting_height = self.get_update_grid_height()
        except Exception as e:
            print(e)
            print_exc()
        return resulting_height



#$ ./tetris < input.txt > output.txt
'''
if __name__ == "__main__":
    testx = Tetris_Grid(10)
    print(testx.process_line_of_moves("q0"))        # -> 2
    # expect 2 get 2

    testy = Tetris_Grid(10)
    print(testy.process_line_of_moves("I0,I4,Q8"))  # -> 1
    # expect 1 get 2

    testz = Tetris_Grid(10)
    print(testz.process_line_of_moves("T1,Z3,I4"))  # -> 4
    # expect 4 get 3

    testa = Tetris_Grid(10)
    print(testa.process_line_of_moves("Q0,I2,I6,I0,I6,I6,Q2,Q4")) # -> 3
    # pc doesn't fall, expect 3

    # "Q0" -> 2
    # "I0,I4,Q8" -> 1
    # "T1,Z3,I4" -> 4
    # "Q0,I2,I6,I0,I6,I6,Q2,Q4" -> 3
    # I0
    # I6
    # Q4
'''


class TetrisGUI:
    def __init__(self, master, grid):
        self.master = master
        master.title("Tetris Simulation")
        self.grid = grid
        self.cell_size = 5
        self.create_widgets()
        self.prev_grid_state = np.zeros_like(self.grid.grid)
        self.draw_blank_grid()

    def create_widgets(self):
        self.canvas = tk.Canvas(self.master, width=self.grid.grid.shape[1] * self.cell_size,
                                height=self.grid.grid.shape[0] * self.cell_size, bg="white")
        self.canvas.pack()
        self.height_label = tk.Label(self.master, text="Height: 0")
        self.height_label.pack()

    def draw_blank_grid(self):
        for row in range(self.grid.grid.shape[0] - 1, -1, -1):
            for col in range(self.grid.grid.shape[1]):
                x1 = col * self.cell_size
                y1 = (self.grid.grid.shape[0] - 1 - row) * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="gray")

    def draw_grid(self):
        # improved draw method to only iterate over changed cells vs entire grid each time
        changed_cells = np.where(self.grid.grid != self.prev_grid_state)
        for row, col in zip(*changed_cells):
            x1 = col * self.cell_size
            y1 = (self.grid.grid.shape[0] - 1 - row) * self.cell_size
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size

            if self.grid.grid[row, col] == 1:
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="blue", outline="")
            else:
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="gray")

        self.height_label.config(text=f"Height: {self.grid.get_update_grid_height()}")
        self.prev_grid_state = self.grid.grid.copy()


    def process_move_list_str(self, tk_handle, raw_cs_text_line:str='', tk_refresh_rate_ms=100):
        list_of_moves = []
        resulting_height = -3
        try:
            list_of_moves = raw_cs_text_line.split(',')
            list_of_moves = [move.strip().upper() for move in list_of_moves]
            list_of_moves = [move for move in list_of_moves if move not in ("", None)] # just in case of spare comma doesn't crash program

            for cur_move in list_of_moves:
                self.grid.drop_piece_in(cur_move)
                self.draw_grid()
                tk_handle.update()
                tk_handle.after(tk_refresh_rate_ms)

                self.grid.remove_full_rows()
                self.draw_grid()
                tk_handle.update()
                tk_handle.after(tk_refresh_rate_ms)
            resulting_height = self.grid.get_update_grid_height()
        except Exception as e:
            print(e)
            print_exc()

        return resulting_height


one_kilobyte = 1024
ten_kb       = 10 * one_kilobyte
one_megabyte = 1024 * one_kilobyte
ten_mb       = 10 * one_megabyte

def process_batches(input_source, show_gui=False, chunk_size=ten_kb, grid_max_height=100, def_refresh_rate_ms=100):
    current_batch = []
    results = []

    if isinstance(input_source, str):
        file = open(input_source, 'r')
    else:
        file = input_source

    try:
        tetris_eng = Tetris_Grid(given_max_height=grid_max_height)
        partial_line_res = None
        partial_line = None
        root_win = None
        gui = None
        leftover_partial_move = None

        if show_gui:
            root_win = tk.Tk()
            gui = TetrisGUI(root_win, tetris_eng)
            root_win.update()


        for chunk in iter(lambda: file.read(chunk_size), ''):
            if leftover_partial_move is not None:
                chunk = leftover_partial_move + chunk
            temp_lines = chunk.split("\n") # python handle os conv for newline
            num_temp_lines = len(temp_lines)
            if num_temp_lines == 1:
                partial_line = temp_lines[0]

            elif num_temp_lines > 1:
                # ew double nested loop, y but for chunking, still ew
                for cur_line in temp_lines[:-1]:
                    if show_gui:
                        cur_res_ht = gui.process_move_list_str(root_win, cur_line, tk_refresh_rate_ms=def_refresh_rate_ms)
                        root_win.update()
                        root_win.after(def_refresh_rate_ms)

                    else:
                        cur_res_ht = tetris_eng.process_line_of_moves( raw_cs_text_line = cur_line )

                    results.append(cur_res_ht)
                    tetris_eng.reset_grid()

                    if show_gui:
                        gui.draw_grid()
                        root_win.update()
                        root_win.after(def_refresh_rate_ms)

                partial_line = temp_lines[-1] # -1 to grab last line

            if partial_line:
                if ',' in partial_line and not (partial_line[-1] == ',' or ( len(partial_line)>2 and partial_line[-3] == ',') ):
                    # meaning with valid input would have ,x EOC # end of chunk
                    leftover_partial_move = partial_line[-1:]
                    partial_line = partial_line[:-1]
                else:
                    leftover_partial_move = None

                if show_gui:
                    partial_line_res = gui.process_move_list_str(root_win, partial_line, tk_refresh_rate_ms=def_refresh_rate_ms)
                else:
                    partial_line_res = tetris_eng.process_line_of_moves( raw_cs_text_line = partial_line )
                # since reset needs to be explicitly called-
                # this will result in processing partial lines until chunks of file are done
        if partial_line_res is not None:
            results.append(partial_line_res)
            tetris_eng.reset_grid()

    except Exception as e:
        print(e)
        print_exc()

    finally:
        if isinstance(input_source, str):
            file.close()

        if show_gui:
            root_win.quit()
            root_win.destroy()

    return results



if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="Process input & output files system stdin < and stdout >, if no file prov")
    parser.add_argument("-g", "--graphics", help="see tkinter graphic of tetris in action",
                        action="store_true")

    args = parser.parse_args()


    results = process_batches(sys.stdin, show_gui=args.graphics) #"input_longone.txt")#sys.stdin, show_gui=args.graphics)
    #print(results)
    with sys.stdout as out_handle:
        for cur_res in results:
            out_handle.write(f"{cur_res}\n")
