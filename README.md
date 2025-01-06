## Tetris Engine Demo

Tetris grid is setup per requirements (10 columns, 100rows).

*Note: # of columns is not yet configurable as that would significantly change processing logic of moves

Input is grabbed via stdin and output to stdout

The program does expect valid input given instruction
"Your program does not need to validate the file format and can assume that there will be no illegal inputs in the file",
however there is error handling; such as invalid moves doesn't crash entire line being processed.  To avoid mucking up stdout with error info, all errors are explicitly written to stderr.

For smaller inputs, graphical option exists to watch the program at work using flag -g or --graphics.
Reason for recommending smaller inputs is that for 10kb files and larger it does add overhead in processing even with updated draw that only iterates over changes cell grids to be redrawn.

Chunking for large files and large single lines was also added.

Note: Blank lines in input files are still counted as input and expected to return 0 given no input, resulting height is 0 for given line.


### Sample Usage

tetris.py < input.txt > output.txt -g  # will show gui and output to output.txt

tetris.py < input.txt --graphics       # will show gui and output to stdout / terminal
