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

# Positions
triangle_pos = (-150, 0)
hexagon_pos = (150, 0)
triangle_side = 50
triangle_height = triangle_side * math.sqrt(3) / 2
hex_side = triangle_side / 2

def regular_polygon_vertices(n_edges, side_length):
    """
    Generate coordinates of a regular polygon centered at (0,0).

    Parameters
    ----------
    n_edges : int
        Number of edges (e.g., 3 for triangle, 6 for hexagon)
    side_length : float
        Length of one side

    Returns
    -------
    vertices : list of (x, y)
        List of N vertex coordinates
    """
    r = side_length / (2 * math.sin(math.pi / n_edges))
    vertices = []
    for i in range(n_edges):
        theta = 2 * math.pi * i / n_edges
        x = r * math.cos(theta)
        y = r * math.sin(theta)
        vertices.append((x, y))
    return vertices

def draw_labeled_polygon(n_sides, side_length, color, position, label):
    """
    Draw a regular polygon with a label on top.

    Parameters
    ----------
    n_sides : Number of polygon edges
    side_length : Length of one side
    color : RGB color of the polygon
    position : Screen position (x, y) of the polygon center
    label : Text label for the polygon
    """
    # Generate polygon vertices
    vertices = geometry.vertices_regular_polygon(n_sides, side_length)
    
    # Create polygon shape
    shape = stimuli.Shape(vertex_list=vertices, colour=color, position=position)

    # Draw vertical line above the polygon
    # Find maximum y-coordinate relative to center
    line_length = 50
    R = side_length / (2 * math.sin(math.pi / n_sides))
    line_start = (position[0], position[1] + R)
    line_end = (line_start[0], line_start[1] + line_length)  # 50px line
    line = stimuli.Line(start_point=line_start, end_point=line_end, line_width=3, colour=(255, 255, 255))
    
    # Draw label 20px above the line
    label_pos = (line_end[0], line_end[1] + 20)
    text = stimuli.TextLine(text=label, position=label_pos, text_size=20, text_colour=(255, 255, 255))

    shape.present(clear=False, update=False)
    line.present(clear=False, update=False)    
    text.present(clear=False, update=False)

# Start experiment
control.start(subject_id=random.randint(1, 999))

# blank text to clear window
text = stimuli.TextLine(text='', position=(0,0))
text.present(clear=True, update=False)

# Draw triangle
draw_labeled_polygon(n_sides=3, side_length=triangle_side, color=(128,0,128), position=triangle_pos, label="triangle")

# Draw hexagon
draw_labeled_polygon(n_sides=6, side_length=hex_side, color=(255,255,0), position=hexagon_pos, label="hexagon")

# blank text to update window
text = stimuli.TextLine(text='', position=(0,0))
text.present(clear=False, update=True)

# Leave it on-screen until a key is pressed
exp.keyboard.wait()

# End the current session and quit expyriment
control.end()