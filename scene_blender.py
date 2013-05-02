#!BPY

import Blender
from Blender import *
import Universe
from random import *
from math import pi


agent = []
building = []
road = []
armlist = []

framepath = Universe.framepath
settingspath = Universe.settingspath

scenepath = Universe.dirpath + '/blend_files/'
modeldir = scenepath + '/pose_man_no_hair.blend'

cubeMesh = Mesh.Primitives.Cube(1.0)
cubeMesh.transform(Mathutils.RotationMatrix(90,4,'x'),True)
doorMesh = Mesh.Primitives.Cube(1.0)
doorMesh.transform(Mathutils.RotationMatrix(90,4,'x'),True)
roadMesh = Mesh.Primitives.Cube(1.0)
roadMesh.transform(Mathutils.RotationMatrix(90,4,'x'),True)

def draw():
    settings = open(settingspath)
    settings.readline()
    while True:
        line = settings.readline()
        if line=="":
            break;
        line = line.split()
        xx = float(line[1])
        zz = float(line[2])
        h = float(line[3])
        R = float(line[4])
        G = float(line[5])
        B = float(line[6])
        if line[0]=="agent":
            rad = float(line[7])
	    agent.append([[xx,zz,h,rad,R,G,B]])
	    
        if line[0]=="obstacle":
            rad = float(line[7])
            obstacle.append([[xx,zz,h,rad,R,G,B]])
        if line[0]=="building":
            x = float(line[7])
            y = h
            z = float(line[8])
	    drx = float(line[9])
	    drz = float(line[10])
            building.append([[xx,h/2.0,zz,x,y,z,R,G,B,drx,drz,line[11],int(line[12])]])
	if line[0]=="road":
            x = float(line[7])
            y = h
            z = float(line[8])
	    road.append([[xx,h/2.0,zz,x,y,z,R,G,B]])
    settings.close()
    
    draw_blender()


def draw_blender():

	Library.Open(scenepath+"scene.blend")
	Library.Load('landscape', 'Object')
	
	tmp = Material.New('empty')
	
	for a in building:
		
		bObj = Object.New('Mesh',str(building.index(a)) +"_"+a[0][11]+ "_Building")
		bObj.setSize([a[0][3],a[0][4],a[0][5]])
		bObj.setLocation ([a[0][0],a[0][4]/2,a[0][2]])
		bObj.link(cubeMesh)
		Scene.GetCurrent().objects.link(bObj)
		drawdoor(a[0][9],a[0][10],a[0][12])
		a.append(bObj)

	for a in road:
		bObj = Object.New('Mesh',str(road.index(a)) + "_Road")
		bObj.setSize([a[0][3],0.001,a[0][5]])
		bObj.setLocation ([a[0][0],0.05,a[0][2]])
		bObj.link(roadMesh)
		Scene.GetCurrent().objects.link(bObj)
		a.append(bObj)


	Library.Open(modeldir)
	
	for a in agent:
		Library.Load('model', 'Object')
		bObj = Object.Get('model')
		bObj.setName(str(agent.index(a)) + "_Agent")
		
		Library.Load('Walk', 'Object')
		arm= Object.Get('Walk')
		arm.setName(str(agent.index(a)) + "_Arm")
		armlist.append(arm)
	
		manModifier = bObj.modifiers
		mod = manModifier.append(Modifier.Types.ARMATURE)
		mod[Modifier.Settings.OBJECT] =  arm
		
		bObj.makeDisplayList()
				
		mat = Material.New('Mat_')
		mat.rgbCol = [0.4,0.4,0.4]
		bObj.setMaterials([tmp,mat])
		bObj.colbits=1<<1
		
		newIpo = Ipo.New('Object', "Agent_ipo")
		bObj.setIpo(newIpo)
		curveX = newIpo.addCurve('LocX')
		curveZ = newIpo.addCurve('LocZ')
		rotY = newIpo.addCurve('RotY')
		curveX.setInterpolation("Bezier")
		curveZ.setInterpolation("Bezier")
		rotY.setInterpolation("Bezier")
		curveX.addBezier((1, a[0][0]))
		curveZ.addBezier((1, a[0][1]))

		walkIpo = Ipo.New('Object', "Walk_arm_ipo")
		arm.setIpo(walkIpo)
		acurveX = walkIpo.addCurve('LocX')
		acurveZ = walkIpo.addCurve('LocZ')
		arotY = walkIpo.addCurve('RotY')
		acurveX.setInterpolation("Bezier")
		acurveZ.setInterpolation("Bezier")
		arotY.setInterpolation("Bezier")
		acurveX.addBezier((1, a[0][0]))
		acurveZ.addBezier((1, a[0][0]))


		a.append(bObj)

	try: 
		file = open(framepath)
	except TypeError:
		print "cannot find frame file"
		exit()
	file.readline()
	while True:
		line = file.readline()
		if line=="":
			break;
		line = line.split()
		i= int(line[0])
		frame = int(line[5])
	
		
		mat = agent[i][1].getMaterials()[1]
		mat.rgbCol = [float(line[6]),float(line[7]),float(line[8])]
		bObj.colbits=1<<1
	
		ipo = agent[i][1].getIpo()
		curveX = ipo.getCurve('LocX')
		curveZ = ipo.getCurve('LocZ')
		rotY = ipo.getCurve('RotY')
		curveX.addBezier((frame, float(line[1])))
		curveZ.addBezier((frame, float(line[2])))
		rotY.addBezier((frame, float(line[3])))
		
		arm = armlist[i]
		ipo = arm.getIpo() 
		curveX = ipo.getCurve('LocX')
		curveZ = ipo.getCurve('LocZ')
		rotY = ipo.getCurve('RotY')
		curveX.addBezier((frame, float(line[1])))
		curveZ.addBezier((frame, float(line[2])))
		rotY.addBezier((frame, float(line[3])))
	file.close()
	Library.Update()
	Scene.GetCurrent().update()
	


def drawdoor(posx,posz,dint):
  if dint%2==0:
    size = [1.2,2.5,0.1]
  else:
    size = [0.1,2.5,1.2]
  entry = [posx,0.0,posz]
  bObj = Object.New('Mesh',"entry")
  bObj.setSize(size)
  bObj.link(doorMesh)
  bObj.setLocation (entry[0], size[1]/2, entry[2])
  Scene.GetCurrent().objects.link(bObj)