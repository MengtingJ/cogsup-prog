# Import the main modules of expyriment
from expyriment import design, control, stimuli
import random

# control.set_develop_mode()

# Create an object of class Experiment: This stores the global settings of your experiment & handles the data file, screen, and input devices
exp = design.Experiment(name = "Square")

# Initialize the experiment: Must be done before presenting any stimulus
control.initialize(exp)

# set square parameters
w, h  = exp.screen.size

square_size = int(w * 0.05)
w, h = w // 2, h // 2

edges = []
for x in (-w, w):
    for y in (-h, h):
        edges.append((x - square_size // 2, y - square_size // 2))

squares = [stimuli.Rectangle(size=(square_size, square_size), colour=(255,0,0), line_width=1, position=pos)
           for pos in edges]

# stim_length = width // 10
# stim_size = (stim_length, stim_length)

# edges = []
# for x in (-w, w):
#     for y in (-h, h):
#         edges.append((x//2, y//2))

# square_size = int(w * 0.05)
# square_pos_x_abs = ((w // 2) - (square_size // 2))* 0.5
# square_pos_y_abs = ((h // 2) - (square_size // 2))* 0.5

# square_1 = stimuli.Rectangle(size=(square_size, square_size), colour=(255, 0, 0), line_width=1, 
#                              position = (square_pos_x_abs, square_pos_y_abs))
# square_2 = stimuli.Rectangle(size=(square_size, square_size), colour=(255, 0, 0), line_width=1, 
#                              position = (-square_pos_x_abs, square_pos_y_abs))
# square_3 = stimuli.Rectangle(size=(square_size, square_size), colour=(255, 0, 0), line_width=1, 
#                              position = (-square_pos_x_abs, -square_pos_y_abs))
# square_4 = stimuli.Rectangle(size=(square_size, square_size), colour=(255, 0, 0), line_width=1, 
#                              position = (square_pos_x_abs, -square_pos_y_abs))

# Start running the experiment
control.start(subject_id=random.randint(1, 999))

# Present squares
for i, sq in enumerate(squares):
    sq.present(clear=(i == 0), update=(i == len(squares) - 1))

# Leave it on-screen until a key is pressed
exp.keyboard.wait()

# End the current session and quit expyriment
control.end()