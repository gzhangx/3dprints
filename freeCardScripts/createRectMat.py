# get current selected sketch (make sure it is a sketch)
sketch = App.ActiveDocument.ActiveObject

startX = 10
startY = 10
xCount = 3
yCount = 3
baseWidth = 2.75
spacing = 2

xStep = baseWidth+ spacing
yStep = baseWidth + spacing

curXOff = 0
curYoff = 0
n = 0

currentEdgeCount = 0


for y in range(yCount):
    for x in range(xCount):
        curXOff = x*xStep
        curYoff = y*yStep
        geoList = []
        # left top to left bottom to right bottom to right top
        curX = startY + curXOff
        curY = startY + curYoff
        thisSize = baseWidth + n*0.01
        leftX = curX
        topY = curY
        rightX = curX + thisSize
        bottomY = curY - thisSize
        geoList.append(Part.LineSegment(App.Vector(leftX, topY, 0.000000),App.Vector(leftX, bottomY, 0.000000)))
        geoList.append(Part.LineSegment(App.Vector(leftX, bottomY, 0.000000),App.Vector(rightX, bottomY, 0.000000)))
        geoList.append(Part.LineSegment(App.Vector(rightX, bottomY, 0.000000),App.Vector(rightX, topY, 0.000000)))
        geoList.append(Part.LineSegment(App.Vector(rightX, topY, 0.000000),App.Vector(leftX, topY, 0.000000)))
        sketch.addGeometry(geoList,False)
        del geoList
        App.ActiveDocument.recompute()
        time.sleep(2)


        constraintList = []
        constraintList.append(Sketcher.Constraint('Coincident', currentEdgeCount, 2, currentEdgeCount+1, 1))
        constraintList.append(Sketcher.Constraint('Coincident', currentEdgeCount+1, 2, currentEdgeCount+2, 1))
        constraintList.append(Sketcher.Constraint('Coincident', currentEdgeCount+2, 2, currentEdgeCount+3, 1))
        constraintList.append(Sketcher.Constraint('Coincident', currentEdgeCount+3, 2, currentEdgeCount + 0, 1))
        constraintList.append(Sketcher.Constraint('Vertical', currentEdgeCount))
        constraintList.append(Sketcher.Constraint('Vertical', currentEdgeCount+2))
        constraintList.append(Sketcher.Constraint('Horizontal', currentEdgeCount+1))
        constraintList.append(Sketcher.Constraint('Horizontal', currentEdgeCount+3))
        sketch.addConstraint(constraintList)
        del constraintList
        sketch.addConstraint(Sketcher.Constraint('Equal',currentEdgeCount+3,currentEdgeCount+0))
        sketch.addConstraint(Sketcher.Constraint('DistanceY',currentEdgeCount+0,2,currentEdgeCount+0,1,thisSize))
        App.ActiveDocument.recompute()
        time.sleep(2)
        currentEdgeCount = currentEdgeCount + 4
        n = n+1
    

