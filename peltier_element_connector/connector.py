import math

base_d = 120.
base_r = base_d / 2.
peltier_h = 42.
peltier_thickness = 8.

wall_height = 20.
wall_thickness = 2.5

screw_hole_d1 = 54.
screw_hole_d2 = 90.

connector_tube_height = 50.

indent = cq.Workplane()\
        .circle(30.)\
        .extrude(4.)

base_plate = cq.Workplane()\
        .circle(base_r)\
        .rect(peltier_h, peltier_h)\
        .extrude(peltier_thickness)\
        .cut(indent)\
        .translate((0., 0., -4.))

base_plate = base_plate.pushPoints(((screw_hole_d1/2., screw_hole_d2/2.),
                               (screw_hole_d1/2., -screw_hole_d2/2.),
                               (-screw_hole_d1/2., screw_hole_d2/2.),
                               (-screw_hole_d1/2., -screw_hole_d2/2.)))\
        .circle(3.)\
        .cutThruAll()




inner_cylinder = cq.Workplane()\
        .cylinder(wall_height, base_r + wall_thickness)\
        .faces("<Z")\
        .workplane()\
        .hole(base_d)

notch1 = cq.Workplane(origin=(0,base_r + wall_thickness, 0))\
        .sphere(2.)\

notch2 = cq.Workplane(origin=(0,-base_r - wall_thickness, 0))\
        .sphere(2.)\

connector = base_plate\
        .union(inner_cylinder)\
        .union(notch1)\
        .union(notch2)


show_object(connector)

connector_tube = cq.Workplane()\
        .circle(base_r + wall_thickness + 5.0)\
        .circle(base_r + wall_thickness + 0.5)\
        .extrude(connector_tube_height)

groove_height = connector_tube_height / 2.
twist_degrees = 60
# find how large the radius of the circle has to be in order
# for the twist-extruded groove to have desired radius (along 
# different axis than the circle)
theta = math.atan(groove_height / (2 * math.pi * (base_r + wall_thickness + 0.5) * twist_degrees / 360))
# assume notch radius of 2,
circle_r = 2. / math.sin(theta) / 2.

grooves = cq.Workplane()\
        .pushPoints(((0, base_r + wall_thickness + 0.2),
                    (0, -base_r - wall_thickness + 0.2)))\
        .circle(circle_r + .5)\
        .twistExtrude(groove_height, twist_degrees)

connector_tube = connector_tube.cut(grooves)


show_object(connector_tube)












