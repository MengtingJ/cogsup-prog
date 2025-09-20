# Import the main modules of expyriment
from expyriment import design, control, stimuli
import random

control.set_develop_mode()

# Create an object of class Experiment: This stores the global settings of your experiment & handles the data file, screen, and input devices
exp = design.Experiment(name = "Launching")

# Initialize the experiment: Must be done before presenting any stimulus
control.initialize(exp)

# set square prameters
square_size = 50
red_start_x = -400
green_start_x = 0
square_red = stimuli.Rectangle(size=(square_size, square_size), colour=(255, 0, 0), position = (red_start_x,0))
square_green = stimuli.Rectangle(size=(square_size, square_size), colour=(0, 255, 0), position = (green_start_x,0))

# Start running the experiment

control.start(subject_id=random.randint(1, 999))

# Present the fixation cross and square
square_red.present(clear=True, update=False)
square_green.present(clear=False, update=True)


total_distance = abs(green_start_x-red_start_x-square_size)  # the distance square should move
steps = 50                      # number of step
dx = int(total_distance / steps)     # number of pixel for each step
delay = 10                      # delay between each step

# red square moves
for _ in range(steps):
    square_red.move((dx,0))        
    square_red.present(clear=True, update=False)  
    square_green.present(clear=False, update=True) 
    exp.clock.wait(delay)

# green square moves
for _ in range(steps):
    square_green.move((dx,0))        
    square_green.present(clear=True, update=False)  
    square_red.present(clear=False, update=True) 
    exp.clock.wait(delay)

# Leave it on-screen until a key is pressed
exp.keyboard.wait()

# End the current session and quit expyriment
control.end()