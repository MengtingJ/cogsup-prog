from expyriment import design, control, stimuli
from expyriment.misc.constants import K_SPACE, C_WHITE, C_BLACK
import random

exp = design.Experiment(name="Ternus Illusion", background_colour=C_WHITE)
control.set_develop_mode()
control.initialize(exp)

def load(stims):
    """Preload all stimuli."""
    for stim in stims:
        stim.preload()

def present_for(stims, frames=12):
    """Present stimuli for given number of frames (~200 ms default), clearing screen each frame."""
    t_ms = frames * 16.67
    t0 = exp.clock.time
    for _ in range(int(frames)):
        exp.screen.clear() 
        for stim in stims:
            stim.present(clear=False, update=False)
        exp.screen.update()
    draw_time = exp.clock.time - t0
    exp.clock.wait(max(0, t_ms - draw_time))

def make_circles(radius, positions, colors=None):
    """Create circles at given positions and optionally add color tags."""
    circles = []
    for i, pos in enumerate(positions):
        # circles
        c = stimuli.Circle(radius=radius, position=pos, colour=C_BLACK)

        if colors is not None:
            tag_pos = (0, 0) 
            tag = stimuli.Circle(radius=5, colour=colors[i], position=tag_pos)
            tag.plot(c)

        circles.append(c)

    # preload
    load(circles)
    return circles

def run_trial(radius=30, isi_frames=1, color_tags=False):
    """
    Run a single Ternus trial.
    motion_type: "element" or "group"
    """
    positions = [(-150,0), (-50,0), (50,0), (150,0)]
    tag_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)] if color_tags else None
    colors = [(255,0,0),    # red
          (0,255,0),    # green
          (0,0,255),    # blue
          (255,255,0)]  # yellow

    # create circles
    circles = make_circles(radius, positions, colors=tag_colors)
    display_frames=30
    
    # 1st frame：left 3 circles
    frame1 = [circles[0], circles[1], circles[2]]
    # 2nd frame：right 3 circles
    frame2 = [circles[1], circles[2], circles[3]]

    while True:
        # 1st frame
        present_for(frame1, frames=display_frames)

        # ISI
        if isi_frames > 0:
            exp.screen.clear()
            exp.screen.update()            
            exp.clock.wait(isi_frames * 16.67)

        # 2nd frame
        present_for(frame2, frames=display_frames)

        # ISI 
        if isi_frames > 0:
            exp.screen.clear()
            exp.screen.update()
            exp.clock.wait(isi_frames * 16.67)

        # if SPACE end trial
        if exp.keyboard.check(K_SPACE):
            break


trials = [
    {"radius":30, "isi_frames":0, "color_tags":False},
    {"radius":30, "isi_frames":5, "color_tags":False},
    {"radius":30, "isi_frames":5, "color_tags":True}
]

control.start(subject_id=random.randint(1, 999))
for trial in trials:
    run_trial(**trial)
control.end()
