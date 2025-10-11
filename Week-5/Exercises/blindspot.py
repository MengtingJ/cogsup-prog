from expyriment import design, control, stimuli
import random
from expyriment.misc.constants import C_WHITE, C_BLACK
from expyriment.misc.constants import K_LEFT, K_RIGHT, K_UP, K_DOWN, K_1, K_2, K_SPACE


""" Global settings """
exp = design.Experiment(name="Blindspot", background_colour=C_WHITE, foreground_colour=C_BLACK)
control.set_develop_mode()
control.initialize(exp)

exp.add_data_variable_names(['eye', 'key', 'final_radius', 'final_x', 'final_y'])

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

    cross_pos = [0, 0]
    fixation = stimuli.FixCross(size=(150, 150), line_width=10, position=cross_pos)
    fixation.preload()

    radius = 50
    pos = [-300, 0] if side.lower() == "left" else [300, 0]
    circle = make_circle(radius, pos = pos)

    # the change in position for each press
    d_pos = 15
    # the change in size for each press
    d_size = 5

    key_map = {
        K_LEFT: 'LEFT',
        K_RIGHT: 'RIGHT',
        K_UP: 'UP',
        K_DOWN: 'DOWN',
        K_1: 'larger',
        K_2: 'smaller',
        K_SPACE: 'quit'
    }

    while True:
        exp.screen.clear()
        fixation.present(clear=False, update=False)
        circle.present(clear=False, update=True)

        key = exp.keyboard.check([K_LEFT, K_RIGHT, K_UP, K_DOWN, K_1, K_2, K_SPACE])
        # print("Pressed:", key)
        
        if key:
            exp.data.add([side.upper(), key_map.get(key, str(key)), radius, pos[0], pos[1]])
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
                # record data
                print("CSV file will be saved in:", exp.data.fullpath)
                break

control.start(subject_id=random.randint(1, 999))

run_trial(side = 'left')
run_trial(side = 'right')
    
control.end()


# ---------------------------------------
# print collected data
# ---------------------------------------
from expyriment.misc.data_preprocessing import read_datafile
import pandas as pd

# read .xpd 
data, variables, subject_info, comments = read_datafile(f"data/blindspot_{exp.subject}.xpd")
df = pd.DataFrame(data, columns=variables)
print(df)