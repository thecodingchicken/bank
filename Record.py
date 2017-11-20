from decimal import Decimal
from jutils import *
__all__=["Record"]
class Record():
    def __init__(self,number,date,details,to,amt,depo=False):
        """__init__(number,date,details,to,amt,depo=False)
    This is the input for object Record.  number is the number of the check.
    date is a tuple of len(3).  details is a string that tells you what the
    transaction was for.  to is a string describing who it is for.
    depo=False   if depo==False, then you are making a payment.
    if it is true, then you are getting payed money.  """
        self.number=number
        if type(date) not in [tuple,list]:
            raise TypeError("date is not of type 'tuple' or 'list'")
        if len(date)!=3:
            raise TypeError("date must be of format (%2d,%2d,%4d)")
        for i in jrange()(len(date)):
            if type(date[i])!=int:
                raise TypeError("object in date isn't an int")
        self.date=date
        self.details=details
        self.amt=Decimal(amt)
        self.to=to
        self.depo=bool(depo)
    def return_line(self):
        if len(self.details)>27:
            bar="%s..."%self.details[:24]
        else:bar=self.details
        bar=bar.replace("\n","")
        foo= "| %-6d | %-2d/%-2d/%4d | %-27s |"%(self.number,
                                     *self.date,bar)
        if self.depo==False:
            foo+=" %-8.2f |          |"%(self.amt)
        else:
            foo= "| DEPOSIT| %-2d/%-2d/%4d | %-27s |"%(*self.date,bar)
            foo+="          | %-8.2f |"%(self.amt)
        return foo
    def return_money(self):
        """return money.  If self.depo=False, return neg(money), else return
pos(money)"""
        if self.depo==True:
            return abs(self.amt)
        else:
            return abs(self.amt)*-1
    def __eq__ (self,other,full=False):
        """return if other is equal to self.
If full=False, then it will only compare the number.
If full=True,  then it will compare every part"""
        if isinstance(other,Record):
            if full == False:
                if self.number==other.number:
                    return True
                return False
            else:
                if ((self.number==other.number) and
                    (self.date==other.date) and
                    (self.details==other.details) and
                    (self.amt==other.amt) and
                    (self.to==other.to)):
                    return True
                return False
        return False
    def __str__(self):
        if self.depo==False:
            foo="Check #%-6d on %2d/%2d/%4d to %s\nPay $%-8.2f\nDetails:\t%s"%(
            self.number,*self.date,self.to,self.amt,self.details)
            return foo
        else:
            foo="Payment #%-6d on %2d/%2d/%4d "
            foo+="from %s\n Given $%-8.2f\nDetails:\t%s"
            return foo%(self.number,*self.date,self.to,self.amt,self.details)
##    def __repr__(self):
##        return "#%6d %2d/%2d/%4d \"%s\" $%8.2f \"\"\"%s\"\"\""%(
##            self.number,*self.date,self.to,self.amt,self.details)
