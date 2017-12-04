import os
import sys
from jutils import *
import time
from Record import Record
try:import xlsxwriter as xlwriter
except:
    sys.stdout.write('Sorry, but you don\'t have xlsxwriter.\n')
    sys.stdout.write('Use pip install xlsxwriter\n')
##    sys.exit(1)
__all__=["file_exists",'maxnumber','get_date','printdict','get_ending_bal',
         'change_one']
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
    keys.sort(key=lambda x:int(x))
    for key in keys:
        jprint("%s%2s: %s"%(start,key,d[key]))
def get_ending_bal(database):
    for i in jrange()(len(database)):
        if not isinstance(database[i],Record):
            raise TypeError("object in database is not of type Record")
    total=0
    for i in jrange()(len(database)):
        total+=database[i].return_money()
    return total
def change_one(record):
    if not isinstance(record,Record):
        raise TypeError("record is not of type Record")
    ##By now, we know that record is of type Record
    jprint("Current number is %-6d"%record.number)
    jprint("Do you want to change it, enter a number if yes, ")
    number=jinput('anything else if no: ')
    try:number=int(number)
    except:
        jprint("Invalid number, using current number")
        number=record.number
    jprint('\n')
    jprint("Do you want to change the %s from %2d/%2d/%4d"%('date',*record.date))
    conf=input("(Y/n)")[0].lower()
    if conf=='y':
        date=get_date()
    else:date=record.date
    jprint("\n")
    jprint("[Start details]\n%s\n[End details]\n"%record.details)
    conf=jinput("Do you want to change it?(Y/n)")[0].lower()
    if conf=='y':
        details=""
        jprint("\nTo quit entering details, type ^C")
        while True:
            try:details+=sys.stdin.readline()
            except (KeyboardInterrupt,EOFError):
                jprint("\nDone")
                break
    else:
        details=record.details
    jprint("\n")
    jprint("Current person to is \"%s\""%record.to)
    if jinput("Change it(Y/n)? ")[0].lower()=='y':
        to=jinput("To:  ")
    else:to=record.to
    jprint("\n")
    jprint("Current amount of money is $%-8.2f"%record.amt)
    if jinput("Change it(Y/n)? ")[0].lower()=='y':
        try:money=Decimal(jinput("Money amount"))
        except:
            jprint("Setting money to default")
            amt=record.amt
    else:amt=record.amt;jprint("Setting money to default")
    if record.depo==False:  jprint("This is currently a payment")
    elif record.depo==True: jprint("This is currently a deposit")
    else:raise TypeError("record.depo must be type bool")
    if jinput("Change it(Y/n) ")[0].lower()=='y':
        choice="e"
        while choice not in 'yn':
            try:choice=jinput("Is this a deposit?(Y/n) ")[0].lower()
            except:pass
        if choice=='y':
            depo=True
        else:depo=False
    return Record(number,date,details,to,amt,depo)
def dump_to_excel(database,filename):
    """This function takes a User object and a filename string.
it creates a file of filename+'.xlsx' .
it then writes to it and closes.'
The format for each line is below:
NUMBER  DATE  INFO  AMOUNT"""
    jprint('working on {0}...'.format(filename))
    filen=filename+'.xlsx'
    workbook=xlwriter.Workbook(filen)
    worksheet=workbook.add_worksheet()
    row=1
    col=0
    maxlength=10
    for record in database.database:
        worksheet.write(row,col,record.number)
        worksheet.write(row,col+1,'%2d/%2d/%2s'%(record.date[0],
                                                 record.date[1],
                                                 record.date[2]))
        worksheet.write(row,col+2,record.details.replace('\n','  '))
        if maxlength<len(record.details):maxlength=len(record.details)
        worksheet.write(row,col+3,record.return_money())
        row+=1
    worksheet.write(0,0,'Number')
    worksheet.write(0,1,"Date")
    worksheet.write(0,2,'Info')
    worksheet.write(0,3,'Amount')
    worksheet.set_column(2, 2, maxlength+5)
    workbook.close()
    return
def get_graph_money(user):
    current_total=0
    end_result=[]
    for i in jrange()(len(user.database)):
        if not isinstance(user.database[i],Record):
            raise TypeError("RECORD IS TYPE %s"%type(user.database[i]))
        current_total+=user.database[i].return_money()
        end_result.append(current_total)
    if end_result==[]:return [0]
    return end_result
