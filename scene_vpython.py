import Universe
from visual import *

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
    
    draw_vpython()
    
def draw_vpython():
    print "vpython"
    floor = box(pos=(0,0,0),length = 50,height=0.01,width=50,color=color.yellow)

    for a in agent:
        a.append(cone(pos=vector(a[0][0],0,a[0][1]),axis=[0,a[0][2]],radius=a[0][3],color=(a[0][4],a[0][5],a[0][6])))

    for a in obstacle:
        a.append(cylinder(pos=vector(a[0][0],0,a[0][1]),axis=[0,a[0][2]],radius=a[0][3],color=(a[0][4],a[0][5],a[0][6])))

    for a in building:
        a.append(box(pos=vector(a[0][0],a[0][1],a[0][2]),length=a[0][3],height=a[0][4]+0.05,width=a[0][5],color=(a[0][6],a[0][7],a[0][8])))

    try: 
        file = open(framepath)
    except TypeError:
        print "cannot find frame file"
        
    file.readline()
    while True:
        rate(50)
        line = file.readline()
        if line=="":
            break;
        line = line.split()
        i= int(line[0])
        agent[i][1].pos = vector(float(line[1]),0,float(line[2]))
    file.close()
    print
 
