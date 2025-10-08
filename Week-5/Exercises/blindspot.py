from expyriment import design, control, stimuli
import random
from expyriment.misc.constants import C_WHITE, C_BLACK
from expyriment.misc.constants import K_LEFT, K_RIGHT, K_UP, K_DOWN, K_1, K_2, K_SPACE


""" Global settings """
exp = design.Experiment(name="Blindspot", background_colour=C_WHITE, foreground_colour=C_BLACK)
control.set_develop_mode()
control.initialize(exp)
# exp.keyboard.set_key_repeat(True)

""" Stimuli """
def make_circle(r, pos=(0,0)):
    c = stimuli.Circle(r, position=pos, anti_aliasing=10)
    c.preload()
    return c

""" Experiment """
def run_trial(side = 'left'):
    """ side: 'left' or 'right', 
            the position of circle relative to the fixation.
    """
    
    # --- Instruction ---
    instructions = f"""
    Blind Spot Task

    Please cover your {side.upper()} eye and fixate on the cross on the screen.
    
    Adjust the circle using:
      - Arrow keys to move
      - 1 to make smaller
      - 2 to make larger
    
    Press SPACE to continue.
    """
    text_screen = stimuli.TextScreen("Instructions", instructions)
    text_screen.present()
    exp.keyboard.wait([K_SPACE]) 

    cross_pos = [300, 0] if side.lower() == "left" else [-300, 0]
    fixation = stimuli.FixCross(size=(150, 150), line_width=10, position=cross_pos)
    fixation.preload()

    radius = 50
    pos = [0, 0]
    circle = make_circle(radius)

    # the change in position for each press
    d_pos = 15
    # the change in size for each press
    d_size = 5

    while True:
        exp.screen.clear()
        fixation.present(clear=False, update=False)
        circle.present(clear=False, update=True)

        key = exp.keyboard.check([K_LEFT, K_RIGHT, K_UP, K_DOWN, K_1, K_2, K_SPACE])
        # print("Pressed:", key)

        # --- Movement ---
        if key == K_LEFT:
            pos[0] -= d_pos
        elif key == K_RIGHT:
            pos[0] += d_pos
        elif key == K_UP:
            pos[1] += d_pos
        elif key == K_DOWN:
            pos[1] -= d_pos

        # --- Size adjustment ---
        elif key == K_1:
            radius = max(d_size, radius - d_size)
        elif key == K_2:
            radius += d_size

        # --- Update circle ---
        circle = make_circle(radius, pos)

        # --- Finish trial ---
        if key == K_SPACE:
            break

control.start(subject_id=random.randint(1, 999))

run_trial(side = 'left')
run_trial(side = 'right')
    
control.end()