"""bank.py

name: bank
author: Joshua Bowe
Needed modules(part of standard library):
    os
    sys
    decimal
    pickle
    time
Needed modules(local):
    Record
    user
    jutils
    utils
This program is to be like a simple checking account program.
It uses the "decimal" program.
From the start, it is python2 and python3 compatible.
"""
import sys
import os
import decimal
import pickle
import time
from decimal import Decimal
from Record import Record
from user import User
from jutils import jprint,jrange,jinput
from utils import file_exists,get_date,printdict
__all__=['paper_copy','run','db_name','jprint','jrange','jinput']
def paper_copy(user_obj):
    """peper_copy
if"""
    if not isinstance(user_obj,User):
        raise TypeError("user_obj must be an instance of User")
    header= "| Number |    Date    |            Info             |"
    header+=" Payment  | Deposit  |"
    sep="-"*75
    jprint(sep)
    jprint(header)
    for i in jrange()(len(user_obj.database)):
        jprint(sep)
        jprint(user_obj.database[i].return_line())
    jprint(sep)


def run(file_n):
    """run.py
This function takes in a file.
It prints up startup messages, Name, license, etc...
It then makes a user object.
It stores the options in a dict, using the numbers as a key.
If you enter an invalid answer, it continues to
the next iteration of the loop.

However, if you do give it valid input, it will check what
your answer is in the dictionary.  It then compares that string to
different if-elif parts.  When it finds it, it executes that
branch and continues.

To learn more, try it out([Font size 3]or look at the source :-) )
"""
    ##############STARTUP INFO######################
    jprint("Joshua's bank program")
    jprint("Use this for your personal needs only")
    jprint("No liabilitys...")
    jprint("This code is for free under the GNU GLPv3")
    time.sleep(0.5)
    jprint("Starting up.")
    ###################LOAD USER####################
    j=User(file_n)
    jprint("Loaded.")
    ############SET OPTION TO EMPTY STRING#########
    option=""
    #The dictionary contains everthing in the format of
    #'whatyouenter':'whatAction_it Does'
    options={'1': 'New','2':'List all','3':  "List one",
             '4': 'Change one','5':'Paper copy','6':'Delete one',
             '9':'Exit'}
    to_enter=sorted(options)##What the user can enter
    while True:
        """This is the loop that is the bank program.  It
           executes it.  If your input equals 'Exit', then break."""
        jprint("\n")
##        jprint("Choices: \n\t1:  New\n\t2:  List all\n\t3:  List one")
##        jprint("\t4:  Change one\n\t5. Paper copy\n\t6. Exit")
        printdict(options,'\t')
        option=jinput("Operation: ")
        if option not in to_enter:
            jprint("Please enter a number from %s to %s"%(min(to_enter),
                                                          max(to_enter)))
            continue
        if options[option]=='Exit':#Put the quickest one first
            break
        elif options[option]=='New':
            r=j.make_rec()
            j.add(r)
            j.save()
            if r.depo==False:
                jprint("Added check #%-6d from %s"%(r.number,r.to))
            else:
                jprint("Added payment from %s"%r.to)
        elif options[option]=='List all':
            jprint(j)
        elif options[option]=='Paper copy':
            paper_copy(j)
        elif options[option]=='List one':
            if len(j.database)==0:
                jprint("database is empty")
                continue
            allowed=[str(j.database[i].number) for i in jrange()(0,len(j.database))]
            allowed_str=', '.join(allowed)
            jprint("Allowed = %s"%allowed_str)
            foo='asdga'
            while foo not in allowed:
                try:foo=jinput("Number of check:  ")
                except:
                    jprint("Sorry, try again")
                else:break
            jprint("\n\n")
            for i in jrange()(0,len(j.database)):
                if j.database[i].number==int(foo):
                    jprint(j.database[i])
        elif options[option]=='Change one':
            jprint("Sorry, but this isn't allowed yet")
        elif options[option]=='Delete one':
            if len(j.database)==0:
                jprint("database is empty, none to delete")
                continue
            allowed=[str(j.database[i].number)
                         for i in jrange()(0,len(j.database))]
            allowed_str=', '.join(allowed)
            jprint("Allowed = %s"%allowed_str)
            foo='asdga'
            while foo not in allowed:
                try:foo=jinput("Number of check:  ")
                except:
                    jprint("Sorry, try again")
                if foo in allowed:break
            jprint("\n\n")
            jprint("Check number %s\n"%foo)
            for i in jrange()(0,len(j.database)):
                if j.database[i].number==int(foo):
                    jprint(j.database[i])

            conf='aasdfdasf'
            while conf not in ['y','n']:
                try:conf=jinput("Are you sure?")[0].lower()
                except KeyboardInterrupt:
                    conf='aasdfdasf'
                    jprint("Exiting delete");break
                except IndexError:
                    conf='aasdfdasf'
                    jprint("Sorry, try again")
                except Exception:
                    jprint("Sorry, but something went wrong, please enter")
                    jprint("in a letter, 'y' or 'n'")
                if conf in ['y','n']:continue
                else:
                    jprint("Please enter in 'y' or 'n'.")
            if conf=='y':
                for i in jrange()(0,len(j.database)):
                    if j.database[i].number==int(foo):
                        del j.database[i]
                        break
                jprint("Deleted.")
            else:jprint("Canceled.")
        else:jprint("Error: \"%s\" is not allowed"%option)
    jprint("Saving file",end='')
    for i in jrange()(0,5):
        jprint(".",end='')
    jprint("")
    jprint("Goodbye.")
##def database(file_obj):
##    db=[]
##    for line in file_obj
db_name="bank.jdb"
##db=open(db_name)
##a=Record(1000,(10,9,2017),"Winter camp","Jon",100.00,True)##Testing
##b=Record(1001,(10,9,2017),"Computer","Intel Corp.","400.00",False)##Testing
##j=User(db_name)##Testing
##j.add(a)##Testing
##j.add(b)##Testing
if __name__=='__main__':
    run(db_name)
else:
    pass
