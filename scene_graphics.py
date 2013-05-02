import Universe
from graphics import *

framepath = Universe.framepath
settingspath = Universe.settingspath

agent = []
building = []
road = []
obstacle = []

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
    
    draw_graphics()
    
def draw_graphics():
    print "graphics library"
    positions=[]
    window=GraphWin("Crowd Simulation",width=300, height=300)
    window.setCoords(Universe.lmin,Universe.wmin,Universe.lmax,Universe.wmax)
    for a in agent:
        val = Circle( Point(a[0][0],a[0][1]), a[0][3]-0.1)
        val.setFill("red")
        positions.append([a[0][0],a[0][1]])
        val.draw(window)
        a.append(val)

    for o in obstacle:
        val = Circle( Point(a[0][0],a[0][1]), a[0][3])
        val.draw(window)
        val.setFill("red")
        o.append(val)

    for a in building:
        bd1 = Point(a[0][0] - a[0][3]/2, a[0][2] - a[0][5]/2)
        bd2 = Point(a[0][0] + a[0][3]/2, a[0][2] - a[0][5]/2)
        bd3 = Point(a[0][0] + a[0][3]/2, a[0][2] + a[0][5]/2)
        bd4 = Point(a[0][0] - a[0][3]/2, a[0][2] + a[0][5]/2)

        Line(bd1,bd2).draw(window)
        Line(bd2,bd3).draw(window)
        Line(bd3,bd4).draw(window)
        Line(bd4,bd1).draw(window)

        a.append(val)

    try: 
        file = open(framepath)
    except TypeError:
        print "cannot find frame file"
    file.readline()
    while True:
        line = file.readline()
        if line=="":
            break;
        line = line.split()
        i= int(line[0])
        newpos = [float(line[1]),float(line[2])]
        dpos = [newpos[0]-positions[i][0],newpos[1]-positions[i][1]]
        agent[i][1].move(dpos[0],dpos[1])
        positions[i]=newpos
    file.close()
