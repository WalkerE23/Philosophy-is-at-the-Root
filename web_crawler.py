'''Web Crawler module will search along valid links, to find the distance to the endpoint. it can also be given a URL for testing or curiosity.'''

import urllib
from BeautifulSoup import BeautifulSoup


BASE = "https://en.wikipedia.org"
PHILOSOPHY = "https://en.wikipedia.org/wiki/Philosophy"

class WebCrawl:
	def __init__(self,lookupTable,url=None):
		self.sitesVisited = []
		self.sitesVisitedCount = 0
		self.lookup = lookupTable
		if(url):
			self.currentURL = url
		else:
			self.currentURL = "https://en.wikipedia.org/wiki/Special:Random"


	def getTitle(self,parsedHTML):
		'''Returns the title of the article. important, as the lookup table uses the title, not url'''
		#there is an issue with ascii vs unicode in some instances, where non-english proper nouns cannot be converted to str.
		try:
			return str(parsedHTML.find('h1',{'id':'firstHeading'}).getText())
		except:
			return unicode(parsedHTML.find('h1',{'id':'firstHeading'}).getText())

	def runToPhilosophy(self):
		'''Main driver for the web crawler to get to the philosophy page'''
		#after each iteration, methods from the lookup table are called to update the growing wiki map. 

		while self.currentURL != PHILOSOPHY:
			#set up each stage. get html from page, find the title of the article, and update the pointer to the next url
			parsedHTML 		= BeautifulSoup(urllib.urlopen(self.currentURL))
			title 			= self.getTitle(parsedHTML)
			self.currentURL = BASE + str(self.findFirstLink(parsedHTML))

			#display current steps
			print title + " : %d " % self.sitesVisitedCount

			#sometimes there is no link, and the article is a stub. 
			if(self.findFirstLink(parsedHTML)):
				#there is a next article: check if it has been seen before
				if(self.lookup.doesContain(title)):
					#this article is in the lookup table, we know it's distance and do not have to keep going.
					knownDist = self.lookup.hitFamiliarEndpoint(title,self.sitesVisited)
					break
				else:
					#this article is new, so we should process it. 
					knownDist = 0 #in the case of the first few runs, the lookup table will be empty
					self.lookup.addToNewStrand(title,self.sitesVisited)
					self.sitesVisited.append(title)
					self.sitesVisitedCount += 1
			else:
				#the article is a stub, or has no valid link
				#invoke method to mark all endpoints as infinite distance
				self.lookup.hitDeadEnd(self.sitesVisited)
				print "HIT DEAD END, THESE ENDPOINTS DONT LEAD TO PHILOSOPHY"
				return

		#exiting the while loop means that philosophy is hit
		print "TOTAL NUMBER OF STEPS TAKEN: " + str(self.sitesVisitedCount + knownDist)
		return


	def findFirstLink(self,parsedHTML):
		'''returns the first valid link'''
		# this process gets hairy because of an edge case. in some articles, there are tables off to the side, 
		#and simply searching for a paragraph tag can lead to the 'first valid link' being a reference from that table. there is no 
		#markup that makes the distinction between main text, and the table to the side. 
		#solution: narrow down using id:mw-content-text, serching for only direct children(non recursive), 
		#and only looking in <p> tags from there. this circumvents the afformentioned table

		wikipediaMainContent = parsedHTML.find('div',{'id':'mw-content-text'}).findChildren(recursive=False)

		for paragraph in wikipediaMainContent:
			if(paragraph.name == 'p'):
				listOfLinks = self.getValidLinks(paragraph) #check what links are in this paragraph. most of the time, its in the first iteration, but not always.

				if(not listOfLinks):
					#this paragraph did not contain any valid links
					pass
				else:
					#this one did have a valid link, and we want the first one!
					#exit the iteration
					return listOfLinks[0]
		return None


	def getValidLinks(self,body):
		'''this method will return a list with all valid links from one paragraph, or an empty list'''
		#Valid links are not inisde parenthesis, are not italic, and are not in refrences
		#Iterates through the parsed paragraph. looks for strings that contain open or closed parenthesis. 
		#	it will not proceed with 'interior' elements if they are within any set of yet to be closed parenthesis. 
		#Tag of element is checked, and only pure links are accepted. links within italics (<i> tag) are not valid, nor are wiki refrences (<sup> tag)

		result = []
		unevenParens = 0
		for i in body:
			#iterate all BS elements in given paragraph
			if(str(type(i)) == "<class 'BeautifulSoup.NavigableString'>"):
				#pure string, ie not enclosed in a tag and sometimes containing parenthesis, are of type <class 'BeautifulSoup.NavigableString'>
				#quick and dirty way to know if we are in parens at the moment, or not.
				if("(" in i):
					unevenParens += 1
				if(")" in i):
					unevenParens -= 1
			elif((str(type(i)) == "<class 'BeautifulSoup.Tag'>") and (unevenParens == 0)): #unevenParens == 0 means that we are valid.
				#html elements are of the type <class 'BeautifulSoup.Tag'>
				if(i.name == 'a'):
					#we only care about links, not italics, not spans, not sup
					result.append(str(i['href']))
		return result
		#other way to do this: return first one you come across, no list needed


