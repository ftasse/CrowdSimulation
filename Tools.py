from math import *

_TINY = 1e-5

class vector(object):
	"""A vector class"""

	def __init__(self,x,y,z):
		self.x = float(x)
		self.y = float(y)
		self.z = float(z)

	def __repr__(self):
		"""Vector representation"""
		return "<vector " + str(self.x) + " " + str(self.y)+ " " + str(self.z) + ">"

	def __add__(self, vec):
		return vector(self.x+vec.x,self.y+vec.y,self.z+vec.z)

	def __neg__(self):
		return vector(-self.x,self.y,-self.z)

	def __sub__(self, vec):
		return vector(self.x-vec.x,self.y-vec.y,self.z-vec.z)

	def __mul__(self, c):
		return vector(self.x*c,self.y*c,self.z*c)

	def __rmul__(self, c):
		return vector(self.x*c,self.y*c,self.z*c)

	def __div__(self, c):
		return vector(self.x/c,self.y/c,self.z/c)

	def __rdiv__(self, c):
		return vector(c/self.x,c/self.y,c/self.z)

	def __eq__(self, other):
		return mag(self-other) < _TINY



def mag(vec):
	return sqrt(vec.x*vec.x +vec.y*vec.y +vec.z*vec.z)

def norm(vec):
	return vec/mag(vec)

def dot(vec1, vec2):
	return vec1.x*vec2.x +vec1.y*vec2.y +vec1.z*vec2.z

def angleVec(vec1, vec2):
	result = -(atan2(vec1.z, vec1.x) - atan2(vec2.z, vec2.x)) * 180.0/pi;
	if(result < 0):
		result += 360.0;
	return result

def perpendicular(vec):
	return vector(-vec.z,0.0, vec.x)



class line(object):
	def closestpointline(self,point):
		vec = self.end-self.start
		offset = point-self.start
		c1 = dot(offset,vec)
		if c1<=0:
			return self.start
		c2 = dot(vec,vec)
		if c2<=c1:
			return self.end
		t = c1/c2
		return self.start+t*(vec)

	def distancepointline(self,point):
		return mag(point-self.closestpointline(point))

	def normalpointline(self,point):
		other = self.closestpointline(point)
		offset = perpendicular(norm(-self.end+self.start))
		return other+offset

	def intersectionWithLine(self,line):

		start1 = self.start
		end1 = self.end
		start2 = line.start
		end2 = line.end
		denom =  (end2.z -start2.z)*(end1.x -start1.x)- (end2.x -start2.x )*(end1.z -start1.z)
		if denom!= 0 :
			a = ((end2.x -start2.x)*(start1.z -start2.z)- (end2.z -start2.z)*(start1.x -start2.x))/denom
			b = ((end1.x -start1.x)*(start1.z -start2.z)- (end1.z -start1.z)*(start1.x -start2.x))/denom
			if a>=0.0 and a<=1 and b>0 and b<1:
				return start1 + a*(end1-start1)
			else:
				return None
		else:
			return None

	def nearlineline(self,line,radius):
		d1 = self.distancepointline(self.start)
		d2 = self.distancepointline(self.end)
		d3 = self.distancepointline((self.start+self.end)/2.0)
		if self.intersectionWithLine(line)==None:# and min(d1,d2,d3)>radius:
			return False
		return True


	def distancecircle(self,point,radius):
		other = self.closestpointline(self,point)
		return abs(mag(point,other)- radius)

	def cut(self):
		val=[]
		for t in range(6):
			val.append(self.start+(t/5)*(self.end-self.start))
		return val

	def __init__(self,s,t):
		self.start=s
		self.end=t
		self.classv="line"
		self.points = self.cut()

	def __str__(self):
		return str([self.start,self.end])

	def __repr__(self):
		"""Line representation"""
		return str([self.start,self.end])




class graph(object): # based on python-graph library
	def __init__(self):
		self.nodes = {}
		self.edges = {}

	def __str__(self):
		return "<graph " + str(self.nodes) + " " + str(self.edges) + ">"

	def __iter__(self):
		for n in self.nodes.iterkey:
			yield n

	def __getitem__(self,node):
		for n in self.nodes[node]:
			yield n

	def get_nodes(self):
		return self.nodes.keys()

	def get_neighbors(self,node):
		return self.nodes[node]

	def get_edges(self):
		return self.edges.keys()


	def has_node(self, node):
		return self.nodes.has_key(node)

	def addnode(self, node):
		n = (node.x,node.z)
		if (not n in self.nodes.keys()):
			self.nodes[n] = []

	def addnodes(self, nodelist):
		for each in nodelist:
			self.addnode(each)

	def addedge(self, n1, n2,label=''):
		u = (n1.x,n1.z)
		v = (n2.x,n2.z)
		try:
			if not (v in self.nodes[u] or u in self.nodes[v]):
			    self.nodes[u].append(v)
			    self.nodes[v].append(u)
			    wt = mag(vector(u[0],0,u[1])-vector(v[0],0,v[1]))
			    self.edges[(u, v)] = [label, wt]
			    self.edges[(v, u)] = [label, wt]
		except KeyError:
			print "cannot add edge"
			return

	def deletenode(self, n):
		#node =(n.x,n.y)
		for each in list(self.get_neighbors(node)):
			self.deleteedge(each, node)
			del(self.nodes[node])

	def deleteedge(self, u, v):
		self.nodes[u].remove(v)
		self.nodes[v].remove(u)
		del(self.edges[(u,v)])
		del(self.edges[(v,u)])

	def get_edge_weight(self, u, v):
		return self.edges[(u, v)][1]

	def set_edge_weight(self, u, v,weight):
		self.edges[(u, v)][1] = weight
		self.edges[(v, u)][1] = weight

	def set_edge_label(self, u, v,label):
		self.edges[(u, v)][0] = label
		self.edges[(v, u)][0] = label

	def has_edge(self, u, v):
		return self.edges.has_key((u,v)) and self.edges.has_key((v,u))

	def shortestpath(self, source):
		# Initialization
		dist	 = { source: 0 }
		previous = { source: None}
		q = self.get_nodes()

		# Algorithm loop
		while q:
			# examine_min process performed using O(nodes) pass here.
			# May be improved using another examine_min data structure.
			u = q[0]
			for node in q[1:]:
				if ((not dist.has_key(u)) 
				    or (dist.has_key(node) and dist[node] < dist[u])):
					u = node
			q.remove(u)

			# Process reachable, remaining nodes from u
			if (dist.has_key(u)):
				for v in self[u]:
					if v in q:
						alt = dist[u] + self.get_edge_weight(u, v)
						if (not dist.has_key(v)) or (alt < dist[v]):
							dist[v] = alt
							previous[v] = u
		return previous, dist

	def findpath(self, n1, n2):
		node1 = (n1.x,n1.z)
		node2 = (n2.x,n2.z)
		path = []
		p = node2
		while not p==node1:
			path.append(p)
			p=self.shortestpath(node1)[0][p]
		#path.reverse()
		for v in path:
			if v == node1:
				path.remove(v)
		#print "true path", path
		newpath = []
		for g in path:
			newpath.append(vector(g[0],0,g[1]))
		return newpath



if __name__ == '__main__':     
	node1 = vector(0,0,0)
	node2 = vector(2,0,0)
	node3 = vector(0,0,-1)
	node4 = vector(2,0,2)
	nodes = [node1,node2,node3,node4]
	my = graph()
	my.addnodes(nodes)
	my.addedge(node1,node2)
	my.addedge(node2,node3)
	my.addedge(node3,node4)
	print my.findpath(node1,node4)
	print angleVec(node3,node4)
	p = perpendicular(node2-node4)
	print p
	print angleVec(p,vector(1,0,1))
	print node1==vector(0,0,1e-16)
	print line(node1,node2)



