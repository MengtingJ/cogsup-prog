# Import the main modules of expyriment
from expyriment import design, control, stimuli
import random
import math

control.set_develop_mode()

# Create an object of class Experiment: This stores the global settings of your experiment & handles the data file, screen, and input devices
exp = design.Experiment(name = "Launching Random Motion")

# Initialize the experiment: Must be done before presenting any stimulus
control.initialize(exp)

def launching_random_direction():
    """
    Display one launching event.
    """
    # Random angle in radians
    angle = random.uniform(0, 2*math.pi)

    # set square prameters
    square_size = 50
    radius = 300

    red_start_x = radius * math.cos(angle)
    red_start_y = radius * math.sin(angle)
    green_start_x = 0
    green_start_y = 0
    

    # Initialize two squares
    square_red = stimuli.Rectangle(size=(square_size, square_size), colour=(255, 0, 0), position = (red_start_x,red_start_y))
    square_green = stimuli.Rectangle(size=(square_size, square_size), colour=(0, 255, 0), position = (green_start_x,green_start_y))

    # Present the initial positions
    square_red.present(clear=False, update=False)
    square_green.present(clear=False, update=True)

    # Calculate total distance for the red square (until touching the green one)
    total_distance = abs(radius - square_size / max(abs(math.sin(angle)), abs(math.cos(angle)))) # the distance square should move         
    delay = 10       # delay between each step

    # min_center_distance = (square_size / 2.0) * (abs(math.cos(angle)) + abs(math.sin(angle)))
    # total_distance = radius - min_center_distance

    # Move the green square
    green_steps = 90  # number of step
    step_size = total_distance / green_steps
    green_dx = math.cos(angle) * step_size    # number of pixel for each step
    green_dy = math.sin(angle) * step_size    # number of pixel for each step

    green_x = green_start_x
    green_y = green_start_y
    for _ in range(green_steps):
        green_x += green_dx
        green_y += green_dy
        square_green.reposition((int(green_x), int(green_y)))
        square_green.present(clear=True, update=False)
        square_red.present(clear=False, update=True)
        exp.clock.wait(delay)
        
    red_steps = green_steps
    red_dx = green_dx
    red_dy = green_dy

    # Move the red square
    red_x = red_start_x
    red_y = red_start_y
    for _ in range(red_steps):
        red_x += red_dx
        red_y += red_dy
        square_red.reposition((int(red_x), int(red_y)))
        square_red.present(clear=True, update=False)
        square_green.present(clear=False, update=True)
        exp.clock.wait(delay)

    message = stimuli.TextLine(text="Press any key to continue", text_size=30, text_colour=(255, 165, 0))
    message.present()
    exp.keyboard.wait()

# Start running the experiment
control.start(subject_id=random.randint(1, 999))

# Show the four conditions
launching_random_direction()
launching_random_direction()
launching_random_direction()

# Leave it on-screen until a key is pressed
exp.keyboard.wait()

# End the current session and quit expyriment
control.end()