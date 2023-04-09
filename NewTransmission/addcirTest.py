skt = App.getDocument('FrontRearConn').getObject('Sketch005')
Gui.runCommand('Sketcher_CompCreateCircle',0)


totalItems = 11
lineInd = 7
distName = 'Spreadsheet.screwSep'
screwSep = 6
circleR = 1.4
circleRName = 'Spreadsheet.screwTightR'
cirInd = skt.Geometry.__len__()
constraintCount = skt.ConstraintCount


skt.addGeometry(Part.Circle(App.Vector(5,8,0),App.Vector(0,0,1),1.4),False)
skt.addConstraint(Sketcher.Constraint('Coincident',cirInd,3,lineInd, 1)) 

skt.addConstraint(Sketcher.Constraint('Radius',cirInd,circleR))
constName = 'Constraints['+str(skt.ConstraintCount - 1)+']'
skt.setExpression(constName, circleRName)
App.ActiveDocument.recompute()





for itm in range(totalItems-1):
  Gui.runCommand('Sketcher_CompCreateCircle',0)
  skt.addGeometry(Part.Circle(App.Vector(5 + (itm+1)*screwSep,8,0),App.Vector(0,0,1),1.4),False)
  cirInd = cirInd + 1
  skt.addConstraint(Sketcher.Constraint('PointOnObject', cirInd ,3, lineInd))   
  skt.addConstraint(Sketcher.Constraint('DistanceX',cirInd - 1,3, cirInd,3, screwSep))  
  constName = 'Constraints['+str(skt.ConstraintCount - 1)+']'
  skt.setExpression(constName, distName)
  skt.addConstraint(Sketcher.Constraint('Radius',cirInd,circleR))
  constName = 'Constraints['+str(skt.ConstraintCount - 1)+']'
  skt.setExpression(constName, circleRName)
  App.ActiveDocument.recompute()

