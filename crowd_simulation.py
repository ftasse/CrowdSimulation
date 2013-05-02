import Universe
from Environment import *
from Agent import *
from random import *
import sys

def randbuilding(num,ll=4,lu=6,hl=4,hu=6,wl=4,wu=6):
    positions = []
    for i in range(num):
      while True:
	rep=False
	p = vector(uniform(lmin,lmax),0,uniform(wmin,wmax))
	for o in positions:
	  if mag(o-p)<5:
	      rep=True
	if not rep:
	  positions.append(p)
	  break
      n = randint(0,len(Universe.intentions)-1)    
      nat = Universe.intentions[n]
      building(pos=p,size=[uniform(ll,lu),uniform(hl,hu),uniform(wl,wu)],nature=nat)
      
if __name__ == '__main__':

	number =int(sys.argv[1])
	buildnum = int(sys.argv[2])
	print "crowd simulation with crowd density "+str(number)+" agents, "+str(buildnum)+" buildings"

	Universe.erase()
	randbuilding(buildnum)

	for i in range(number):
		randomagent()

	while Universe.timeframe<Universe.numberofframes:
		Universe.timeframe+=1
		Universe.updatebucket()
		for a in Universe.agent:
			a.move()
	print "simulation over"
