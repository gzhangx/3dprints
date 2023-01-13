

#------------------------- Start --------------------
# sketches = ['Sketch005', 'Sketch006']
# edges = ['Edge1', 'Edge2']
# for s in sketches:
#   for e in edges:
#     makeScrewHole(s+'.'+e)

#fullName: Sketch006.Edge1
def makeScrewHole(fullName, bodyName = 'Body'):
import math

toothSize = 1.8
helixPitch = toothSize + 0.1
helixDepth = 6

nameParts = fullName.split('.')    
sketchName = nameParts[0]
body = App.ActiveDocument.getObject(bodyName)

curSketch = body.getObject(sketchName)
egmPos = int(nameParts[1][4:])-1
#get selection

gem = curSketch.Geometry[egmPos]
radius = gem.Radius;

sk4 = body.newObject('Sketcher::SketchObject','SketchTemp_'+curSketch.Name+'_Edge'+str(egmPos))
sk4.Support = curSketch.Support;
sk4.MapMode = 'FlatFace'
sk4.AttachmentOffset = App.Placement(gem.Location,App.Rotation(App.Vector(1.00,0.00,0.00),90.00))
App.ActiveDocument.recompute()

Gui.runCommand('Sketcher_CreateLine',0)
height = math.sqrt(toothSize*toothSize*3/4);
sk4.addGeometry(Part.LineSegment(App.Vector(radius, toothSize/2,0),App.Vector(radius+height,0,0)),False)
sk4.addGeometry(Part.LineSegment(App.Vector(radius+height,0,0), App.Vector(radius, -toothSize/2,0)),False)
sk4.addGeometry(Part.LineSegment(App.Vector(radius, -toothSize/2,0), App.Vector(radius, toothSize/2,0)),False)
sk4.addConstraint(Sketcher.Constraint('Equal',2,0)) 
sk4.addConstraint(Sketcher.Constraint('Equal',2,1)) 
sk4.addConstraint(Sketcher.Constraint('Distance',2, toothSize)) 
sk4.setDatum(2,App.Units.Quantity(str(toothSize)+' mm'))

sk4.addConstraint(Sketcher.Constraint('Coincident', 0, 2, 1, 1))
sk4.addConstraint(Sketcher.Constraint('Coincident', 1, 2, 2, 1))
sk4.addConstraint(Sketcher.Constraint('Coincident', 2, 2, 0, 1))
sk4.addConstraint(Sketcher.Constraint('Parallel',2,-2)) 
sk4.addConstraint(Sketcher.Constraint('PointOnObject',0,2,-1))
Gui.runCommand('Sketcher_ConstrainDistanceX',0)
sk4.addConstraint(Sketcher.Constraint('DistanceX',-1,1,0,1, radius)) 
sk4.setDatum(8,App.Units.Quantity(str(radius)+' mm'))

helix = body.newObject('PartDesign::SubtractiveHelix','SubtractiveHelix')
helix.Profile = sk4
helix.ReferenceAxis = (sk4, ['V_Axis'])
helix.Mode = 0
helix.Pitch = helixPitch
helix.Height = helixDepth
helix.Angle = 0
helix.Growth = 0
helix.LeftHanded = 0
helix.Reversed = 1
App.ActiveDocument.recompute()
