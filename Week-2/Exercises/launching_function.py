# Import the main modules of expyriment
from expyriment import design, control, stimuli
import random

control.set_develop_mode()

# Create an object of class Experiment: This stores the global settings of your experiment & handles the data file, screen, and input devices
exp = design.Experiment(name = "Launching Function")

# Initialize the experiment: Must be done before presenting any stimulus
control.initialize(exp)

def show_launching(temporal_gap_ms=0, spatial_gap_px=0, speed_ratio=1.0, title=""):
    """
    Display one launching event.
    Parameters:
        temporal_gap_ms: delay (in ms) between collision and green square movement
        spatial_gap_px: initial spatial gap (in px) between the two squares
        speed_ratio: green square speed / red square speed
    """
    # set square prameters
    square_size = 50
    red_start_x = -400
    green_strat_x = spatial_gap_px

    # Initialize two squares
    square_red = stimuli.Rectangle(size=(square_size, square_size), colour=(255, 0, 0), position = (red_start_x,0))
    square_green = stimuli.Rectangle(size=(square_size, square_size), colour=(0, 255, 0), position = (green_strat_x,0))

    # Create a title at the top of the screen
    title_text = stimuli.TextLine(text=title, text_size=30, position=(0, 150), text_colour=(255, 165, 0))

    # Present initial display (title + squares)
    title_text.present(clear=True, update=False)
    square_red.present(clear=False, update=False)
    square_green.present(clear=False, update=True)

    # Present the initial positions
    square_red.present(clear=False, update=False)
    square_green.present(clear=False, update=True)

    # Calculate total distance for the red square (until touching the green one)
    total_distance = abs(0 - red_start_x - square_size) # the distance square should move         
    red_steps = 50  # number of step
    red_dx = int(total_distance / red_steps)    # number of pixel for each step
    delay = 10       # delay between each step

    # Move the red square
    for _ in range(red_steps):
        square_red.move((red_dx, 0))
        title_text.present(clear=True, update=False)
        square_red.present(clear=False, update=False)
        square_green.present(clear=False, update=True)
        exp.clock.wait(delay)

    # Wait after collision if temporal gap is set
    if temporal_gap_ms > 0:
        exp.clock.wait(temporal_gap_ms)

    # Move the green square
    green_steps = int(red_steps / speed_ratio)
    green_dx = int(total_distance / green_steps)

    for _ in range(green_steps):
        square_green.move((green_dx, 0))
        title_text.present(clear=True, update=False)
        square_green.present(clear=False, update=False)
        square_red.present(clear=False, update=True)
        exp.clock.wait(delay)

    message = stimuli.TextLine(text="Press any key to continue", text_size=30, text_colour=(255, 165, 0))
    message.present()
    exp.keyboard.wait()


# Start running the experiment
control.start(subject_id=random.randint(1, 999))

# Show the four conditions
show_launching(temporal_gap_ms=0,   spatial_gap_px=0,   speed_ratio=1.0, title="Michottean Launching")
show_launching(temporal_gap_ms=500, spatial_gap_px=0,   speed_ratio=1.0, title="Temporal Gap")
show_launching(temporal_gap_ms=0,   spatial_gap_px=100, speed_ratio=1.0, title="Spatial Gap")
show_launching(temporal_gap_ms=0,   spatial_gap_px=0,   speed_ratio=3.0, title="Triggering")

# Leave it on-screen until a key is pressed
exp.keyboard.wait()

# End the current session and quit expyriment
control.end()