import math
import cadquery as cq

base_d = 120.
base_r = base_d / 2.
peltier_h = 42.
peltier_thickness = 3.

wall_height = 20.
wall_thickness = 2.5

screw_hole_d1 = 54.
screw_hole_d2 = 90.

connector_tube_height = 50.


indent_thickness = 4.
indent = cq.Workplane()\
        .circle(30.)\
        .extrude(indent_thickness)

base_plate = cq.Workplane()\
        .circle(base_r)\
        .rect(peltier_h, peltier_h)\
        .extrude(peltier_thickness + indent_thickness)\
        .cut(indent)\
        .translate((0., 0., -4.))


cable_slot1 = cq.Workplane("XZ", origin=(peltier_h / 2, peltier_h/2, 2))\
        .rect(-3, -7, centered=False)\
        .extrude(-3.)
cable_slot1 = cable_slot1.union(\
    cq.Workplane("XZ", origin=(peltier_h / 2, peltier_h/2, 0))\
            .rect(-3, -7, centered=False)\
            .extrude(-25.)
    )

cable_slot2 = cq.Workplane("XZ", origin=(-peltier_h / 2, peltier_h/2, 2))\
        .rect(3, -7, centered=False)\
        .extrude(-3.)
cable_slot2 = cable_slot2.union(\
    cq.Workplane("XZ", origin=(-peltier_h / 2, peltier_h/2, 0))\
            .rect(3, -7, centered=False)\
            .extrude(-25.)
    )


base_plate = base_plate\
        .cut(cable_slot1)\
        .cut(cable_slot2)

base_plate = base_plate.pushPoints(((screw_hole_d1/2., screw_hole_d2/2.),
                               (screw_hole_d1/2., -screw_hole_d2/2.),
                               (-screw_hole_d1/2., screw_hole_d2/2.),
                               (-screw_hole_d1/2., -screw_hole_d2/2.)))\
        .circle(3.)\
        .cutThruAll()

base_plate = base_plate.pushPoints(((0,50),))\
        .rect(12, 7)\
        .cutThruAll()



inner_cylinder = cq.Workplane()\
        .cylinder(wall_height, base_r + wall_thickness)\
        .faces("<Z")\
        .workplane()\
        .hole(base_d)

notch_r = 2.
notch1 = cq.Workplane(origin=(0,base_r + wall_thickness, 0))\
        .sphere(notch_r)\

notch2 = cq.Workplane(origin=(0,-base_r - wall_thickness, 0))\
        .sphere(notch_r)\

connector = base_plate\
        .union(inner_cylinder)\
        .union(notch1)\
        .union(notch2)


show_object(connector)

tube_r_inner = base_r + wall_thickness + 0.2
tube_thickness = 5.

connector_tube_lower = cq.Workplane()\
        .circle(tube_r_inner + tube_thickness)\
        .circle(tube_r_inner)\
        .extrude(connector_tube_height/2)


groove_clearance = 0.2
groove_angle_deg = 60
groove_angle_rad = groove_angle_deg / 360 * 2 * math.pi
ellipse_e = math.cos(groove_angle_rad)
ellipse_ma = (tube_r_inner+notch_r+groove_clearance) / math.cos(groove_angle_rad)



groove1 = cq.Workplane()\
        .transformed(rotate=cq.Vector(groove_angle_deg, 0, 0))\
        .ellipse(tube_r_inner+notch_r+groove_clearance, ellipse_ma)\
        .extrude(2*notch_r)\
        .fillet(notch_r-0.0001)\
        .cut(cq.Workplane(origin=(-base_r,0,0)).box(base_r, base_r, base_r))

groove2 = groove1.rotate((0,0,0), (0,0,1), 180)

connector_tube_lower = connector_tube_lower.cut(groove1).cut(groove2)

connector_tube_upper = cq.Workplane()\
        .circle(tube_r_inner + tube_thickness)\
        .circle(tube_r_inner)\
        .extrude(-connector_tube_height/2)

connector_tube = connector_tube_lower.union(connector_tube_upper)

# show_object(connector_tube)
cq.exporters.export(connector, "connector.stl")
cq.exporters.export(connector_tube, "connector_tube.stl")





