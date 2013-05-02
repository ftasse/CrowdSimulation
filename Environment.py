
import Universe

from Tools import *
from random import uniform,random

c = 5

lmax=Universe.lmax-c
lmin=Universe.lmin+c
wmax=Universe.wmax-c
wmin=Universe.wmin+c

doorw = Universe.doorw
maxradius = Universe.maxradius

def nearobject(point,r=0):
    near=[]
    for o in Universe.object:
        if o.classv == "building":
            near.extend(o.nearobstacle(point,r))
        if o.classv == "obstacle":
            near.extend(o.nearobstacle(point,r))
    return near

def linenearobject(line):
    for o in Universe.object:
        if o.classv!="empty" and o.linenearobstacle(line):
            return True
    return False

def nearroad(point):
    near=[]
    for o in Universe.road:
        near.extend(o.nearobstacle(point))
    return near

def linenearroad(line):
    for o in Universe.road:
        if o.linenearobstacle(line):
            return True
    return False
        

def randombuilding():
    xx = uniform(lmin,lmax)
    yy = 0
    zz = uniform(wmin,wmax)
    x = uniform(6,9)
    y = uniform(6,9)
    yy += y/2
    z = uniform(6,9)
    red = random()
    green = random()
    blue = random()
    return building (pos = vector(xx,yy,zz), size=(x,y,z),color=(red,green,blue),nature="eat")

def randomobstacle():
    xx = uniform(lmin,lmax)
    yy =0
    zz = uniform(wmin,wmax)
    red = random()
    green = random()
    blue = random()
    return obstacle(pos = vector(xx,yy,zz), rad=uniform(3,5), h=uniform(6,9), color=(red,green,blue),nature="drink")

def randomroad():
    xx = uniform(lmin,lmax)
    yy = 0.1
    zz = uniform(wmin,wmax)
    x = uniform(6,9)
    z = uniform(6,9)
    y = yy/2
    red = random()
    green = random()
    blue = random()
    return road (pos = vector(xx,yy,zz), size=(x,y,z),color=(red,green,blue))

 

class building(object):
    def nearobstacle(self, point,r=0):
        near = []
        for li in self.line:
            if li.distancepointline(point)<maxradius+r:
                near.append(li)
        return near
        
    def linenearobstacle(self, other):
        for li in self.line:
            if other.intersectionWithLine(li)!=None:
                return True
        return False
        
    def __init__(self,pos,size,color= None,nature=" ",draw=True):
        self.position = pos
        self.length = size[0]
        self.height = size[1]
        self.width = size[2]
	if color==None:
	  color = [random(),random(),random()]
        self.color = color
        self.classv = "building"
        self.nature = nature
        
        
        border0=(vector(pos.x-size[0]/2,0.0,pos.z-size[2]/2))
        border1=(vector(pos.x+size[0]/2,0.0,pos.z-size[2]/2))
        border2=(vector(pos.x+size[0]/2,0.0,pos.z+size[2]/2))
        border3=(vector(pos.x-size[0]/2,0.0,pos.z+size[2]/2))
	self.bd=  [border0,border1,border2,border3]
        self.border = [border0,border1,border2,border3]
        doorint = 0
        i=0
        while i<4:
            if line(self.border[i],self.border[(i+1)%4]).distancepointline(vector(0,0,0))<line(self.border[doorint],self.border[(doorint+1)%4]).distancepointline(vector(0,0,0)):
                doorint =i
            i+=1
       

        dist  = mag(self.border[(doorint+1)%4]-self.border[doorint])
        borda = self.border[doorint]+(self.border[(doorint+1)%4]-self.border[doorint])*(0.5-doorw/(2*dist))
        bordb = self.border[doorint]+(self.border[(doorint+1)%4]-self.border[doorint])*(0.5+doorw/(2*dist))
        self.doorpos = (self.border[(doorint+1)%4]+self.border[doorint])*0.5
        self.border.insert(doorint+1,borda)
        self.border.insert(doorint+2,bordb)
        self.line=[]
        for i in range(len(self.border)):
            if not(self.border[i]==borda and self.border[(i+1)%len(self.border)]==bordb):
                li = line(self.border[i],self.border[(i+1)%len(self.border)])
                self.line.append(li)

        Universe.object.append(self)
        
        try:
	    if draw:
	      f=open(Universe.settingspath,'a')
	      f.write("\nbuilding "+" "+str(pos.x)+"  "+str(pos.z)+" "+str(size[1])+" "+str(color[0])+" "+str(color[1])+" "+str(color[2])+" "+str(size[0])+ " "+str(size[2])+" "+str(self.doorpos.x)+ " "+str(self.doorpos.z)+" "+str(self.nature)+ " "+str(doorint))
	      f.close()
            
        except TypeError:
            print "cannot save his work"
            return
        #self.position = self.doorpos
            
class empty(object):
    def nearobstacle(self, point,r=0):
        near = []
        if mag(self.position-point)<maxradius+r:
            near.append(self)
        return near
        
    def linenearobstacle(self, other):
        if other.distancecircle(self.position,self.radius)<maxradius:
            return True
        return False
    
    def __init__(self,pos,nature="",rad=0.0,color=(0.5,0.5,0.5)):
        self.position = pos
        self.radius = rad
        self.color = color
        self.classv = "empty"
        self.nature = nature

        Universe.object.append(self)
        
    
class obstacle(object):
    def nearobstacle(self, point, r=0):
        near = []
        if mag(self.position-point)<maxradius+self.radius+r:
            near.append(self)
        return near
        
    def linenearobstacle(self, other):
        p = other.closestpointline(self.position)
        if mag(p-self.position)<self.radius+maxradius:
            return True
        return False
            
        
    def __init__(self,pos,rad,h,color,nature=""):
        self.position = pos
        self.radius = rad
        self.height = h
        self.color = color
        self.nature = nature
        self.classv = "obstacle"

        try:
            f=open(Universe.settingspath,'a')
            f.write("\nobstacle "+" "+str(pos.x)+"  "+str(pos.z)+" "+str(h)+" "+str(color[0])+" "+str(color[1])+" "+str(color[2])+" "+str(rad))
            f.close()
        except TypeError:
            print "cannot save his work"
            return

        Universe.object.append(self)
    
class road(object):

    def nearobstacle(self, point,r=0):
        near = []
        for li in self.line:
            if li.distancepointline(point)<maxradius+r:
                near.append(li)
        return near
        
    def linenearobstacle(self, other):
	count=0
        for li in self.line:
            if other.intersectionWithLine(li)!=None:
                count+=1
		if count>=1:
		  return True
        return False
        
    def __init__(self,pos,size,color=[0.5,0.5,0.5]):
        self.position = pos
        self.length = size[0]
        self.height = size[1]
        self.width = size[2]
        self.color = color
        self.classv = "road"

        border0=(vector(pos.x-size[0]/2,0.0,pos.z-size[2]/2))
        border1=(vector(pos.x+size[0]/2,0.0,pos.z-size[2]/2))
        border2=(vector(pos.x+size[0]/2,0.0,pos.z+size[2]/2))
        border3=(vector(pos.x-size[0]/2,0.0,pos.z+size[2]/2))
        self.border = [border0,border1,border2,border3]
	self.bd = self.border
        self.line=[]
        for i in range(len(self.border)):
            li = line(self.border[i],self.border[(i+1)%len(self.border)])
            self.line.append(li)

        try:
            f=open(Universe.settingspath,'a')
            f.write("\nroad "+" "+str(pos.x)+"  "+str(pos.z)+" "+str(size[1])+" "+str(color[0])+" "+str(color[1])+" "+str(color[2])+" "+str(size[0])+ " "+str(size[2]))
            f.close()
        except TypeError:
            print "cannot save his work"
            return

        Universe.road.append(self)


