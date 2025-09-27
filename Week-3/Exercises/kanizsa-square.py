# Import the main modules of expyriment
from expyriment import design, control, stimuli
from expyriment.misc.constants import C_GREY
import random

control.set_develop_mode()

# Create an object of class Experiment: This stores the global settings of your experiment & handles the data file, screen, and input devices
exp = design.Experiment(name = "Square", background_colour=C_GREY)

# Initialize the experiment: Must be done before presenting any stimulus
control.initialize(exp)

# set square parameters
screen_w, screen_h  = exp.screen.size

square_size = int(screen_w * 0.25)
circle_r = int(square_size * 0.5 / 2)

half_side = square_size // 2


positions = []
for x in (-half_side, half_side):
    for y in (-half_side, half_side):
        positions.append((x, y))

# Create circles
circle_colors = [(255, 255, 255), (0, 0, 0)] * 2
circles = []
for i, (x, y) in enumerate(positions):
    circ = stimuli.Circle(circle_r, colour=circle_colors[i], position=(x, y))
    circles.append(circ)
# Create square
square = stimuli.Rectangle(size=(square_size, square_size), colour=C_GREY)

# Start running the experiment
control.start(subject_id=random.randint(1, 999))

# Present circles and square
for i, circ in enumerate(circles):
    circ.present(clear = (i == 0), update = False)
square.present(clear = False, update = True)

# Leave it on-screen until a key is pressed
exp.keyboard.wait()

# End the current session and quit expyriment
control.end()