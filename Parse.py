#Imports
from HTMLParser import HTMLParser
from itertools import count
import time,os,inspect,urllib2,mmap

#Functions
def deleteContent(pfile): #Delete File Contents
    pfile.seek(0)
    pfile.truncate()
    return pfile
#create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    def handle_data(self, data):
        if len(data) > 1:
            htmldata.write('::DATA: ' + data + '\n')
            log.write('\t-HTML Data info Written to htmldata.tmp\n')
    def handle_starttag(self, tag, attrs):
        htmldata.write('Item :\n')
        htmldata.write('::TAG: ' + tag + '\n')
        for attr in attrs:
            if len(attr)<2:
                htmldata.write('\t' + attr + '\n')
            else:
                st1 = attr[0]
                st2 = attr[1]
                htmldata.write('\t' + st1 + ' = ' + st2 + '\n')
        log.write('\t-HTML Tag info Written to htmlatt.tmp\n')
#    def handle_starttag(self, tag, attrs):
#        print "Encountered a start tag:", tag
#    def handle_endtag(self, tag):
#        print "Encountered an end tag :", tag
#    def handle_data(self, data):
#        print "Encountered some data  :", data
        
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
##
path = excFilePath.replace("Parse.py", "") + 'html1.tmp'
log.write('2-HTML URL to open: ' + HtmlURL + '\n')
with open(path,'w') as filetmp:
    with deleteContent(filetmp) as html1:
        for line in HtmlData:
            html1.write(line)
        log.write('3-Wrote HTML to : ' + path + '\n')
        pass
    pass
with open(path,'r') as html1:
    log.write('4-Reading ' + path + 'as var: html1')
    kstr = ''
    for line in html1:
        kstr = kstr + line #Make large string of the html file
    pass

#Make temp files for storing html information
path = excFilePath.replace("Parse.py", "") + 'htmldata.tmp'
with open(path,'w') as filetmp:
    with deleteContent(filetmp) as htmldata:
# instantiate the parser and fed it some HTML
        parser = MyHTMLParser()
        parser.feed(kstr)
        pass
    pass
log.write('5-Finished parsing the html document\n')
path = excFilePath.replace("Parse.py", "") + 'htmldata.tmp'
with open(path,'r') as htmldata:
    log.write('6-Opened htmldata.tmp in readonly mode\n')

# Find links in the file
    log.write('7-Looking for links...\n')
    path = excFilePath.replace("Parse.py", "") + 'links.tmp'
    with open(path,'w') as filetmp:
        with deleteContent(filetmp) as linkfile:
            x = htmldata.readlines()
            a = 0
            for i in x:
                if a == 1:
                    log.write('\t Link Found!\n')
                    indx = i.index('=') +2
                    link = i[indx:]
                    linkfile.write(link)
                    log.write('\t Link Recorded!\n')
                if i.find('::TAG: a') == 0:
                    a = 1
                else:
                    a = 0
        #if '::TAG: a' in line:
            #print htmldata[]
            pass
        pass
    pass



#Debuging
#os.remove(excFilePath.replace("Parse.py", "") + 'html1.tmp') #Uncomment during debug.

#Close open files.
log.close