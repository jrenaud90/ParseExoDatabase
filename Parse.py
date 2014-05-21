#Imports
from HTMLParser import HTMLParser
from itertools import count
from datetime import date
import os,inspect,urllib2,types,datetime

def date_to_julian_day(my_date):
    """Returns the Julian day number of a date."""
    a = (14 - my_date.month)//12
    y = my_date.year + 4800 - a
    m = my_date.month + 12*a - 3
    return my_date.day + ((153*m + 2)//5) + 365*y + y//4 - y//100 + y//400 - 32045

#Functions
def deleteContent(pfile): #Delete File Contents
    pfile.seek(0)
    pfile.truncate()
    return pfile
def CurrentUTC():
    #Needs imported datetime
    x = datetime.datetime.utcnow()
    return x
def UTC2str(UTC):
    y=float(UTC.year)
    m=float(UTC.month)
    d=float(UTC.day)
    hr=UTC.hour
    mn=UTC.minute
    sec=UTC.second
    Full = str(y) + ' ' + str(m) + ' ' + str(d) + ' :: ' + str(hr) + ':' + str(mn) + ':' + str(sec)
    return Full
def utc2jd(utc):
    """
    Convert UTC to Julian date.

    Conversion translated from TPM modules utcnow.c and gcal2j.c, which
    notes that the algorithm to convert from a gregorian proleptic calendar
    date onto a julian day number is taken from
    The Explanatory Supplement to the Astronomical Almanac (1992),
    section 12.92, equation 12.92-1, page 604.

    @param utc: UTC (Universal Civil Time)
    @type utc: U{datetime<http://docs.python.org/lib/datetime.html>} object
    @return: Julian date (to the nearest second)
    @rtype: float



    """

##  But, beware of different rounding behavior between C and Python!
##    - integer arithmetic truncates -1.07 to -2 in Python; to -1 in C
##    - to reproduce C-like behavior in Python, do the math with float
##  arithmetic, then explicitly cast to int.


    y=float(utc.year)
    m=float(utc.month)
    d=float(utc.day)
    hr=utc.hour
    min=utc.minute
    sec=utc.second

    #Address differences between python and C time conventions
    #       C:                Python datetime
    # 0 <= mon  <= 11        1 <= month <= 12
    #

    #C code to get the julian date of the start of the day */
    #takes as input 1900+ptm->tm_year, ptm->tm_mon+1, ptm->tm_mday
    # So we can use just (year, month, mday)

    mterm=int((m-14)/12)
    aterm=int((1461*(y+4800+mterm))/4)

    bterm=int((367*(m-2-12*mterm))/12)

    cterm=int((3*int((y+4900+mterm)/100))/4)

    j=aterm+bterm-cterm+d
    j -= 32075
    #offset to start of day
    j -= 0.5


#    print "h/m/s: %f/%f/%f"%(hr,min,sec)

    #Apply the time
    jd = j + (hr + (min + (sec/60.0))/60.0)/24.0

    return jd

class DownloadHTMLtext:
    def __init__(self,html,log):
        self.url = html
        self.log = log
    def string(self):
        #Open HTML in question
        HtmlData = urllib2.urlopen(self.url)
##
        path = excFilePath.replace("Parse.py", "") + 'html1.tmp'
        self.log.write('2-HTML URL to open: ' + HtmlURL + '\n')
        with open(path,'w') as filetmp:
            with deleteContent(filetmp) as html1:
                for line in HtmlData:
                    html1.write(line)
                    self.log.write('3-Wrote HTML to : ' + path + '\n')
                pass
            pass
        with open(path,'r') as html1:
            self.log.write('4-Reading ' + path + 'as var: html1')
            kstr = ''
            for line in html1:
                kstr = kstr + line #Make large string of the html file
            pass
        return kstr
        
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
        log.write('\t-HTML Tag info Written to htmldata.tmp\n')
#    def handle_starttag(self, tag, attrs):
#        print "Encountered a start tag:", tag
#    def handle_endtag(self, tag):
#        print "Encountered an end tag :", tag
#    def handle_data(self, data):
#        print "Encountered some data  :", data


#Global Vars
 #Observatory information
Long = 38.8526 #Fairfax, Degrees
Lat = -77.3044 #Fairfax, Degrees

 #UTC Datetime
now = UTC2str(CurrentUTC())
excFilePath = inspect.getfile(inspect.currentframe()) #Finds current file path including file name.
 
 #Find Julian Date
jdate =  utc2jd(CurrentUTC())

#Open and use log file
path = excFilePath.replace("Parse.py", "") + 'Output.log' #Gets rid of current file name and replaces it with log name, change parse.py to current file name.
filetmp = open(path,'w')
log = deleteContent(filetmp)
LogStartStr = 'Exoplanet HTML Database Parse Ver 0\nScript by Joe Renaud\nLog file created on (UTC): ' + now + '\n\n' + '1-Begin...\n'
log.write(LogStartStr)
filetmp = None
path = None

#Open HTML in question
HtmlURL = 'http://var2.astro.cz/ETD/predictions.php?JDmidnight=' + str(jdate) + '&delka=' + str(Long) + '&sirka=' + str(Lat)
kstr = DownloadHTMLtext(HtmlURL,log).string()
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
                    #Do an if command here to see if the link is of interest.
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