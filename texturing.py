#!BPY

"""
Name: 'City Texturing'
Blender: 245
Group: 'Import'
Tooltip: 'A Procedural Texturing of a city'
"""

__author__ = "Flora"
__url__ = ()
__version__ = "0.1"
__bpydoc__ = "Empty"

import Universe
from Blender import *
from random import *
import os

if os.name=="nt":
	textures = Universe.dirpath+"/textures/"
else:
	textures = Universe.dirpath+"/textures//"
worldnum = 1
landnum = 1
roadnum = 1
buildnum = 1 


############ World material ###################
tnum = abs(int(random() * worldnum) + 1)
tid = "Sky%d"%tnum
Library.Open(textures + tid + ".blend")
Library.Load(tid, 'World')
Scene.GetCurrent().world = World.Get(tid)

############ Landscape material ###################
tnum = abs(int(random() * landnum) + 3)
tid = "Landscape%d"%tnum
Library.Open(textures + tid + ".blend")
Library.Load(tid, 'Material')
matt = Material.Get(tid)
matt.spec = 0
matt.ref = 0.3
matt.amb = 0.09
ob = Object.Get("landscape")
me = ob.getData(False, True)
me.materials = [matt]	
ob.setMaterials([matt])

###### Road material ############
tnum = abs(int(random() * roadnum) + 2)
tid = "Road%d"%tnum
Library.Open(textures + tid + ".blend")
Library.Load(tid, 'Material')
matt = Material.Get(tid)
matt.spec = 0
matt.ref = 0.3
matt.amb = 0.09
for ob in Object.Get():
	if ob.getName().find("Road")!=-1:
		me = ob.getData(False, True)
		me.materials = [matt]	
		ob.setMaterials([matt])

###### Wall material ############
tnum = abs(int(random() * buildnum) + 2)
tid = "Wall%d"%tnum
Library.Open(textures + tid + ".blend")
Library.Load(tid, 'Material')
matt = Material.Get(tid)
matt.spec = 0
matt.ref = 0.3
matt.amb = 0.09
for ob in Object.Get():
	if ob.getName().find("Building")!=-1:
		me = ob.getData(False, True)
		me.materials = [matt]	
		ob.setMaterials([matt])


for m in Material.Get():
	m.setAmb(0.08)
	m.setSpec(0.0)