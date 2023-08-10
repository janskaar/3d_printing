
inner_d = 95.
inner_r = inner_d / 2.
skirt_thickness = 1.5

skirt_length = 42.
floor_height = 4.
inner_height = 10.


connector_r = 30.
connector_height = 10.
connector_thickness = 5.

nose_height = 45.

#
# Part that attaches to rocket
#

sPnts = [
         (inner_r+skirt_thickness-2, -skirt_length/4.),
         (inner_r+skirt_thickness-1, -skirt_length/2.),
         (inner_r+skirt_thickness, -skirt_length),
]

skirt = cq.Workplane("XZ")\
                .lineTo(inner_r-3.,0.)\
                .spline(sPnts, includeCurrent=True)\
                .lineTo(0., -skirt_length)\
                .close()\
                .revolve(360, (0, 0, 0), (0, 1, 0))\
                .faces("<Z")\
                .shell(-skirt_thickness)

connector = cq.Workplane("XY")\
        .circle(connector_r)\
        .extrude(connector_height)\
        .faces(">Z or <Z")\
        .shell(connector_thickness)

slits = cq.Workplane("XY", origin=(0,0,connector_height/2.))\
        .box(5., inner_d, connector_height)

slits = slits.union(slits.rotateAboutCenter((0,0,1), 120))
slits = slits.union(slits.rotateAboutCenter((0,0,1), 120))
connector = connector.cut(slits)        

startAngle = 12
holes = cq.Workplane("XZ", origin=(0,0,3.))\
        .cylinder(inner_d, 1., centered = True)\
        .rotateAboutCenter((0,0,1), startAngle)

for i in range(5):
    holes = holes.union(holes.rotateAboutCenter((0,0,1), 60))

holes = holes.union(holes.rotateAboutCenter((0,0,1), 60 - 2 * startAngle))

for i in range(5):
    holes = holes.union(holes.rotateAboutCenter((0,0,1), 60))

connector = connector.cut(holes)

bracket = skirt.union(connector)


#
# Nose tip
#

sPnts = [
         (inner_r - 4.5, connector_height/2.),
         (inner_r - 6, connector_height),
]

lower_nose = cq.Workplane("XZ")\
        .lineTo(inner_r-3.,0.)\
        .spline(sPnts, includeCurrent=True)\
        .lineTo(0., connector_height)\
        .close()\
        .revolve(360, (0, 0, 0), (0, 1, 0))\
        .faces(">Z")\
        .workplane()\
        .hole(2 * (connector_r + connector_thickness) + 2.)

lower_nose = lower_nose.edges(cq.selectors.NearestToPointSelector((0,0,10)))\
        .fillet(1.0)

holes = cq.Workplane("XZ", origin=(0,inner_r,3.))\
        .cylinder(30., 1.)
holes = holes.union(holes.translate((4,0,0)))
lower_nose = lower_nose.cut(holes)


sPnts = [
        (37., nose_height * 0.25),
        (23, nose_height * 0.8),
        (10, nose_height * 0.96),
        (0., nose_height)
]


upper_nose = cq.Workplane("XZ", origin=(0,0,connector_height))\
        .lineTo(inner_r-6.,0.)\
        .spline(sPnts, includeCurrent=True)\
        .lineTo(0., connector_height)\
        .close()\
        .revolve(360, (0, 0, 0), (0, 1, 0))\
        .faces("<Z")\
        .shell(-2.)
nose = lower_nose.union(upper_nose)

cq.exporters.export(nose, "/home/janeirik/Repositories/3d_printing/rocket_nose/nose.stl",
                    angularTolerance=0.05)
#cq.exporters.export(bracket, "/home/janeirik/Repositories/3d_printing/rocket_nose/bracket.stl")
show_object(bracket)
#show_object(upper_nose)
show_object(lower_nose)
#show_object(nose)





