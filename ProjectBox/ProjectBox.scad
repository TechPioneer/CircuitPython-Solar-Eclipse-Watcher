$fn = 64;

postSpacingX = 15.2 * 9;
postSpacingY = 15.2 * 4;

boardWidth = postSpacingX + 15.2;
boardDepth = postSpacingY + 15.2;
spacingAroundBoard = 10;
wallThickness = 2;
cornerRadius = 5;
bottomSpacing = 30;
topSpacing = 6;

raisedLipHeight = 4;

// Calculated
bottomHeight = wallThickness + bottomSpacing;
topHeight = wallThickness + topSpacing;

insideWidth = boardWidth + 2 * spacingAroundBoard;
insideDepth = boardDepth + 2 * spacingAroundBoard;

outsideWidth = insideWidth + 2 * wallThickness;
outsideDepth = insideDepth + 2 * wallThickness;


// Uncomment the one you want to see

//frame();
//top();
bottom();


module posts() {
  translate([postSpacingX/2, postSpacingY/2, 0])
    post();
  translate([postSpacingX/2, -postSpacingY/2, 0])
    post();
  translate([-postSpacingX/2, postSpacingY/2, 0])
    post();
  translate([-postSpacingX/2, -postSpacingY/2, 0])
    post();
}

module post() {
  difference() {
    cylinder(bottomSpacing, 5, 5);
    translate([0, 0, .1])
      cylinder(bottomSpacing, 1.25, 1.25);
  }
}

module frame() {
    difference() {
      cube([(outsideWidth-wallThickness*2)/2-2, outsideDepth-wallThickness*2-2, wallThickness], true);
      cube([(outsideWidth-wallThickness*2)/2-20, outsideDepth-wallThickness*2-20, wallThickness*2], true);
    }
}


module top() {
        translate([0, 0, topHeight - wallThickness]) {
            difference() {
                cube([outsideWidth, outsideDepth, topHeight*2], true);
                translate([0, 0, topHeight])
                    cube([outsideWidth+1, outsideDepth+1, topHeight*2], true);
              //frame
                translate([(outsideWidth-wallThickness*2)/4, 0, -10])
                    cube([(outsideWidth-wallThickness*2)/2-20, outsideDepth-wallThickness*2-20, topHeight*2], true);
                translate([0, 0, -raisedLipHeight])
                    difference() {
                        cube([outsideWidth-wallThickness, outsideDepth-wallThickness, topHeight*2], true);
                        translate([0, 0, -topHeight])
                            cube([outsideWidth, outsideDepth, topHeight*2], true);
                    }
                translate([0, 0, wallThickness])
                    cube([insideWidth, insideDepth, topHeight*2], true);
                radius = 2;
                for(x = [-outsideWidth+wallThickness+radius:10:-wallThickness-radius])
                  for(y = [0:10:outsideDepth/2-wallThickness-radius]) {
                    translate([x, y, -5])
                      cylinder(10, radius, radius, true);
                    translate([x, -y, -5])
                      cylinder(10, radius, radius, true);
                  }
            }
            translate([0, 0, -topHeight/2+.5])
              cube([2, outsideDepth-wallThickness*2-1, topHeight-3], true);
        }
}

module bottom() {
      translate([0, 0, bottomHeight - wallThickness]) {
          difference() {
              union() {
                  difference() {
                      cube([outsideWidth, outsideDepth, bottomHeight*2], true);
                      translate([0, 0, bottomHeight])
                          cube([outsideWidth+1, outsideDepth+1, bottomHeight*2], true);
                  }
                  translate([0, 0, raisedLipHeight])
                      cube([outsideWidth-wallThickness-.1, outsideDepth-wallThickness-.1, bottomHeight*2], true);
              }
              translate([0, 0, bottomHeight + raisedLipHeight])
                  cube([outsideWidth, outsideDepth, bottomHeight*2], true);
              translate([0, 0, wallThickness])
                  cube([insideWidth, insideDepth, bottomHeight*2], true);
              
              // plug
  translate([-postSpacingX/2 + 38, -boardDepth/2 - 7.5, -bottomHeight + 15])
  cube([25, 15, 15], true);
          for(x = [wallThickness+2:10:outsideWidth/2-25])
            translate([x+4, outsideDepth, -4])
              rotate([90, 90, 0])
                hull() {
                  cylinder(outsideDepth*2, 2, 2);
                  translate([2*bottomHeight/3, 0, 0])
                    cylinder(outsideDepth*2, 2, 2);
                }
          }
      }
      posts();
}