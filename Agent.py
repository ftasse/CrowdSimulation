import Universe
from BasicMotion import *
from LocalBehaviour import *
from GlobalBehaviour import *

from random import random,uniform

c = 3

def randomagent(ll=lmin,lu=lmax,wl=wmin,wu=wmax,red=random(),green=random(),blue=random(),nat = "agent"):
    xx = uniform(ll,lu)
    yy =0
    zz = uniform(wl,wu)
    return agent(pos = vector(xx,yy,zz), rad=uniform(Universe.minradius,Universe.maxradius), h=uniform(2,3), color=(red,green,blue),nature=nat)


class agent(object):
    def update_goal(self):
        #if self.classv=="agent":
	    #if self.nature=="agent":
	      #self.gbehaviour.state[3]=0
	    #else:
	      #self.gbehaviour.state[0]=0
	      #self.gbehaviour.state[1]=0
	      #self.gbehaviour.state[2]=0
	      #self.gbehaviour.state[3]=1	
	self.maingoal = self.gbehaviour.findintention(self.position)
	if  self.maingoal.classv=="building":
	    self.bmotion.stopdist=0.0
        if self.maingoal.classv in ["agent","obstacle","empty"]:
            self.bmotion.stopdist=self.maingoal.radius
        
    def update_path(self):
	try:
          if self.nature=="car":
		  self.color = [random(),random(),random()]
		  self.position = vector(-19,0,0)
		  self.path=[self.maingoal.position]
		  return
	  self.path = self.lbehaviour.findpath(self.position,self.maingoal.doorpos)
	  self.path.insert(0,self.maingoal.position)
 	except KeyError:
	  self.path = [self.maingoal.position,self.maingoal.doorpos]
	#print self.path
	#print "pos ",self.position
	#print "door ",self.maingoal.doorpos
	#print "goal ",self.maingoal.position
        
    def move(self):
        if self.bmotion.goals == [] and self.nature!="car":
	    self.update_goal()
	    #print "Agent ",Universe.agent.index(self),": ",self.maingoal.nature
	    self.path=[]
      
        if self.path==[]:
	    self.update_path()
	    if len(self.path)==0:
	      self.path = [self.maingoal.position]
            self.bmotion.goals = self.path

	if self.maingoal.classv=="agent":
	    self.bmotion.goals = [self.maingoal.position]

        self.bmotion.update_position()
        self.gbehaviour.updatestates()
        self.position = self.bmotion.position
        self.velocity = self.bmotion.velocity
        self.orientation = self.bmotion.orientation
        
        

        
        
    def __init__(self,pos,rad,h,color,nature=""):
	nat=nature
        self.position = pos
        self.velocity = vector(0,0,0)
        self.radius = rad
        self.color = color
        self.orientation = 0
        self.classv = "agent"
	if nat=="":
		self.nature = "agent"
	else:
		self.nature=nat
	Universe.agent.append(self)

        id = Universe.agent.index(self)
        self.maingoal = None
        self.path = []
        self.bmotion = basicmotion(id,pos,rad,color)
        self.lbehaviour = localbehaviour()
        self.gbehaviour = globalbehaviour()
        
        try:
            f=open(Universe.settingspath,'a')
            f.write("\nagent "+" "+str(pos.x)+"  "+str(pos.z)+" "+str(h)+" "+str(color[0])+" "+str(color[1])+" "+str(color[2])+" "+str(rad))
            f.close()
        except TypeError:
            print "cannot save his work"
            return


