import os
lmax = 20.0
lmin = -20.0
wmax = 20
wmin = -20

fps = 9
timeframe=0
numberofframes=250

agent = []
object = []
road = []

dirpath = '/home/g08p6176/Download/ibizan/apps/crowd/Project assignments/CD/crowd'

if os.path=="nt":
	framepath = dirpath + '/data//frame.txt'
	settingspath = dirpath + '/data//testv.txt'
else:
	framepath = dirpath + '/data/frame.txt'
	settingspath = dirpath + '/data/testv.txt'

minradius=0.25
maxradius=0.35

minradius=0.25
maxradius=0.35

minspeed = 1.5
maxspeed = 1.5

doorw=2.0

cellw = 20
cellh = 20
bucket = []
env = []
for i in range(cellw):
    bucket.append([])
    for j in range(cellh):
        bucket[i].append([])
        bucket[i][j]=[]

for i in range(cellw):
    env.append([])
    for j in range(cellh):
        env[i].append([])
        env[i][j]=[]

statenum=1
states = ["hunger","thrist","shopping","work","school"]
intentions= ["eat", "drink", "shop","work","school"]
factors =   [  1.5     ,     1.0      ,  1.35       ,   1.75,        1.005]

ts = 1.0/fps

def updatestate(name,val):
    index = name
    v= val+factors[index]*(ts*ts*ts)
    v=min(v,1.0)
    return v

def updatebucket():
    for a in agent:
        w = int(a.position.x % cellw)
        h = int(a.position.z % cellh)
        bucket[w][h].append(agent.index(a))
    temp = []
    for i in range(cellw):
        for j in range(cellh):
            temp = []
            for o in bucket[i][j]:
                if not o in temp:
                    temp.append(o)
                else:
                    bucket[i][j].remove(o)

def updateenv():
    for o in object:
        if o.classv == "obstacle":
            w = int(o.position.x % cellw)
            h = int(o.position.z % cellh)
            env[w][h].append(o)
            i =int(self.radius%cellw)
            for r in range(i):
                if w-r>=0:
                    env[w-r][h].append(o)
                    if h-r>=0:
                        env[w-r][h-r].append(o)
                    if h+r<cellh:
                        env[w-r][h+r].append(o)
                if h-r>=0:
                    env[w][h-r].append(o)
                    if w+r<cellw:
                        env[w+r][h-r].append(o)
                if w+r<cellw:
                    env[w+r][h].append(o)
                    if h+r<cellh:
                        env[w+r][h+r].append(o)
                if h+r<cellh:
                    env[w][h+r].append(o)

        if o.classv == "building":
            for l in o.line:
                for a in l.points:
                    w = int(o.position.x % cellw)
                    h = int(o.position.z % cellh)
                    if not l in env[w][h]:
                        env[w][h].append(l)
        for i in range(cellw):
            for j in range(cellh):
                temp = []
                for o in env[i][j]:
                    if not o in temp:
                        temp.append(o)
                    else:
                        env[i][j].remove(o)
        
            

def erase():
    try:
        file = open(settingspath,"w")
        file.write("#class posx posy h rad r g b")
        file.close
    except TypeError:
        return
    try:
        file = open(framepath,"w")
        file.write("#class posx posy h rad r g b")
        file.close
    except TypeError:
        return
