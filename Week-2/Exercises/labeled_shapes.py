# Import the main modules of expyriment
from expyriment import design, control, stimuli
import random
import math
from expyriment.misc import geometry

control.set_develop_mode()

# Create an object of class Experiment: This stores the global settings of your experiment & handles the data file, screen, and input devices
exp = design.Experiment(name = "Labeled Shapes")

# Initialize the experiment: Must be done before presenting any stimulus
control.initialize(exp)

# set square prameters
# Parameters
triangle_side = 50
triangle_height = triangle_side * math.sqrt(3) / 2
hex_side = triangle_side / 2
line_length = 50
line_width = 3
line_gap = 15
label_offset = 20

# Positions
triangle_pos = (-150, 0)
hexagon_pos = (150, 0)

# Colors
triangle_color = (128, 0, 128)  # purple
hex_color = (255, 255, 0)      # yellow

line_color = (255, 255, 255)   # white
text_color = (255, 165, 0)


# create triangle
triangle_vertices = geometry.vertices_regular_polygon(3, triangle_side) 
triangle = stimuli.Shape(vertex_list=triangle_vertices, colour=triangle_color, position=triangle_pos)
# create hexagon
hex_vertices = geometry.vertices_regular_polygon(6, hex_side)
hexagon = stimuli.Shape(vertex_list=hex_vertices, colour=hex_color, position=hexagon_pos)


# Start running the experiment
control.start(subject_id=random.randint(1, 999))

# Create vertical lines
R = triangle_side / (2 * math.sin(math.pi / 3))
triangle_line_start = (triangle_pos[0], triangle_pos[1] + R)
triangle_line_end = (triangle_line_start[0], triangle_line_start[1] + line_length)  # 50px line
line_triangle_x = triangle_pos[0] 
line_triangle_y_start = triangle_pos[1] + max(y for x, y in hex_vertices)
line_triangle = stimuli.Line(start_point=triangle_line_start,
                             end_point=triangle_line_end,
                             line_width=line_width,
                             colour=(255,255,255))

R = hex_side / (2 * math.sin(math.pi / 6))
hex_line_start = (hexagon_pos[0], hexagon_pos[1] + R)
hex_line_end = (hex_line_start[0], hex_line_start[1] + line_length)  # 50px line

line_hexagon = stimuli.Line(start_point=hex_line_start,
                            end_point=hex_line_end,
                            line_width=line_width, colour=line_color)

# Create labels
label_triangle = stimuli.TextLine(text="triangle", text_size=20, position=(triangle_line_end[0], triangle_line_end[1]+label_offset), text_colour=text_color)
label_hexagon = stimuli.TextLine(text="hexagon", text_size=20, position=(hex_line_end[0], hex_line_end[1]+label_offset), text_colour=text_color)

# Present the fixation cross and square
triangle.present(clear=True, update=False)
hexagon.present(clear=False, update=False)
line_triangle.present(clear=False, update=False)
line_hexagon.present(clear=False, update=False)
label_triangle.present(clear=False, update=False)
label_hexagon.present(clear=False, update=True)

# Leave it on-screen until a key is pressed
exp.keyboard.wait()

# End the current session and quit expyriment
control.end()