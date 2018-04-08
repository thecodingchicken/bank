"""bank.py

name: bank
author: Joshua Bowe
Needed modules(part of standard library):
    os
    sys
    decimal
    pickle
    time
    re
    shutil
Needed modules(not part of std):
    matplotlib
    xlsxwriter
Needed modules(local):
    record
    user
    jutils
    utils
This program is to be like a simple checking account program.
It uses the "decimal" program.
From the start, it is python2 and python3 compatible.
"""
import time
START_T = time.time()
import sys
import os
import re
from user import User
try:
    from matplotlib import pyplot as plt
except:
    sys.stdout.write('Sorry, but you don\'t have matplotlib.\n')
    sys.stdout.write('	Use pip install matplotlib\n')
    sys.exit()

from jutils import jprint, jrange, jinput
from utils import printdict, get_ending_bal, change_one
from utils import dump_to_excel, get_graph_money
b=time.time()
jprint("Took %f seconds to load modules"%(b-START_T))
__all__=['paper_copy', 'run', 'DB_NAME', 'jprint', 'jrange', 'jinput']
def paper_copy(user_obj,debug=False):
    b = time.time()
    """paper_copy of a check book"""
    if not isinstance(user_obj, User):
        raise TypeError("user_obj must be an instance of User")
    user_obj.ending_bal = get_ending_bal(user_obj.database)
    header =  "| Number |    Date    |            Info             |"
    header += " Payment  | Deposit  |"
    sep = "-" * 75
    jprint(sep)
    jprint(header)
    for i in jrange()(len(user_obj.database)):
        jprint(sep)
        jprint(user_obj.database[i].return_line())
    jprint(sep)
    jprint("| %-6d Rows         |"%(len(user_obj.database)), end='')
    jprint(" "*23, end="")
    jprint("Ending balance: $%-8.2f | "%user_obj.ending_bal)
    jprint(sep)
    if user_obj.ending_bal<0:
        jprint(" " * 25,"*****BALANCE BELOW ZERO*****")
    a = time.time()
    if debug:
        jprint("[ Printed in %f seconds ]"%(a - b))

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
    j = User(file_n)
    jprint("Loaded.")
    ############SET OPTION TO EMPTY STRING#########
    option = ""
    #The dictionary contains everthing in the format of
    #'whatyouenter':'whatAction_it Does'
    options = {'1': 'New', '2':'List all', '3':  "List one",
             '4': 'Change one', '5':'Paper copy', '6':'Delete one',
             '7':'Get total', '8':'Graph money', '9':'dump to excel',
             '15':'Exit'}
    to_enter = sorted(options)##What the user can enter
    to_enter.sort(key=lambda x:int(x))
    while True:
        """This is the loop that is the bank program.  It
           executes it.  If your input equals 'Exit', then break."""
        j.ending_bal = get_ending_bal(j.database)
        jprint("\n")
        printdict(options,'\t')
        option = jinput("Operation: ")
        if option not in to_enter:
            jprint("Please enter a number from %s to %s"%(
                    min(to_enter, key=lambda x:int(x)),
                    max(to_enter, key=lambda x:int(x))))
            continue
        if options[option] == 'Exit':#Put the quickest one first
            break
        elif options[option] == 'New':
            r = j.make_rec()
            j.add(r)
            j.save()
            if r.depo is False:
                jprint("Added check #%-6d from %s"%(r.number, r.to_person))
            else:
                jprint("Added payment from %s"%r.to_person)
        elif options[option] == 'List all':
            jprint(j)
        elif options[option] == 'Paper copy':
            paper_copy(j)
        elif options[option] == 'Get total':
            jprint("$%.2f"%(j.ending_bal))
        elif options[option] == 'dump to excel':
            spam = os.listdir()
            eggs = []
            for i in spam:
                if i.endswith('.xlsx'):
                    eggs.append(i)
            del spam
            jprint("Current excel files: ",", ".join(eggs))
            jprint("Please give a name, exclude the ending filetype")
            try:name = jinput('Name: ')
            except:
                continue
            else:
                if re.findall(r'[^A-Za-z0-9 _\-\\]', name) != []:
                    jprint("Sorry, but that isn't a good file name")
                    continue
                dump_to_excel(j, name)
        elif options[option] == 'List one':
            if not j.database:
                jprint("database is empty")
                continue
            allowed=[str(j.database[i].number) for i in jrange()(0,len(j.database))]
            allowed_str=', '.join(allowed)
            jprint("Allowed = %s"%allowed_str)
            check_num='asdga'
            while check_num not in allowed:
                try:
                    check_num=jinput("Number of check:  ")
                except:
                    jprint("Sorry, try again")
                else:break
            jprint("\n\n")
            for i in jrange()(0, len(j.database)):
                if j.database[i].number == int(check_num):
                    jprint(j.database[i])
        elif options[option] == 'Change one':
            if not j.database:
                jprint("database is empty, none to change")
                continue
            allowed = [str(j.database[i].number)
                     for i in jrange()(0, len(j.database))]
            allowed_str = ', '.join(allowed)
            jprint("Allowed = %s"%allowed_str)
            check_num = 'asdga'
            while check_num not in allowed:
                try:
                    check_num = jinput("Number of check:  ")
                except:
                    jprint("Sorry, try again")
                else:
                    break
            jprint("\n\n")
            for i in jrange()(0, len(j.database)):
                if j.database[i].number == int(check_num):
                    jprint(j.database[i])
                    break
            try:
                conf = jinput("Is this correct?(Y/n) ")[0].lower()
            except:
                jprint("Something happened.  ")
                continue
            if conf == 'y':
                jprint("Enter nothing to keep it,",
                       "enter something to change it.")
                new_rec=change_one(j.database[i])
                jprint(new_rec)
                conf='e'
                while conf not in ['y','n']:
                    try:
                        conf = jinput("Is this correct(Y/n)? ")[0].lower()
                    except:
                        pass
                if conf=='n':
                    jprint("Not saving")
                else:
                    del j.database[i]
                    j.add(new_rec)
                    jprint("saved")
            else:jprint("quitting")
        elif options[option] == 'Graph money':
            jprint("This may take a while, depending on how long the checkbook")
            jprint("is.  Close the graph window to continue.")
            a = time.time()
            plt.figure(dpi=128,figsize=(10 ,6))
##            x_vals=list(jrange()(len(j.database)))
            x_v = list(jrange()(len(j.database)))
##            y_v=[j.database[i].return_money()
##                 for i in jrange()(len(j.database))]
            y_v = get_graph_money(j)
            plt.scatter(x_v,y_v,s=20)
            b = time.time()
            jprint("Figured in %f seconds"%(b - a))
            try:
                plt.show()
            except: 
                pass
        elif options[option] == 'Delete one':
            if not j.database:
                jprint("database is empty, none to delete")
                continue
            allowed = [str(j.database[i].number)
                         for i in jrange()(0, len(j.database))]
            allowed_str = ', '.join(allowed)
            jprint("Allowed = %s"%allowed_str)
            check_num = 'asdga'
            while check_num not in allowed:
                try:
                    check_num = jinput("Number of check:  ")
                except KeyboardInterrupt:
                    break
                except:
                    jprint("Sorry, try again")
                if check_num in allowed:
                    break
            else:
                jprint("\n\n")
                jprint("Check number %s\n"%check_num)
                for i in jrange()(0, len(j.database)):
                    if j.database[i].number == int(check_num):
                        jprint(j.database[i])

                conf = 'aasdfdasf'
                while conf not in ['y','n']:
                    try:
                        conf=jinput("Are you sure?")[0].lower()
                    except KeyboardInterrupt:
                        conf = 'aasdfdasf'
                        jprint("Exiting delete")
                        break
                    except IndexError:
                        conf = 'aasdfdasf'
                        jprint("Sorry, try again")
                    except Exception:
                        jprint("Sorry, but something went wrong, please enter")
                        jprint("in a letter, 'y' or 'n'")
                    if conf in ['y','n']:
                        continue
                    else:
                        jprint("Please enter in 'y' or 'n'.")
                if conf == 'y':
                    for i in jrange()(0, len(j.database)):
                        if j.database[i].number == int(check_num):
                            del j.database[i]
                            break
                    jprint("Deleted.")
                else:
                    jprint("Canceled.")
        else:
            jprint("Error: \"%s\" is not allowed"%option)
    jprint("Saving file",end='')
    for i in jrange()(0,5):
        jprint(".",end='')
    jprint("")
    jprint("Goodbye.")
DB_NAME ="bank.jdb"
if __name__=='__main__':
    jprint("Set up in %f seconds"%(time.time() - START_T))
    run(DB_NAME)
else:
    pass
j = User(DB_NAME)##Testing
print(repr(j))
