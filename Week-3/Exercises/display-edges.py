# Import the main modules of expyriment
from expyriment import design, control, stimuli
import random

control.set_develop_mode()

# Create an object of class Experiment: This stores the global settings of your experiment & handles the data file, screen, and input devices
exp = design.Experiment(name = "Square")

# Initialize the experiment: Must be done before presenting any stimulus
control.initialize(exp)

# set square parameters
screen_w, screen_h  = exp.screen.size

stim_size = int(screen_w * 0.05)
w = screen_w // 2 - stim_size // 2
h = screen_h // 2 - stim_size // 2

edges = []
for x in (-w, w):
    for y in (-h, h):
        edges.append((x, y))

squares = [stimuli.Rectangle(size=(stim_size, stim_size), colour=(255,0,0), line_width=1, position=pos)
           for pos in edges]

# Start running the experiment
control.start(subject_id=random.randint(1, 999))

# Present the fixation cross and square
for i, sq in enumerate(squares):
    sq.present(clear=(i == 0), update=(i == len(squares) - 1))

# Leave it on-screen until a key is pressed
exp.keyboard.wait()

# End the current session and quit expyriment
control.end()