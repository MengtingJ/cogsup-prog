from expyriment import design, control, stimuli
from expyriment.misc.constants import C_WHITE, C_BLACK, K_r, K_b, K_g, K_o
import random
import itertools

# Helper for obtaining derangements in python
def derangements(lst):
    ders = []
    for perm in itertools.permutations(lst):
        if all(original != perm[idx] for idx, original in enumerate(lst)):
            ders.append(perm)
    return ders

# WORDS = ["red", "blue", "green", "orange"]
# PERMS = derangements(WORDS)
# print(PERMS)
# print(f"Totally {len(PERMS)} derangements。")


""" Constants """
COLOR_KEYS = {
    K_r: 'red',
    K_b: 'blue',
    K_g: 'green',
    K_o: 'orange'
}
KEYS = [K_r, K_b, K_g, K_o]
TRIAL_TYPES = ["match", "mismatch"]
WORDS = ["red", "blue", "green", "orange"]
COLORS_RGB = {
    "red": (255, 0, 0),
    "blue": (0, 0, 255),
    "green": (0, 255, 0),
    "orange": (255, 165, 0)
}


N_BLOCKS = 8
N_TRIALS_IN_BLOCK = 16

INSTR_START = """
In this task, you have to indicate what is the color of word's font.
Press R for red, B for blue, G for green, and O for orange\n
Press SPACE to continue.
"""
INSTR_MID = """You have finished half of the experiment, well done! Your task will be the same.\nTake a break then press SPACE to move on to the second half."""
INSTR_END = """Well done!\nPress SPACE to quit the experiment."""

FEEDBACK_CORRECT = """ ^ _ ^ """
FEEDBACK_INCORRECT = """ (⊙ _ ⊙ ) """

WORDS = ["red", "blue", "green", "orange"]
PERMS = derangements(WORDS)
COLORS = ["red", "blue", "green", "orange"]

# Choose one derangement for mismatch mapping
perm = random.choice(PERMS)
dict_mismatch = dict(zip(WORDS, perm))
print("Chosen mismatch mapping:", dict_mismatch)

""" Helper functions """
def load(stims):
    for stim in stims:
        stim.preload()

def timed_draw(*stims):
    t0 = exp.clock.time
    exp.screen.clear()
    for stim in stims:
        stim.present(clear=False, update=False)
    exp.screen.update()
    t1 = exp.clock.time
    return t1 - t0

def present_for(*stims, t=1000):
    dt = timed_draw(*stims)
    exp.clock.wait(t - dt)

def present_instructions(text):
    instructions = stimuli.TextScreen(text=text, text_justification=0, heading="Instructions")
    instructions.present()
    exp.keyboard.wait()

""" Global settings """
exp = design.Experiment(name="Balanced Stroop (Color Naming)", background_colour=C_WHITE, foreground_colour=C_BLACK)
exp.add_data_variable_names(['block_cnt', 'trial_cnt', 'trial_type', 'word', 'color', 'RT', 'key', 'correct'])
exp.add_bws_factor("assignment", derangements(COLORS))

control.set_develop_mode()
control.initialize(exp)

""" Stimuli """
fixation = stimuli.FixCross()
fixation.preload()

stims = {w: {c: stimuli.TextLine(w, text_colour=COLORS_RGB[c]) for c in COLORS_RGB} for w in COLORS_RGB}

load([stims[w][c] for w in COLORS for c in COLORS])

feedback_correct = stimuli.TextLine(FEEDBACK_CORRECT, text_size=40)
feedback_incorrect = stimuli.TextLine(FEEDBACK_INCORRECT, text_size=40)
load([feedback_correct, feedback_incorrect])
stims = {w: {c: stimuli.TextLine(w, text_colour=COLORS_RGB[c]) for c in COLORS_RGB} for w in COLORS_RGB}
for w in WORDS:
    for c in COLORS_RGB:
        stims[w][c].preload()

""" Experiment """
def run_trial(block_id, trial_id, trial_type, word, color):
    stim = stims[word][color]
    present_for(fixation, t=500)
    stim.present()
    key, rt = exp.keyboard.wait(KEYS)
    correct = COLOR_KEYS[key] == color
    exp.data.add([block_id, trial_id, trial_type, word, color, rt, COLOR_KEYS[key], correct])
    feedback = feedback_correct if correct else feedback_incorrect
    present_for(feedback, t=1000)

control.start(subject_id=random.randint(1, 999))

present_instructions(INSTR_START)

for block_id in range(1, N_BLOCKS + 1):
    for trial_id in range(1, N_TRIALS_IN_BLOCK + 1):
        trial_type = random.choice(TRIAL_TYPES)
        word = random.choice(COLORS)
        if trial_type == "match":
            color = word
        else:
            color = random.choice([c for c in COLORS if c != word])

        run_trial(block_id, trial_id, trial_type, word, color)

    if block_id != N_BLOCKS:
        present_instructions(INSTR_MID)
present_instructions(INSTR_END)

control.end()