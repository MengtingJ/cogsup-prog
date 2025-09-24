# Import the main modules of expyriment
from expyriment import design, control, stimuli
import random

control.set_develop_mode()

# Create an object of class Experiment: This stores the global settings of your experiment & handles the data file, screen, and input devices
exp = design.Experiment(name = "Display-edges")

# Initialize the experiment: Must be done before presenting any stimulus
control.initialize(exp)

# Create a fixation cross (color, size, and position will take on default values)
fixation = stimuli.FixCross() 
square = stimuli.Rectangle(size=(50, 50), colour=(0, 0, 255))

# Start running the experiment

control.start(subject_id=random.randint(1, 999))

# Present the fixation cross and square
square.present(clear=True, update=False)
fixation.present(clear=False, update=True)
exp.clock.wait(500)

# Remove the cross and replace it with a circle
square.present(clear=True, update=True)

# Leave it on-screen until a key is pressed
exp.keyboard.wait()

# End the current session and quit expyriment
control.end()