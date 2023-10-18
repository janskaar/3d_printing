import numpy as np

wall_thickness = 2.
wall_height = 30.

bottom_x = 156
bottom_y = 156
rect_center = (bottom_x / 2, bottom_y / 2)
d = 10.                # minimal diameter
D = 2 / np.sqrt(3) * d # maximal diameter
t = 2.                 # thickness
s = 0.5 * d * 2 / np.sqrt(3) 
n_x = 16
n_y = 14

y_start_even = 0#y_start_odd + 0.5 * d + 0.5 * t
y_start_odd = y_start_even + 0.5 * d + 0.5 * t
x_start = 0#-0.5 * s

xshift = t / np.sin(np.pi / 3)
xshift = (t * (1 - 0.5 * np.sin(np.pi/6))) / np.sin(np.pi/3)
hex_cs = []
for i in range(n_x):
    for j in range(n_y):
        if i % 2 == 0:
            y_start = y_start_even
        else:
            y_start = y_start_odd
        xpos = x_start + i * (0.5 * (D + s) + xshift)
        ypos = y_start + j * (d + t)
        hex_cs.append((xpos, ypos))

bottom_plate = cq.Workplane()\
        .rect(bottom_x, bottom_y, centered=False)\
        .extrude(4.)\

hex = cq.Workplane()\
        .pushPoints(hex_cs)\
        .polygon(6, D, circumscribed=False)\
        .extrude(4.)

bottom_plate = bottom_plate.cut(hex)
walls = cq.Workplane(origin=(-wall_thickness, -wall_thickness, 0))\
        .rect(bottom_x + 2 * wall_thickness, bottom_y + 2 * wall_thickness, centered=False)\
        .workplane(origin=(0,0,0))\
        .rect(bottom_x, bottom_y, centered=False)\
        .extrude(wall_height)\


glass_thickness = 5

# connector = cq.Workplane()\
#         .polygon(6,D+t)\
#         .extrude(2)
# 
# cut = cq.Workplane(origin=(0,-D,0))\
#         .rect(-2*D, 2*D, centered=False)\
#         .extrude(2)
# 
# connector = connector.cut(cut)

a = 0.5*t - wall_thickness - glass_thickness - 0.5 * d - 5
b = 0.5*t - wall_thickness - glass_thickness - 0.5 * d
c = 0.5*t - wall_thickness - 0.5 * d
hook = cq.Workplane("YZ")\
        .move(-1,0)\
        .lineTo(-1, 100)\
        .lineTo(a, 100)\
        .lineTo(a, 80)\
        .lineTo(b, 80)\
        .lineTo(b, 95)\
        .lineTo(c, 95)\
        .lineTo(c,wall_height+5)\
        .lineTo(0.5 * (t - d), wall_height+5)\
        .lineTo(0.5 * (t - d), -4.1 - 5)\
        .lineTo(20, -4.1 - 5)\
        .lineTo(20, -4.1)\
        .lineTo(-1, -4.1)\
        .close()\
        .extrude(3.5)

#connector = connector.union(hook)

hook = hook\
        .translate((10, 5, 4))




show_object(walls)
show_object(bottom_plate)
show_object(hook)

