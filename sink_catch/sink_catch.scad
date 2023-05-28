$fn = 16;
eps = 0.0;
extrusion_width = 0.45;
extrusion_height = 0.2;
base_radius = 39;
base_height = 0.2;
slit_width = 1;
slit_length = 0.6 * base_radius;
center_radius = 10;
knob_radius = 3.;
top_radius = 42;
wall_thickness = extrusion_width;
wall_height = 25;

// Bottom plate with holes
difference() {
    cylinder(h=base_height, r1=base_radius, r2=base_radius);
    for ( angle = [0:22.5:337.5] ) {
        xmove = (center_radius + 0.5 * slit_length) * cos(angle);
        ymove = (center_radius + 0.5 * slit_length) * sin(angle);
        translate([xmove, ymove, base_height / 2]) {
            rotate([0, 0, angle]) { 
                cube([slit_length, slit_width, base_height+0.001], center=true);

            }
        }
    }
}

// Walls
difference() {
    cylinder(h=wall_height, r1=base_radius, r2=top_radius);
    translate([0, 0, -eps]) {
        cylinder(h=wall_height+2*eps, r1=base_radius-wall_thickness, r2=top_radius-wall_thickness);
    }
} 

// Knob
cylinder(h=wall_height, r1=knob_radius, r2=knob_radius);



// Strengthening circles on bottom plate
// outermost
difference() {
    r = base_radius - wall_thickness;
    cylinder(h=base_height+extrusion_height, r1=r, r2=r, center=false);
    translate([0,0,-eps]) {
        cylinder(h=base_height+extrusion_height+2*eps, r1=r-extrusion_width, r2=r-extrusion_width, center=false);
    }
}

for ( f = [1/10:1/10:9/10] ) {
    difference() {
        r = base_radius * f;
        cylinder(h=base_height+extrusion_height, r1=r, r2=r, center=false);
        translate([0,0,-eps]) {
            cylinder(h=base_height+extrusion_height+2*eps, r1=r-extrusion_width, r2=r-extrusion_width, center=false);
        }
    }
}
