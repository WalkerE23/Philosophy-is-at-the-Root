'''This is the LookupTable module, which is a dictionary of all visited nodes, their distance to the endpoint, and frequency of how many times each of these is hit. 
the display method compiles some basic statistics, and shows, in descending order, the distances and frequencies of each node.'''
from math import sqrt
import operator

class LookupTable:
	def __init__(self):
		self.visited_stepsToEnd = {}
		self.visited_nodeFrequency = {}
		self.deadEnds = 0

	def printAll(self):
		sorted_ste 	= 	self.getSorted(self.visited_stepsToEnd)
		sorted_nf 	= 	self.getSorted(self.visited_nodeFrequency)

		print"@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
		print"@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
		print "=======DISTANCE FROM PHILOSOPHY FOR EACH NODE==================="
		for entry in sorted_ste:
  			print entry[0],entry[1]
  		print "=======FREQUENCY OF EACH NODE - DESC ORDER======================"
  		for entry in sorted_nf:
  			print entry[0],entry[1]
  		print "=======STATISTICS ON SEARCH PATH RESULTS========================"
  		print "MEAN: %d, STANDARD DEVIATION: %d, VARIANCE: %d" % self.compileStatsOnMap(self.visited_stepsToEnd)
  		print "THREE MOST COMMON: %s,%s,%s, FARTHEST AWAY: %s" % sorted_nf[0],sorted_nf[1],sorted_nf[2],sorted_ste[0]
		print"@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
		print"@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"



	def compileStatsOnMap(self, myMap):
		'''returns mean, standard deviation and variance of path distances'''
		myList = []
		for i in myMap:
			myList.append(myMap[i])
		mean = sum(myList)/len(myList)
		print mean
		var = 0
		for j in myList:
			var += ((j-mean)**2)
		var /= len(myList)
		stdev = sqrt(var)
		return (mean,var,stdev)


	def getSorted(self,myMap):
		'''return sorted array of a map'''
		sorted_array = sorted(myMap.items(), key=operator.itemgetter(1),reverse=True)
		return sorted_array

	def doesContain(self, title):
		'''check if article has been visited'''
		if(title in self.visited_stepsToEnd):
			return True
		else:
			return False

	def addToNewStrand(self,title,list):
		'''add a new node to the LookupTable'''
		self.visited_stepsToEnd[title] = 1
		self.visited_nodeFrequency[title] = 1
		for i in list:
			self.visited_stepsToEnd[i] += 1
		return

	def hitFamiliarEndpoint(self,title,list):
		'''process the node if it is familiar, and return the known distance to the endpoint'''
		knownDist = self.visited_stepsToEnd[title]
		self.visited_nodeFrequency[title] += 1
		for i in list:
			self.visited_stepsToEnd[i] += knownDist
		return knownDist
	def hitDeadEnd(self,list):
		knownDist = 0
		for i in list:
			self.visited_stepsToEnd[i] = knownDist
		self.deadEnds += 1
