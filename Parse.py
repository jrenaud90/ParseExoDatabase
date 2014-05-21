#Imports
from HTMLParser import HTMLParser
import time,os,inspect

#Functions
def deleteContent(pfile): #Delete File Contents
    pfile.seek(0)
    pfile.truncate()
	return pfile

#Global Vars
now = time.strftime("%c")
excFilePath = inspect.getfile(inspect.currentframe()) # script filename (usually with path)

#Open and use log file
path = excFilePath + '/Output.log'
filetmp = open(path,'w')
log = deleteContent(filetmp)
LogStartStr = 'Exoplanet HTML Database Parse Ver 0\nScript by Joe Renaud\nLog file created on: ' + now + '\n\n' + '1-Begin...\n'
log.write(LogStartStr)
# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print "Encountered a start tag:", tag
    def handle_endtag(self, tag):
        print "Encountered an end tag :", tag
    def handle_data(self, data):
        print "Encountered some data  :", data

# instantiate the parser and fed it some HTML
parser = MyHTMLParser()
parser.feed('<html><head><title>Test</title></head>'
            '<body><h1>Parse me!</h1></body></html>')