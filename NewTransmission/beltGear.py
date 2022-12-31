#cirName = 'Sketch.Edge1'
#teethCount = 24
#pitch = 3
makeBeltGear(cirName = 'Sketch.Edge1', teethCount = 30, pitch = 3)
#makeBeltGear(cirName = 'Sketch001.Edge1', teethCount = 10, pitch = 3)

def makeBeltGear(cirName = 'Sketch.Edge1', teethCount = 30, pitch = 3):
  #height of tooth
  diaAdj = 0.3 

  teethR = pitch/2.5
  body = App.ActiveDocument.Body

  import math

  [sketchName, edgeName] =  cirName.split('.')
  sketch = App.ActiveDocument.getObject(sketchName)
  geomPos = int(edgeName[4:]) - 1
  cir = sketch.Geometry[geomPos]
  r = teethCount*pitch/math.pi/2 - diaAdj
  sketch.movePoint(geomPos, 0, App.Vector(cir.Center.x+r, cir.Center.y))
  App.ActiveDocument.recompute()

  teethAng = math.pi*2/teethCount

  trims = []
  origTrims = []
  nextEdge = 0
  for i in range(teethCount):
    curAng = i*teethAng
    cs = math.cos(curAng)
    si = math.sin(curAng)
    x = r*cs + cir.Center.x
    y = r*si + cir.Center.y
    pc = Part.Circle(App.Vector(x,y), App.Vector(0,0,1), teethR)
    con = sketch.addGeometry(pc)
    nextEdge = con + 1
    App.ActiveDocument.recompute()
    #sketch.trim(con, )
    trims.append({
      'ind': con,
      'vec': App.Vector(teethR*cs+x, teethR*si + y)
    })
    #App.ActiveDocument.recompute()
    try:
      #cs = math.cos(curAng+0.05)
      #si = math.sin(curAng +0.05)
      #x = r*cs + cir.Center.x
      #y = r*si + cir.Center.y
      #sketch.trim(geomPos, App.Vector(x,y))
      origTrims.append({
        'ind': geomPos,
        'vec': App.Vector(x,y)
      })    
      #App.ActiveDocument.recompute()
    except Exception as err:
      print(err)
      print("triming " + str(geomPos)+ " x="+str(x)+","+str(y))
      #npc = Part.Circle(App.Vector(x,y), App.Vector(0,0,1), 0.1)
      #con = sketch.addGeometry(npc)

  for trim in trims:
    sketch.trim(trim['ind'], trim['vec'])

  App.ActiveDocument.recompute()
  print("nextEdge="+str(nextEdge))
  origTrims.reverse()
  for trim in origTrims:
    try:
      sketch.trim(trim['ind'], trim['vec'])
      App.ActiveDocument.recompute()
      print("good trim inner")
    except Exception as err:
      print("triming at", trim['vec'])
      sketch.trim(nextEdge, trim['vec'])

  App.ActiveDocument.recompute()
  print('done')