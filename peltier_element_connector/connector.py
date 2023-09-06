base_d = 110.
base_r = base_d / 2.
peltier_h = 42.
peltier_thickness = 8.

wall_height = 20.
wall_thickness = 2.5


indent = cq.Workplane()\
        .circle(30.)\
        .extrude(4.)

base_plate = cq.Workplane()\
        .circle(base_r)\
        .rect(peltier_h, peltier_h)\
        .extrude(peltier_thickness)\
        .cut(indent)\
        .translate((0., 0., -4.))

inner_cylinder = cq.Workplane()\
        .cylinder(wall_height, base_r + wall_thickness)\
        .faces("<Z")\
        .workplane()\
        .hole(base_d)

notch1 = cq.Workplane(origin=(0,base_r + wall_thickness, 0))\
        .sphere(1.)\

notch2 = cq.Workplane(origin=(0,-base_r - wall_thickness, 0))\
        .sphere(1.)\

connector = base_plate\
        .union(inner_cylinder)\
        .union(notch1)\
        .union(notch2)


show_object(connector)










