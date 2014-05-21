#Imports
from HTMLParser import HTMLParser
import time,os,inspect,urllib2

#Functions
def deleteContent(pfile): #Delete File Contents
    pfile.seek(0)
    pfile.truncate()
    return pfile

#Global Vars
now = time.strftime("%c")
excFilePath = inspect.getfile(inspect.currentframe()) #Finds current file path including file name.

#Open and use log file
path = excFilePath.replace("Parse.py", "") + 'Output.log' #Gets rid of current file name and replaces it with log name, change parse.py to current file name.
filetmp = open(path,'w')
log = deleteContent(filetmp)
LogStartStr = 'Exoplanet HTML Database Parse Ver 0\nScript by Joe Renaud\nLog file created on: ' + now + '\n\n' + '1-Begin...\n'
log.write(LogStartStr)
filetmp = None
path = None
#Open HTML in question
HtmlURL = 'http://tedxgeorgemasonu.com/thankyou'
HtmlData = urllib2.urlopen(HtmlURL)
path = excFilePath.replace("Parse.py", "") + 'html1.tmp'
log.write('2-HTML URL to open: ' + HtmlURL + '\n')
filetmp = open(path,'w')
html1 = deleteContent(filetmp)
for line in HtmlData:
    html1.write(line+'\n')
log.write('3-Wrote HTML to : ' + path + '\n')
path = None
filetmp = None

# create a subclass and override the handler methods
#class MyHTMLParser(HTMLParser):
#    def handle_starttag(self, tag, attrs):
#        print "Encountered a start tag:", tag
#    def handle_endtag(self, tag):
#        print "Encountered an end tag :", tag
#    def handle_data(self, data):
#        print "Encountered some data  :", data

# instantiate the parser and fed it some HTML
#parser = MyHTMLParser()
#parser.feed('<html><head><title>Test</title></head>'
#            '<body><h1>Parse me!</h1></body></html>')