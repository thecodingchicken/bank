import pickle
from utils import file_exists,maxnumber,get_date
from jutils import *
import time
import sys
import decimal
from Record import Record
class User():
    
    def __init__(self,file_n):
        """
class User(file_n)
this is a class for a checking accout user.
You give it a file that has a pickled database.  It will try to extract it.
If it gets an EOF error, the db is empty.  """
        self.file_n=file_n
        self.sorter=lambda x:x.number
        file_exists(self.file_n)
        try:#Assume that it exists.
            self.database=pickle.load(open(self.file_n,'rb'))##Always open files
            #like this in binary mode.
            self.database.sort(key=self.sorter)
            self.nextnum=maxnumber(self.database)+1#When making new checks, find
            #the max Record.number.  Add one.  That is your next check number
        except EOFError:##If you get EOFError, then you 
            self.database=[]#have an empty database
            self.nextnum=0
    def add(self,rec):
        """rec is a valid Record.  Use this function when possible, because
the database has no checking.  It will also filter out duplicates.  """
        if isinstance(rec,Record):##Make sure that rec is actually a record
            #before adding it to the database.
            self.database.append(rec)## db is actually just a list
        self.database=self.remove_dups()##get rid of duplicates
        self.database.sort(key=self.sorter)
    def remove_dups(self):
        """remove duplicates from the database.  It does so very easily.  It
iterates using an adaptive funtion that returns range in python3 and xrange in
python2.  If the record at self.database[i] is not in the new list, it adds it
to the list.  """
        new_db=[]
        for i in jrange()(len(self.database)):
            if self.database[i] not in new_db:
                new_db.append(self.database[i])
        return new_db
    def save(self):
        "save the database to self.file_n in 'rb' mode"
        self.database=self.remove_dups()#remove dups
        self.database.sort(key=self.sorter)
        pickle.dump(self.database,open(self.file_n,'wb'))#use pickle.dump
        #This makes things easier, since you can store binary data.  
    def __str__(self):
        "return a printable version of self with a short listing of every check"
        self.database=self.remove_dups()
        self.database.sort(key=self.sorter)
        string=""
        for i in jrange()(len(self.database)):
            foo="{:,}".format(self.database[i].amt)
            if foo.count(".")==0:
                foo+=".00"
                
            if self.database[i].depo==True:
                string+="#%-6d   $%-12s from %s\n"%(self.database[i].number,
                                           foo,
                                           self.database[i].to)
            else:
                string+="#%-6d   $%-12s to %s\n"%(self.database[i].number,
                                           foo,
                                           self.database[i].to)
##        jprint(string)
        return string
    def __repr__(self):
        self.database.sort(key=self.sorter)
        self.database=self.remove_dups()
        string="{0} at {1} checks".format(str(j.__class__),
                                          str(len(j.database)))
        return string
    def make_rec(self):
        number=jinput("Number(enter nothing for the next check): ")
        if number=='':
            number=self.nextnum
            self.nextnum+=1
        else:
            try:number=int(number)
            except:
                jprint("Invalid number, using #%-6d"%self.nextnum)
                number=self.nextnum
                self.nextnum+=1
        date=get_date()
        details=""
        jprint("\nTo quit entering details, type ^C")
        while True:
            try:details+=sys.stdin.readline()
            except (KeyboardInterrupt,EOFError):
##                jprint(details)
                jprint("\nDone")
                break
        to=jinput("To:  ")
        money="w"
        while True:
            money=jinput("Money: ")
            try:money=abs(decimal.Decimal(money))
            except decimal.InvalidOperation as e:
                jprint("Invalid amount.  \nPlease only enter the dollars and")
                jprint("cents.  Example 100.34")
            else:break
        depo=False
        while True:
            choices=['y','n']
            jprint("Is this a deposit?: ")
            depo=jinput("(Y/n):  ")[0].lower()
            if depo=='y':depo=True;break
            elif depo=='n':depo=False;break
            else:jprint("Please enter one of the below(%s)"%', '.join(choices))
        rec=Record(number,date,details,to,money,depo)
        return rec
