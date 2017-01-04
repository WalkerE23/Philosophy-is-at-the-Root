'''Written By Elliott Walker For Moat.com's interview process. 
This is the runToPhilosophy wikipedia game, wherein a web crawler clicks on the first non-italicized, not-in-parenthesis link available, 
in order to try and get to the philosophy page. 
This approach makes use of a dictionary/lookuptable, in order to cache known and popular articles leading to philosophy. 
Helps shorten amount of needed url calls; frequency map also included, to show the most popular nodes.'''

'''IMPORTANT!!!!
DEPENDANCIES: urllib, BeautifulSoup, math, and operator
'''

from web_crawler import WebCrawl
from lookuptable import LookupTable


def main(number_of_articles=10):
	wikiMap = LookupTable() #input number of times you want to run the article search.
	for i in range(number_of_articles):
		x = WebCrawl(wikiMap)
		x.runToPhilosophy()
	wikiMap.printAll()


main(10)