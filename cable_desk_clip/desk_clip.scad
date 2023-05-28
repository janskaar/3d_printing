$fn = 128;
eps = 0.01;
base_thickness = 4.;
height = 22.7;
depth = 20.;
width = 10.;

radius = 2.;
top_thickness = 2.;


minkowski() {
    translate([0,0,-(height+2*base_thickness)/2]){
    difference() {
        cube([depth,width,height+2*base_thickness], center=true);
        translate([base_thickness,0,0]) {
            cube([depth+eps,width+eps,height], center=true);
        }
    }
    }
sphere(0.25);
}

minkowski() {
    translate([-depth / 3, 0, 3.5]) {
    rotate([0,-90,0]) {
    difference() {
        cylinder(h=top_thickness, r1=radius + top_thickness, r2=radius + top_thickness, center=true);
        cylinder(h=top_thickness+eps, r1=radius, r2=radius, center=true);
        translate([radius,0,0]) {
            cube([2 * radius, 3, 2 * top_thickness], center=true);
        }
    }
    }
    }
sphere(0.25);
}
