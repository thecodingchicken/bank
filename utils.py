import os
from jutils import *
import time
__all__=["file_exists",'maxnumber','get_date','printdict']
def file_exists(db_name):
    if not os.path.exists(db_name):
        jprint("Creating database %s"%db_name)
        a=open(db_name,'w')
        a.close()
        del a
    else:
        jprint("Database \"%s\" exists"%db_name)
def maxnumber(database):
    maxnum=database[0].number
    for i in jrange()(len(database)):
        if database[i].number>maxnum:
            maxnum=database[i].number
    return maxnum
def test():
    "test utils functions.  Any files will start with 'utils_test_'"
    jprint("Clearing all 'utils_test_*' files")
    try:os.unlink("utils_test_file.test")
    except:pass
    file_exists('utils_test_file.test')
    file_exists('utils_test_file.test')
def get_date():
    date=[time.gmtime(time.time())[1],time.gmtime(time.time())[2],
          time.gmtime(time.time())[0]]
    month,day,year="aa","bb","cccc"
    while type(month)!=int:
        month=jinput("Month as a 2 digit number(ex 10): ")
        if month=='':
            jprint("Setting date to :\n\t%d/%d/%d"%(date[0],date[1],date[2]))
            return tuple(date)
        try:month=month[:2]
        except:jprint("Please give a two digit number");continue
        try:month=int(month)
        except:jprint("Please only give an int");continue
        if month>12 or month<1:
            month="aa"
            jprint("Please give a month from 1 to 12")
    while type(day)!=int:
        day=jinput("Day as a 2 digit number(ex 10): ")
        try:day=day[:2]
        except:jprint("Please give a two digit number");continue
        try:day=int(day)
        except:jprint("Please only give an int");continue
        if day>31 or day<1:
            day="aa"
            jprint("Please give a day from 1 to 31")
    while type(year)!=int:
        year=jinput("Year as a 4 digit number(ex 10): ")
        if year=='':
            jprint("Setting date to :\n\t%d/%d%d"%(month,day,date[2]))
            return (month,day,date[2])
        try:year=year[:4]
        except:jprint("Please give a two digit number");continue
        try:year=int(year)
        except:jprint("Please only give an int");continue
        if year>2200 or year<2000:###This code will work until the year
            year="aa"#2200. 
            jprint("Please give a year from 2000 to 2200")
    return month,day,year
def printdict(d,start):
    keys=sorted(d)
    for key in keys:
        jprint("%s%2s: %s"%(start,key,d[key]))
