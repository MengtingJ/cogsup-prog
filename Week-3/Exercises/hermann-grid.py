# hermann-grid.py

from expyriment import design, control, stimuli
from expyriment.misc.constants import C_BLACK, C_WHITE, C_GREY
import random

control.set_develop_mode()

def hermann_grid(square_size=100, square_colour=C_BLACK, spacing=20, rows=5, cols=5,
        background_colour=C_WHITE):
    """
    Draws a Hermann grid illusion.

    Parameters
    ----------
    square_size : size of each square (pixel).
    square_colour : colour of squares.
    spacing : space between squares (pixel).
    rows : Number of rows.
    cols : Number of columns.
    background_colour : background colour.
    """

    exp = design.Experiment(name="Hermann Grid", background_colour=background_colour)
    control.initialize(exp)
    square_size = int(square_size)

    screen_w, screen_h = exp.screen.size

    # Grid total size
    grid_w = cols * square_size + (cols - 1) * spacing
    grid_h = rows * square_size + (rows - 1) * spacing

    # Top-left corner square center coordinate
    start_x = int(-grid_w // 2 + square_size // 2)
    start_y = int(-grid_h // 2 + square_size // 2)

    # Create squares
    squares = []
    for i in range(rows):
        for j in range(cols):
            x = start_x + j * (square_size + spacing)
            y = start_y + i * (square_size + spacing)
            sq = stimuli.Rectangle(size=(square_size, square_size),
                                   colour=square_colour,
                                   position=(x, y))
            squares.append(sq)

    # Start experiment
    control.start(subject_id=random.randint(1, 999))

    # Present all squares
    for k, sq in enumerate(squares):
        sq.present(clear=(k == 0), update=(k == len(squares) - 1))

    # Wait for key
    exp.keyboard.wait()

    # End
    control.end()

hermann_grid(square_size=80, square_colour=C_BLACK, spacing=20, rows=5, cols=5,
        background_colour=C_WHITE)