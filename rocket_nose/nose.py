
inner_d = 95.
inner_r = inner_d / 2.
skirt_thickness = 2.

skirt_length = 42.
floor_height = 4.
inner_height = 10.


connector_height = 10.


sPnts_inner = [
               (inner_r+skirt_thickness-4, -skirt_length/4.),
               (inner_r+skirt_thickness-2, -skirt_length/2.),
               (inner_r+skirt_thickness, -skirt_length),
]

#sPnts_outer = [(p[0]+skirt_thickness, p[1]) for p in sPnts_inner]

skirt = cq.Workplane("XZ")\
                .lineTo(inner_r-6.,0.)\
                .spline(sPnts_inner, includeCurrent=True)\
                .lineTo(0., -skirt_length)\
                .close()\
                .revolve(360, (0, 0, 0), (0, 1, 0))\
                .faces("<Z")\
                .shell(-skirt_thickness)

connector = cq.Workplane("XY")\
        .circle(30.)\
        .extrude(connector_height)\
        .faces(">Z or <Z")\
        .shell(5.)

slits = cq.Workplane("XY", origin=(0,0,connector_height/2.))\
        .box(5., inner_d, connector_height)

slits = slits.union(slits.rotateAboutCenter((0,0,1), 120))
slits = slits.union(slits.rotateAboutCenter((0,0,1), 120))
connector = connector.cut(slits)        


# slit2 = slit1.rotateAboutCenter((0,0,1), 120)
# 
# slit3 = slit2.rotateAboutCenter((0,0,1), 120)



show_object(skirt)
show_object(connector)
#show_object(slits)
#show_object(slit2)
#show_object(slit3)

