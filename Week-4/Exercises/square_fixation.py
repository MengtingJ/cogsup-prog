from expyriment import design, control, stimuli
import random

exp = design.Experiment(name="Square")

control.set_develop_mode()
control.initialize(exp)

fixation = stimuli.FixCross()
square = stimuli.Rectangle(size=(100, 100), line_width=5)

control.start(subject_id=random.randint(1, 999))

square.present(clear=True, update=False)
fixation.present(clear=False, update=True)

exp.clock.wait(500)

exp.keyboard.wait()

control.end()