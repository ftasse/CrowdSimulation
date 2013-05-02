#!BPY

"""
Name: 'Crowd simulation'
Blender: 245
Group: 'Import'
Tooltip: 'A Procedural Crowd Generator'
"""

__author__ = "Flora"
__url__ = ()
__version__ = "0.1"
__bpydoc__ = """Procedural crowd simulation: Once the plug-in is installed you can find it at File <- Import <- Crowd simulation. To use it, just click and a graphical interface will appear. You can modify the number of agents, the number of buildings and the number of frames. You can also create your own city before running the plug-in. Objects representing buildings should have the term ``Building'' in their name and a road object name should contain ``Road''. Press OK and wait. The crowd simulation is generated and drawn in the 3D view. You can add textures to the city by clicking on File <- Import <- City texturing. """

from scene_blender import *
import Blender
from Blender import *
from Blender.Window import *

import Universe
from random import *
from Environment import *
from Agent import *
import sys
import time

c = 5

lmax=Universe.lmax-c
lmin=Universe.lmin+c
wmax=Universe.wmax-c
wmin=Universe.wmin+c

def genbuilding(ll=3.5,lu=4,hl=5,hu=7,wl=4,wu=6):
    road(pos=vector(0,0,0),size=[1.5,0,40])
    road(pos=vector(0,0,0),size=[40,0,1.5])
    nat = ""
    building(pos=vector(6.0,0.0,6.0),size=[uniform(ll,lu),uniform(hl,hu),uniform(wl,wu)],nature=nat)
    building(pos=vector(6.0,0.0,14.0),size=[uniform(ll,lu),uniform(hl,hu),uniform(wl,wu)],nature=nat)
    #building(pos=vector(4.0,0.0,16.0),size=[uniform(ll,lu),uniform(hl,hu),uniform(wl,wu)],nature=nat)
    building(pos=vector(14.0,0.0,6.0),size=[uniform(ll,lu),uniform(hl,hu),uniform(wl,wu)],nature=nat)
    building(pos=vector(14.0,0.0,14.0),size=[uniform(ll,lu),uniform(hl,hu),uniform(wl,wu)],nature=nat)
    #building(pos=vector(10.0,0.0,16.0),size=[uniform(ll,lu),uniform(hl,hu),uniform(wl,wu)],nature=nat)
    #building(pos=vector(16.0,0.0,4.0),size=[uniform(ll,lu),uniform(hl,hu),uniform(wl,wu)],nature=nat)
    #building(pos=vector(16.0,0.0,10.0),size=[uniform(ll,lu),uniform(hl,hu),uniform(wl,wu)],nature=nat)
    #building(pos=vector(16.0,0.0,16.0),size=[uniform(ll,lu),uniform(hl,hu),uniform(wl,wu)],nature=nat)

    building(pos=vector(-6.0,0.0,6.0),size=[uniform(ll,lu),uniform(hl,hu),uniform(wl,wu)],nature=nat)
    building(pos=vector(-6.0,0.0,14.0),size=[uniform(ll,lu),uniform(hl,hu),uniform(wl,wu)],nature=nat)
    #building(pos=vector(-4.0,0.0,16.0),size=[uniform(ll,lu),uniform(hl,hu),uniform(wl,wu)],nature=nat)
    building(pos=vector(-14.0,0.0,6.0),size=[uniform(ll,lu),uniform(hl,hu),uniform(wl,wu)],nature=nat)
    building(pos=vector(-14.0,0.0,14.0),size=[uniform(ll,lu),uniform(hl,hu),uniform(wl,wu)],nature=nat)
    #building(pos=vector(-10.0,0.0,16.0),size=[uniform(ll,lu),uniform(hl,hu),uniform(wl,wu)],nature=nat)
    #building(pos=vector(-16.0,0.0,4.0),size=[uniform(ll,lu),uniform(hl,hu),uniform(wl,wu)],nature=nat)
    #building(pos=vector(-16.0,0.0,10.0),size=[uniform(ll,lu),uniform(hl,hu),uniform(wl,wu)],nature=nat)
    #building(pos=vector(-16.0,0.0,16.0),size=[uniform(ll,lu),uniform(hl,hu),uniform(wl,wu)],nature=nat)

    building(pos=vector(6.0,0.0,-6.0),size=[uniform(ll,lu),uniform(hl,hu),uniform(wl,wu)],nature=nat)
    building(pos=vector(6.0,0.0,-14.0),size=[uniform(ll,lu),uniform(hl,hu),uniform(wl,wu)],nature=nat)
    #building(pos=vector(4.0,0.0,-16.0),size=[uniform(ll,lu),uniform(hl,hu),uniform(wl,wu)],nature=nat)
    building(pos=vector(14.0,0.0,-6.0),size=[uniform(ll,lu),uniform(hl,hu),uniform(wl,wu)],nature=nat)
    building(pos=vector(14.0,0.0,-14.0),size=[uniform(ll,lu),uniform(hl,hu),uniform(wl,wu)],nature=nat)
    #building(pos=vector(10.0,0.0,-16.0),size=[uniform(ll,lu),uniform(hl,hu),uniform(wl,wu)],nature=nat)
    #building(pos=vector(16.0,0.0,-4.0),size=[uniform(ll,lu),uniform(hl,hu),uniform(wl,wu)],nature=nat)
    #building(pos=vector(16.0,0.0,-10.0),size=[uniform(ll,lu),uniform(hl,hu),uniform(wl,wu)],nature=nat)
    #building(pos=vector(16.0,0.0,-16.0),size=[uniform(ll,lu),uniform(hl,hu),uniform(wl,wu)],nature=nat)

    building(pos=vector(-6.0,0.0,-6.0),size=[uniform(ll,lu),uniform(hl,hu),uniform(wl,wu)],nature=nat)
    building(pos=vector(-6.0,0.0,-14.0),size=[uniform(ll,lu),uniform(hl,hu),uniform(wl,wu)],nature=nat)
    building(pos=vector(-14.0,0.0,-14.0),size=[uniform(ll,lu),uniform(hl,hu),uniform(wl,wu)],nature=nat)
    building(pos=vector(-14.0,0.0,-6.0),size=[uniform(ll,lu),uniform(hl,hu),uniform(wl,wu)],nature=nat)
    #building(pos=vector(-14.0,0.0,-14.0),size=[uniform(ll,lu),uniform(hl,hu),uniform(wl,wu)],nature=nat)
    #building(pos=vector(-10.0,0.0,-16.0),size=[uniform(ll,lu),uniform(hl,hu),uniform(wl,wu)],nature=nat)
    #building(pos=vector(-16.0,0.0,-4.0),size=[uniform(ll,lu),uniform(hl,hu),uniform(wl,wu)],nature=nat)
    #building(pos=vector(-16.0,0.0,-10.0),size=[uniform(ll,lu),uniform(hl,hu),uniform(wl,wu)],nature=nat)
    #building(pos=vector(-16.0,0.0,-16.0),size=[uniform(ll,lu),uniform(hl,hu),uniform(wl,wu)],nature=nat)

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

def gui():
    global evtNoEvt,evtagent,evtbuild,evtarm ,evtframe,evtToggle
    global agentnum ,buildingnum,armature,frames,toggle
    BGL.glRasterPos2i(10,360)  # position the cursor to write text
    Draw.Text("Press Q or ESC to quit.")
    agentnum = Draw.Number("Number of agents", evtagent, 10, 330, 160, 18, agentnum.val, 0, 10000, "Insert the crowd density")
    buildingnum = Draw.Number("Number of buidings",evtbuild,10, 310, 160, 18, buildingnum.val, 0, 20, "Insert the number of buildings")
    menuName = "Include Armature?%t|y %x1|n %x2"
    frames = Draw.Number("Frames", evtframe, 10, 290, 160, 18, frames.val, 1, 10000, "Insert the number of frames")
    toggle = Draw.Toggle("OK", evtToggle, 10, 250, 160, 18, toggle.val, "Submit the parameters")

def event(evt, val):  # function that handles keyboard and mouse events
    if evt == Draw.ESCKEY or evt == Draw.QKEY:
        stop = Draw.PupMenu("OK?%t|Stop script %x1")
        if stop == 1:
            Draw.Exit()
            return
def buttonEvt(evt):  # function that handles button events
    global evtNoEvt,evtagent,evtbuild,evtarm ,evtframe,evtToggle
    global agentnum ,buildingnum,armature,frames,toggle
    if evt == evtToggle:
        generate()
	Draw.Exit()
    if evt:
        Draw.Redraw()

if __name__ == '__main__':
    for obj in Object.Get():
      name=obj.getName()
      if name.find("Building")!=-1:
	p = obj.getLocation()
	x = obj.SizeX
	y = obj.SizeY
	z = obj.SizeZ
	n = randint(0,len(Universe.intentions)-1)
        nat = Universe.intentions[n]
	building (pos = vector(p[0],p[1],p[2]), size=(x,y,z),color=(0.5,0.5,0),nature=nat,draw=False)
      if name.find("Road")!=-1:
	p = obj.getLocation()
	x = obj.SizeX
	y = obj.SizeY
	z = obj.SizeZ
	road (pos = vector(p[0],p[1],p[2]), size=(x,y,z),color=(0.5,0.5,0))
    
    evtNoEvt   = 0
    evtagent  = 1
    evtbuild  = 2
    evtframe = 4
    evtToggle  = 5
    # Initial values of buttons:
    agentnum = Draw.Create(0)
    buildingnum = Draw.Create(0)
    frames = Draw.Create(250)
    toggle = Draw.Create(1)
    Draw.Register(gui, event, buttonEvt)
    

def generate():
    print "simulation with "+str(agentnum.val)+" agents and "+str(buildingnum.val) + " buildings"
    start = time.clock()
    Universe.erase()
    
    
    DrawProgressBar(0.0, "Generating buildings ...")
    randbuilding(buildingnum.val)
    #genbuilding()
    DrawProgressBar(1.0, "Finish Generating buildings ...")
        
    for i in range(agentnum.val):
        a = randomagent()
	DrawProgressBar(i/agentnum.val, "Generating agents ...")
	
    while Universe.timeframe<frames.val:
	Universe.timeframe+=1
	Universe.updatebucket()
	for a in Universe.agent:
	    a.move()
	    a.bmotion.color = a.maingoal.color
	DrawProgressBar(0.8+Universe.timeframe/frames.val, "Generating frames ...")

    draw()

    
    stop = time.clock()
    diff = stop-start
    print "Time elapsed ",diff
    print "simulation over"

