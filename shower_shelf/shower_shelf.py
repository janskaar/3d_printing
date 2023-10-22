import numpy as np

wall_thickness = 3.
wall_height = 30.

bottom_x = 156
bottom_y = 70
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

eps = 0.5 
hook = cq.Workplane("YZ", origin=(-wall_thickness, 0, 0))\
        .lineTo(0, wall_height * 2)\
        .lineTo(-13, wall_height * 2)\
        .lineTo(-13, wall_height+15)\
        .lineTo(-wall_thickness-6-eps, wall_height+15)\
        .lineTo(-wall_thickness-6-eps, wall_height + 25)\
        .lineTo(-wall_thickness, wall_height + 25)\
        .lineTo(-wall_thickness,0)\
        .close()\
        .extrude(bottom_x + 2 * wall_thickness)


shelf = bottom_plate.union(walls).union(hook)


cq.exporters.export(shelf, "shelf.stl")
show_object(shelf)

