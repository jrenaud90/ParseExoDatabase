# -*- coding: utf-8 -*-
"""
Created on Fri May 23 16:05:03 2014

@author: jrenaud
"""

import os,datetime,csv,inspect
import matplotlib.dates as dates
def deleteContent(pfile): #Delete File Contents
    pfile.seek(0)
    pfile.truncate()
    return pfile
def jd2gd(juldat):
    """ Convert a numerial Julian date into a Gregorian date using Pylab.
        Timezone returned will be UTC.

       EXAMPLES:
          print jd2gd(2454324.5)  --> 2007-08-12 00:00:00
          print jd2gd(2451545)    --> 2000-01-01 12:00:00

       SEE ALSO: gd2jd"""
    # 2008-08-26 14:03 IJC: Created    
    strtest = str(juldat)[0]+str(juldat)[1]
    if not strtest == '24':
        juldattsrt = '24'+str(juldat)
        juldat = float(juldattsrt)
        
    d = dates.julian2num(juldat)
    #gd = dates.num2date(d - 3442850)
    gd = dates.num2date(d)
    Date = str(gd.month)+'/'+str(gd.day)+'/'+str(gd.year)[2:]
    hour = gd.hour
    if hour >12:
        hrn = hour - 12
        hr = str(hrn)
        AMPM = 'PM'
        if hrn < 10:
            hr = '0'+hr
    else:
        hr = str(hour)
        AMPM = 'AM'
    if hour < 10:
        hr = '0'+hr
    if gd.minute < 10:
        mnH = gd.minute 
        mn = '0'+str(mnH)
    else:
        mn = str(gd.minute)
    if gd.second < 10:
        scH = gd.second 
        sc = '0'+str(scH)
    else:
        sc = str(gd.second)
    Time = hr+':'+mn + ':'+sc+' '+AMPM

    return Date,Time
def testrow(row,currenttime,mindeg,toolate,tooearly,TimePre,TimePost):
    testime=float(row[6])
    now2 = dates.date2num(currenttime)
    testtime = dates.julian2num(testime)
    tester1 = False
    if now2 >= testtime:
        res = False
    else:
        if row[4]<mindeg:
            res = False
        elif row[12]<mindeg:
            res = False
        else:
            ht = int(toolate[0:2])
            mt = int(toolate[3:5])
            time = jd2gd(float(row[14]))[1]
            if time[-2:] == 'AM':
                h = int(time[0:2])
                m = int(time[3:5])+TimePost #the additional 20 is for post transit observations
                if m > 60:
                    m = m - 60
                    h = h + 1
                if h==ht:
                    if m<=mt:
                        tester1 = True
                    else:
                        res = False
                elif h<ht:
                    tester1 = True
                else:
                    res = False
                if tester1 == True:
                    tester1 = False
                    ht = int(tooearly[0:2])
                    mt = int(tooearly[3:5])
                    time = jd2gd(float(row[6]))[1]
                    if time[-2:] == 'AM':
                        h = int(time[0:2])
                        m = int(time[3:5])-TimePre #the additional 20 is for post transit observations
                        if m < 0:
                            m = m + 60
                            h = h - 1
                        if h==ht:
                            if m>=mt:
                                tester1 = True
                            else:
                                res = False
                        elif h>ht:
                            tester1 = True
                        else:
                            res = False
                        if tester1 == True:
                            res = True
                    else:
                        res = False
            else:
                res = False
    return res
        
            
    
    
    
    
PathH = inspect.getfile(inspect.currentframe()) #Finds current file path including file name.
Path = PathH.replace("OutputCSVtoGoogleCSV.py", "")
now = datetime.datetime.now()
defaultQ = input('Do you want to use default parameters (1=yes,0=no): ')
if defaultQ == 0:
    mindeg = input('What is the telescope\'s minimum degree (in degrees, default is 20): ')
    toolate = raw_input('When is it too late in the night for a complete transit plus 20 mins after (formate in 01:30 UTC, default is \'07:30\' -> 2:30am EST): ')
    tooearly = raw_input('When is it too early in the night for a complete transit plus 20 mins before (formate in 01:30 UTC, default is \'02:00\' -> 8:00pm EST): ')
else:
    mindeg = 20 #degree
    toolate = '07:30' #Time UTC
    tooearly = '02:00' #Time UTC

TimePre = 20 #Pad Transit Start (mins)
TimePost = 20 #Pad Transit End(mins)
#Open File
with open(Path+'Exoplanets.csv','rb') as inputcsvH:
    with open(Path+'ExoplanetsUpload.csv','w') as outputcsvH:
        with deleteContent(outputcsvH) as outputcsv:
            outputcsv.write('Subject, Start Date, Start Time, End Date, End Time, All Day Event, Description, Location, Private\n')
            inputcsv = csv.reader(inputcsvH, delimiter=',', quotechar='|')
            for row in inputcsv:
                if testrow(row,now,mindeg,toolate,tooearly,TimePre,TimePost):
                    [btrandate,btrantime] = jd2gd(float(row[6])-TimePre*60*0.000011574)
                    [etrandate,etrantime] = jd2gd(float(row[14])+TimePost*60*0.000011574)
                    [mtrandate,mtrantime] = jd2gd(float(row[10]))
                    Desc1 = '\"'+row[1] + '; Prediction URL: \'' + row[0] + '\'; Begin-Transit: ' + row[4] + row[5]+',' + row[6] + '; '
                    Desc2 = 'End-Transit: ' + row[12] + row[13]+',' + row[14] + '; '
                    Desc3 = 'Location: RA=' + row[19] + ', DE=' + row[20] + '; '
                    Desc4 = 'D: ' + row[15] + '; V: ' + row[16] + '; Depth(Mag): ' + row[17] + '\"'
                    Desc = Desc1 + Desc2 + Desc3 + Desc4
                    line = row[1]+' (mag=' + row[17] + '),'+btrandate+','+btrantime+','+etrandate+','+etrantime+',False,'+Desc+',GMUObservatory,'+'False'
                    outputcsv.write(line + '\n')
            pass
        pass
    pass