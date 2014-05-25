#Imports
from HTMLParser import HTMLParser
import os,inspect,urllib2,datetime,shutil

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
def linkfinder(path):
    with open(path,'r') as htmldata:
        log.write('6-Opened htmldata.tmp in readonly mode\n')

# Find links in the file
        log.write('7-Looking for links...\n')
        path = excFilePath.replace("Parse.py", "") + 'TMP/links.tmp'
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
def ExoplanetHolder(htmldatapath,date):
    with open(htmldatapath,'r') as htmldata:
        path = excFilePath.replace("Parse.py", "") + 'TMP/exoplanets.tmp' #Gets rid of current file name and replaces it with log name, change parse.py to current file name.
        path2 = excFilePath.replace("Parse.py", "") + 'Exoplanets.csv' #Gets rid of current file name and replaces it with log name, change parse.py to current file name.
        url = None;name = None;const = None;b_UT = None;b_pos=None;b_jtime=None
        m_UT = None;m_pos=None;m_jtime=None;D=None;V=None;DEP=None
        e_UT = None;e_pos=None;e_jtime=None;ttime=None;RA=None;DE=None
        testword = 'predict_detail'
        with open(path2,'a') as filetmp2:
            with filetmp2 as exocsv:
                with open(path,'a') as filetmp:
                    with filetmp as exo:
                        exo.write('Date (UTC): ' + date + '\n')
                        exo.write('- - - - - - - - - -\n')
                        #exocsv.write(date + '\n')
                        x = htmldata.readlines()
                        cnt = 1
                        u = 0;c = 0;d = 0;f = 0;e = 0;k = 0;l=0;m=0;n=0;p=0;o=0;r=0;t=0;v=0
                        s = 0; w=0;ww=0;uu=0
                        for i in x:
                            if ww == 1:
                                if i.find('::DATA:')==0:
                                    indx = i.index(':') + 12
                                    DE = i[indx:].rstrip('\n')
                                    ww = 0
                            if w == 1:
                                if i.find('::DATA:')==0:
                                    indx = i.index(':') + 12
                                    RA = i[indx:].rstrip('\n')
                                    w = 0
                                    ww = 1
                            if s == 1:
                                if i.find('::DATA:')==0:
                                    indx = i.index(':') + 8
                                    ttime = i[indx:].rstrip('\n')
                                    s = 0
                                    w = 1
                            if v == 1:
                                if i.find('::DATA:')==0:
                                    indx = i.index(':') + 8
                                    DEP = i[indx:].rstrip('\n')
                                    v = 0
                                    s = 1
                            if t == 1:
                                if i.find('::DATA:')==0:
                                    indx = i.index(':') + 8
                                    V = i[indx:].rstrip('\n')
                                    t = 0
                                    v = 1
                            if r == 1:
                                if i.find('::DATA:')==0:
                                    indx = i.index(':') + 8
                                    D = i[indx:].rstrip('\n')
                                    r = 0
                                    t = 1
                            if o == 1:
                                if i.find('::DATA:')==0:
                                    indx = i.index(':') + 8
                                    e_jtime = i[indx:].rstrip('\n')
                                    o = 0
                                    r = 1
                            if p == 1:
                                if i.find('::DATA:')==0:
                                    indx = i.index(':') + 8
                                    e_pos = i[indx:].rstrip('\n')
                                    p = 0
                                    o = 1
                            if n == 1:
                                if i.find('::DATA:')==0:
                                    indx = i.index(':') + 8
                                    e_UT = i[indx:].rstrip('\n')
                                    n = 0
                                    p = 1
                            if m == 1:
                                if i.find('::DATA:')==0:
                                    indx = i.index(':') + 8
                                    m_jtime = i[indx:].rstrip('\n')
                                    m = 0
                                    n = 1
                            if l == 1:
                                if i.find('::DATA:')==0:
                                    indx = i.index(':') + 8
                                    m_pos = i[indx:].rstrip('\n')
                                    l = 0
                                    m = 1
                            if k == 1:
                                if i.find('::DATA:')==0:
                                    indx = i.index(':') + 8
                                    m_UT = i[indx:].rstrip('\n')
                                    l = 1
                                    k = 0
                            if f == 1:
                                if i.find('::DATA:')==0:
                                    indx = i.index(':') + 8
                                    b_jtime = i[indx:].rstrip('\n')
                                    f = 0
                                    k = 1
                            if e == 1:
                                if i.find('::DATA:')==0:
                                    indx = i.index(':') +8
                                    b_pos = i[indx:].rstrip('\n')
                                    e = 0
                                    #Find beginning sky position, reset e
                                    f = 1
                            if d == 1:
                                if i.find('::DATA:')==0:
                                    indx = i.index(':') +8
                                    b_UT = i[indx:].rstrip('\n')
                                    d = 0
                                    #Find beginning UT time, reset d
                                    e = 1
                            if c == 1:
                                if i.find('::DATA:' )==0:
                                    indx = i.index(':') +8
                                    const = i[indx:].rstrip('\n')
                                    c=0
                                    #Find Constilation, reset c
                                    d=1
                            if u == 1:
                                indx = i.index(':') +8
                                name = i[indx:].rstrip('\n')
                                u = 0
                                #Record Name
                                c = 1
                            if uu == 1:
                                if testword in i:
                                    indx = i.index('f') +4
                                    url = i[indx:].rstrip('\n')
                                    u = 1
                                    uu = 0
                                else:
                                    uu = 0
                            if i.find('::TAG: a' )==0:
                                uu = 1
                                    #Record URL and mark next line as name line.
                            
                            if url:
                                exo.write('Exoplanet ' + str(cnt) + ': \n')
                                exo.write('\tURL: ' + url + '\n')
                                exocsv.write(url+',')
                                cnt +=1
                                url = None
                            if name:
                                exo.write('\tName: ' + name + '\n')
                                exocsv.write(name+',')
                                name = None
                            if const:
                                exo.write('\tConstellation: ' + const + '\n')
                                exocsv.write(const+',')
                                const = None
                                exo.write('\t-TRANSIT START-\n')
                            if b_UT:
                                exo.write('\t\tUTC: ' + b_UT + '\n')
                                exocsv.write(b_UT+',')
                                b_UT = None
                            if b_pos:
                                exo.write('\t\tPOS: ' + b_pos + '\n')
                                exocsv.write(b_pos+',')
                                b_pos = None
                            if b_jtime:
                                exo.write('\t\tJ-Time: 24' + b_jtime + '\n')
                                exocsv.write('24'+b_jtime+',')
                                b_jtime = None
                            if m_UT:
                                exo.write('\t-TRANSIT MID-\n')
                                exo.write('\t\tUTC: ' + m_UT + '\n')
                                exocsv.write(m_UT+',')
                                m_UT = None
                            if m_pos:
                                exo.write('\t\tPOS: ' + m_pos + '\n')
                                exocsv.write(m_pos+',')
                                m_pos = None
                            if m_jtime:
                                exo.write('\t\tJ-Time: 24' + m_jtime + '\n')
                                exocsv.write('24'+m_jtime+',')
                                m_jtime = None
                            if e_UT:
                                exo.write('\t-TRANSIT END-\n')
                                exo.write('\t\tUTC: ' + e_UT + '\n')
                                exocsv.write(e_UT+',')
                                e_UT = None
                            if e_pos:
                                exo.write('\t\tPOS: ' + e_pos + '\n')
                                exocsv.write(e_pos+',')
                                e_pos = None
                            if e_jtime:
                                exo.write('\t\tJ-Time: 24' + e_jtime + '\n')
                                exocsv.write('24'+e_jtime+',')
                                e_jtime = None
                            if D:
                                exo.write('\tD: ' + D + '\n')
                                exocsv.write(D+',')
                                D = None
                            if V:
                                exo.write('\tV: ' + V + '\n')
                                exocsv.write(V+',')
                                V = None
                            if DEP:
                                exo.write('\tDEP: ' + DEP + '\n')
                                exocsv.write(DEP+',')
                                DEP = None
                            if ttime:
                                exo.write('\ttran-time: ' + ttime + '\n')
                                exocsv.write(ttime+',')
                                ttime = None
                            if RA:
                                exo.write('\tRA: ' + RA + '\n')
                                exocsv.write(RA+',')
                                RA = None
                            if DE:
                                exo.write('\tDE: ' + DE + '\n')
                                exocsv.write(DE+'\n')
                                DE = None
                                exo.write('Exoplanet End\n\n')
                        pass
                    pass
                pass
            pass
        pass
    os.remove(htmldatapath)
        
def DownloadHTMLtext(html,log,instance):
        HtmlData = urllib2.urlopen(html)
        path = excFilePath.replace("Parse.py", "") + 'TMP/html'+str(instance)+'.tmp'
        log.write('HTML URL to open: ' + HtmlURL + '\n')
        with open(path,'w') as filetmp:
            with deleteContent(filetmp) as html1:
                for line in HtmlData:
                    html1.write(line)
                pass
            pass
        html1 = None
        with open(path,'r') as html1:
            log.write('Reading ' + path + 'as var: html1')
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
    def handle_starttag(self, tag, attrs):
        htmldata.write('Item: \n')
        htmldata.write('::TAG: ' + tag + '\n')
        for attr in attrs:
            if len(attr)<2:
                htmldata.write('\t' + attr + '\n')
            else:
                st1 = attr[0]
                st2 = attr[1]
                htmldata.write('\t' + st1 + ' = ' + st2 + '\n')


#Global Vars Function
def globvars():
    d1 = input('Do you want to use Default Observatory location (1=yes,0=no)? ')
    if d1 == 0:
        Long = input('Observatory Longitude (0 to 360, degrees): ')
        Lat = input('Observatory Latitude (90 to 0 to -90, degrees): ')
    else:
        #Observatory information
        Long = 38.8526 #Fairfax, Degrees
        Lat = -77.3044 #Fairfax, Degrees
    d2 = input('Do you want to use today\'s date as starting point (1=yes,0=no)? ')
    if d2 == 0:
        jdate = input('Starting Date (Julian, no time): ')
    else:
        #Find Julian Date
        jdate =  utc2jd(CurrentUTC())
    return Long, Lat, jdate
  
#Get Global Variables
gvar = globvars()
Long = gvar[0]
Lat = gvar[1]
jdate = gvar[2]
excFilePath = inspect.getfile(inspect.currentframe()) #Finds current file path including file name.

#Make Temp File Directory
testtmpdir = excFilePath.replace("Parse.py", "") + 'TMP/'
if not os.path.exists(testtmpdir):
    os.makedirs(testtmpdir)
#Delete old files
os.remove(excFilePath.replace("Parse.py", "") + 'Exoplanets.csv')
os.remove(excFilePath.replace("Parse.py", "") + 'Output.log')
#Open and use log file
path = excFilePath.replace("Parse.py", "") + 'Output.log' #Gets rid of current file name and replaces it with log name, change parse.py to current file name.
filetmp = open(path,'w')
log = deleteContent(filetmp)
LogStartStr = 'Exoplanet HTML Database Parse Ver 1.1\nScript by Joe Renaud\nLog file created on (jdate): ' + str(jdate) + '\n\n' + 'Begin...\n'
log.write(LogStartStr)
filetmp = None;path = None

#Open HTML in question
for ikn in range(30):
    jdatenew = jdate + ikn
    #Open HTML in question
    HtmlURL = 'http://var2.astro.cz/ETD/predictions.php?JDmidnight=' + str(jdatenew) + '&delka=' + str(Long) + '&sirka=' + str(Lat)
    kstr = None
    kstr = DownloadHTMLtext(HtmlURL,log,ikn)
    path = excFilePath.replace("Parse.py", "") + 'TMP/htmldata.tmp'
    with open(path,'w') as filetmp:
        with deleteContent(filetmp) as htmldata:
            # instantiate the parser and fed it some HTML
            parser = MyHTMLParser()
            parser.feed(kstr)
            pass
        pass
    log.write('Day: ' + str(ikn) + ' - Finished parsing the html document\n')
    ExoplanetHolder(path,str(jdate+ikn))
    log.write('Day: ' + str(ikn) + ' - Exoplanetholder ran\n')
    
    
log.close()
#Debuging, please comment out the following to see temp files

shutil.rmtree(excFilePath.replace("Parse.py", "") + 'TMP/')
