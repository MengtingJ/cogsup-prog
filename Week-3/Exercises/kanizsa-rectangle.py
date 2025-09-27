# Import the main modules of expyriment
from expyriment import design, control, stimuli
from expyriment.misc.constants import C_GREY
import random

control.set_develop_mode()

def kanizsa_rectangle(aspect_ratio=1.5, rect_scale=0.25, circle_scale=0.5):
    """
    Draws a Kanizsa rectangle illusion.

    Parameters
    ----------
    aspect_ratio : aspect_ratio = Width / height ratio of the rectangle.
    rect_scale : rect_scale = rectangle height / screen width.
    circle_scale : circle_scale = circle diameter / rectangle height.
    """

    # Create an object of class Experiment: This stores the global settings of your experiment & handles the data file, screen, and input devices
    exp = design.Experiment(name = "Square", background_colour=C_GREY)

    # Initialize the experiment: Must be done before presenting any stimulus
    control.initialize(exp)

    # set square parameters
    screen_w, _  = exp.screen.size
    rect_h = int(screen_w * rect_scale)
    rect_w = int(rect_h * aspect_ratio)

    circle_r = int(rect_h * circle_scale / 2)

    positions = []
    for x in (-rect_w, rect_w):
        for y in (-rect_h, rect_h):
            positions.append((x // 2, y // 2))

    # Create circles
    circle_colors = [(255, 255, 255), (0, 0, 0)] * 2
    circles = []
    for i, (x, y) in enumerate(positions):
        circ = stimuli.Circle(circle_r, colour=circle_colors[i], position=(x, y))
        circles.append(circ)
    # Create square
    square = stimuli.Rectangle(size=(rect_w, rect_h), colour=C_GREY)

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

######################################################
###                      Main                      ###
######################################################
kanizsa_rectangle(aspect_ratio=1.5, rect_scale=0.25, circle_scale=0.5)



