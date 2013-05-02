

import Universe
from Environment import *
from Tools import *

class globalbehaviour(object):
    def findtopdesires(self):
        topdes = []
        j=0
        while len(topdes)<3:
            top=None
            topvalue =0.0
            for val in self.state:
                i = self.state.index(val)
                if (i not in topdes)  and (val > topvalue):
                    topvalue = val
                    top = i
            if top!=None:
                topdes.append(top)
            else:
                break
	if len(topdes)==0:
	    topdes = [0]  
        return topdes

        
    def updatestates(self):
        for i in range(len(self.state)):
            self.state[i]=Universe.updatestate(i,self.state[i])
        
    def findintention(self,position):
	if self.desire!=None:
            self.state[self.desire]=0
        #desires = self.findtopdesires()
        #length = len(desires)
	desires=self.state
	length = len(desires)
        ratios = []
        goals= []
	for  i in range(length):
            nearestgoal = None
            dist = 10000
            #for g in Universe.object:
                #if g.nature == Universe.intentions[desires[i]] and mag(g.position-position)<dist:
                    #dist = mag(g.position-position)
                    #nearestgoal = g
            #for g in Universe.agent:
                #if g.nature == Universe.intentions[desires[i]] and mag(g.position-position)<dist:
                    #nearestgoal = g
                    #dist = mag(g.position-position)
            #goals.append(nearestgoal)
            #ratios.append(self.state[desires[i]]/(dist+0.001))
	    for g in Universe.object:
                if g.nature == Universe.intentions[i] and mag(g.position-position)<dist:
                    dist = mag(g.position-position)
                    nearestgoal = g
            for g in Universe.agent:
                if g.nature == Universe.intentions[i] and mag(g.position-position)<dist:
                    nearestgoal = g
                    dist = mag(g.position-position)
	    if nearestgoal==None:
	      nearestgoal = Universe.object[0]
            goals.append(nearestgoal)
	    if i==self.desire:
	      dist = 100000
            ratios.append(self.state[i]/(dist+0.001))
        maxRatio = max(ratios)
	for  i in range(length):
            if maxRatio == ratios[i]:
                self.desire = i
                self.goal=goals[i]
                return self.goal
                
        
    def findgoal():
        ## Bouml preserved body begin 0001FEE4
        pass
        ## Bouml preserved body end 0001FEE4
        
    def __init__(self):
        self.state = []
        self.belief = None
        self.emotion = None
        self.intention = None
        self.goal = None
        self.desire=None
        for i in range(len(Universe.states)):
	    val = uniform(0.0,1.0/len(Universe.states))
	    #print val
            self.state.append(val)

##        for i in range(len(Universe.beliefs)):
##            self.belief.append(uniform(0.0,1/len(Universe.beliefs)))
##
##        for i in len(Universe.emotions):
##            self.belief.append(uniform(0.0,1/len(Universe.beliefs)))
##
##        for i in len(Universe.intentions):
##            self.intention.append(uniform(0.0,1/len(Universe.intentions)))

        
    
