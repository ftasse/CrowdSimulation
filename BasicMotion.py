

import Universe
import math
from Environment import *
from LocalBehaviour import *
from Tools import *
      

dt = 1.0/Universe.fps
framepath=Universe.framepath

class basicmotion(object):
    def __init__(self,id,pos,rad,color,p=0.3,q=0.0):
        self.id = id
        self.position = pos
        self.radius = rad
        self.color = color
        self.orientation = 0
        self.priority = len(Universe.agent)
        self.velocity = vector(0,0,0)
        self.p = p
        self.q = q
        self.nearby = []
        self.nearby_ob = []
        self.goals = []
        self.stopdist = 0
	self.wait = 0
	self.ok = True

        self.speed= uniform(Universe.minspeed,Universe.maxspeed)
        self.direction = vector(0,0,0)
        self.mass = 80
        self.chartime = 0.5
        self.A = 2000
        self.B = 0.15
        self.K = 120000
        self.k = 240000

    def attract_target(self):
        target = self.goals[len(self.goals)-1]
        direction = norm(target-self.position)
        tot = 0
        average = vector(0,0,0)
        for b in self.nearby:
            if mag(self.position-b.position)<=2:
                average+=self.direction
                tot+=1
        if tot!=0:
            average/=tot
        self.direction = norm((1-self.p)*direction + self.p*average)

        force = self.mass*((self.speed*self.direction - self.velocity)/self.chartime)
        return force

    def repulse_agent(self):
        force = vector(0,0,0)
        for b in self.nearby:
	    if not b.position==self.position:
		nij = norm(self.position - b.position)
		tij = vector(-nij.z,0,nij.x)
		dvji = dot(b.velocity-self.velocity,tij)
		rij = self.radius + b.radius
		dij = mag(self.position - b.position)
		if dij>rij:
			g=0
		else:
			g = rij - dij
		f = ( self.A*exp((rij-dij)/self.B) + self.k*g ) * nij + self.K*g*dvji*tij
            	force+=f
        return force

    def repulse_wall(self):
        force = vector(0,0,0)
        for b in self.nearby_ob:
            if b.classv == "line":
                vec = b.start - b.end
                niw = norm(perpendicular(vec))
                tiw = vector(-niw.z,0,niw.x)
                ri = self.radius
                diw = b.distancepointline(self.position)
                if diw>ri:
                    g=0
                else:
                    g = ri - diw
		B=0.01
                f = ( self.A*exp((ri-diw)/B) + self.k*g ) * niw - self.K*g*dot(self.velocity,tiw)*tiw
                force+=f
        return force
                

        
    def findnearby(self):
        near = []
        for b in Universe.agent:
            pos = b.position #+b.velocity*dt
            if not(self.position==b.position) and mag(self.position-pos)<2.0+(self.radius+b.radius): #and self.infront(b,110)
                near.append(b)
        return near

    def findnearby2(self):
        self.neary = []
        near = []
        val = []
        w = int(self.position.x % Universe.cellw)
        h = int(self.position.z % Universe.cellh)
        val.extend(Universe.bucket[w][h])
        #self.nearby_ob.extend(Universe.env[w][h])
        if w>0:
            val.extend(Universe.bucket[w-1][h])
            #self.nearby_ob.extend(Universe.env[w-1][h])
            if h>0:
                val.extend(Universe.bucket[w-1][h-1])
                #self.nearby_ob.extend(Universe.env[w-1][h-1])
            if h<Universe.cellh-1:
                val.extend(Universe.bucket[w-1][h+1])
                #self.nearby_ob.extend(Universe.env[w-1][h+1])
        if h>0:
            val.extend(Universe.bucket[w][h-1])
            #self.nearby_ob.extend(Universe.env[w][h-1])
            
        if w<Universe.cellw-1:
            val.extend(Universe.bucket[w+1][h])
            #self.nearby_ob.extend(Universe.env[w+1][h])                      
            if h<Universe.cellh-1:
                val.extend(Universe.bucket[w+1][h+1])
                #self.nearby_ob.extend(Universe.env[w+1][h+1])
            if h>0:
                val.extend(Universe.bucket[w+1][h-1])
                #self.nearby_ob.extend(Universe.env[w+1][h-1])
                
        if h<Universe.cellh-1:
            val.extend(Universe.bucket[w][h+1])
            #self.nearby_ob.extend(Universe.env[w][h+1])

        temp = []
        for i in val:
            if i!=self.id and not i in temp:
                near.append(Universe.agent[i])

##        near = []
##        near.extend(Universe.agent)
##        for a in near:
##            if self.position==a.position:
##                near.remove(a)
        return near
       
    def findnearby_ob2(self):
        near = []
        for o in Universe.object:
            near.extend(o.nearobstacle(self.position,2.0))
        return near

    def findnearby_ob(self):
        near = self.nearby_ob
        temp = []
        for o in near:
            if not o in temp:
                temp.append(o)
            else:
                near.remove(o)
        return near
                
        
    def infront(self, other,angle):
        if angleVec(self.velocity,other.velocity)<angle:
            return True
        else:
            return False
        
    def seek(self):
        target = self.goals[len(self.goals)-1]
        seek = target - self.position
        seek = norm(seek)
        return (seek-self.velocity)/0.5
        
    def separate(self):
        sep = vector(0,0,0)
        for b in self.nearby:
            rab=self.position-b.position
            rij = self.radius+b.radius
            dij = mag(rab)
            if rij-dij>=0:
                n = rij-dij
            else:
                n=0
            sc = A*exp(B*(rij-dij)) + K*n*(rij-dij)
            f = sc*norm(rab)
            
            sep+=f
        return sep
            
        
    def align(self):            #dummy
        align = vector(0,0,0)
        for b in self.nearby:
            pos = b.position+b.velocity*dt
            align+=norm(self.position-b.pos)
##        if mag(align)>0:
##            align = norm(align)
        return align
        
    def circleavoid(self):
        force = vector(0.0,0.0,0.0)
        for b in self.nearby_ob:
            if b.classv=="obstacle":
                rab=self.position-b.position
                rij = self.radius+b.radius
                dij = mag(rab)
                if rij-dij>=0:
                    n = rij-dij
                else:
                    n=0
                sc = A*exp(B*(rij-dij)) + K*n*(rij-dij)
                f = sc*norm(rab)
                force+=f
        return force
        
    def lineavoid(self):
        force = vector(0.0,0.0,0.0)
        for l in self.nearby_ob:
            if l.classv=="line":
                b = l.closestpointline(self.position)
                rab=self.position-b
                rij = self.radius
                dij = mag(rab)
                if rij-dij>=0:
                    n = rij-dij
                else:
                    n=0
                sc = (A-2)*exp(B*(rij-dij))+ K*n*(rij-dij)
                f = sc*norm(rab)
                force+=f
        return force
        
    def update_position(self):
        target = self.goals[len(self.goals)-1]
	#print mag(self.goals[0]-self.position)
        if  len(self.goals)>1 and mag(target-self.position)<0.05+self.radius:
            self.position = target
            self.goals.pop()
            arm = "walk"
        elif len(self.goals)==1 and mag(target-self.position)<self.stopdist+self.radius:
	    #if self.wait<31:
	      #self.wait+=1
	    #else:
	      #self.wait=0
	    self.position = target
	    self.goals.pop()
            arm = "stand"
        else:
            arm = "walk"
            self.nearby = self.findnearby2()
            self.nearby_ob = self.findnearby_ob2()
        
            
            forces = self.attract_target()+(self.repulse_agent()+self.repulse_wall())
            self.velocity+=forces*dt/self.mass
            if mag(self.velocity)>self.speed:
                self.velocity=self.speed*norm(self.velocity)
            self.position+=self.velocity*dt

        direction = vector(0,0,0)
        if mag(self.velocity)!=0.0:
            direction = norm(self.velocity)
        dp = dot(direction,vector(0,0,1))
        radian = math.acos(dp)
        angle = (radian / math.pi) * 18 #For some insane reason these are degrees divided by ten (should be *180)
        if (direction.x < 0): angle = -1 * angle
        self.orientation = angle

        try:
            file = open(framepath,'a')
            file.write("\n"+str(self.id)+" "+str(self.position.x)+" "+str(self.position.z)+" "+str(self.orientation)+" "+str(arm)+" "+str(Universe.timeframe)+" "+str(self.color[0])+" "+str(self.color[1])+" "+str(self.color[2]))
            file.close()
        except TypeError:
            return
     
        
        
    
    
