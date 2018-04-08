"""record.py
bank/record.py

This file needs the following modules:
    decimal
This file needs the following local modules:
    jutils


"""
from decimal import Decimal
from jutils import jprint, jrange
__all__ = ["Record"]
class Record():
    """Record()
This is a row for a checking account.
"""
    def __init__(self, number, date, details, to, amt, depo=False):
        """__init__(number,date,details,to,amt,depo=False)
    This is the input for object Record.  number is the number of the check.
    date is a tuple of len(3).  details is a string that tells you what the
    transaction was for.  to is a string describing who it is for.
    depo=False   if depo==False, then you are making a payment.
    if it is true, then you are getting payed money.  """
        self.number = number
        if not isinstance(date, (tuple, list)):
            raise TypeError("date is not of type 'tuple' or 'list'")
        if len(date) != 3:
            raise TypeError("date must be of format (%2d, %2d, %4d)")
        for i in jrange()(len(date)):
            if not isinstance(date[i], int):
                raise TypeError("object in date isn't an int")
        self.date = date
        self.details = details
        self.amt = Decimal(amt)
        self.to_person = to
        self.depo = bool(depo)
    def is_same(self, other):
        """check to see if other==self
        Note-Not working"""
    def __lt__(self, other):
        "Return self<other.  Compare by date"
        if not isinstance(other, Record):
            raise TypeError("other is not of class Record")
        if self.date[2] < other.date[2]:
            return True
        elif self.date[1] < other.date[1]:
            return True
        elif self.date[0] < other.date[0]:
            return True
        return False
    def __gt__(self, other):
        "Return self>other.  Compare by date"
        if not isinstance(other, Record):
            raise TypeError("other is not of class Record")
        if   self.date[2] > other.date[2]:
            return True
        elif self.date[1] > other.date[1]:
            return True
        elif self.date[0] > other.date[0]:
            return True
        return False

    def return_line(self):
        'return the record as a line, like to be printed'
        if len(self.details) > 27:
            eggs = "%s..."%self.details[:24]
        else:
            eggs = self.details
        eggs = eggs.replace("\n", "")
        spam = "| %-6d | %-2d/%-2d/%4d | %-27s |"%(self.number,
                                                   *self.date, eggs)
        if self.depo is False:
            spam += " %-8.2f |          |"%(self.amt)
        else:
            spam = "| DEPOSIT| %-2d/%-2d/%4d | %-27s |"%(*self.date, eggs)
            spam += "          | %-8.2f |"%(self.amt)
        return spam
    def return_money(self):
        """return money.  If self.depo=False, return neg(money), else return
pos(money)"""
        if self.depo is True:
            return abs(self.amt)
        else:
            return abs(self.amt) * -1
    def __eq__(self, other):
        "Return self == other.  Compare by date"
        if not isinstance(other, Record):
            raise TypeError("other is not of class Record")
        if self.date == other.date:
            return True
        return False
#     def __eq__(self, other, full=False):
#         """return if other is equal to self.
# If full=False, then it will only compare the number.
# If full=True,  then it will compare every part"""
#         if isinstance(other, Record):
#             if full is False:
#                 if self.number == other.number:
#                     return True
#                 return False
#             else:
#                 if ((self.number == other.number) and
#                         (self.date == other.date) and
#                         (self.details == other.details) and
#                         (self.amt == other.amt) and
#                         (self.to_person == other.to_person)):
#                     return True
#                 return False
#         return False
    def __str__(self):
        if self.depo is False:
            return ("Check #%-6d on %2d/%2d/%4d to %s\nPay"+
                    " $%-8.2f\nDetails:\t%s"%(
                        self.number, *self.date, self.to_person,
                        self.amt, self.details))
        else:
            spam = "Payment #%-6d on %2d/%2d/%4d "
            spam += "from %s\n Given $%-8.2f\nDetails:\t%s"
            return spam%(self.number, *self.date, self.to_person,
                         self.amt, self.details)
##    def __repr__(self):
##        return "#%6d %2d/%2d/%4d \"%s\" $%8.2f \"\"\"%s\"\"\""%(
##            self.number,*self.date,self.to_person,self.amt,self.details)
    def to_csv(self, sep=''):
        "Return the record object in csv format"
        raise NotImplementedError("Not made yet")

if __name__ == '__main__':
    REC1 = Record(1001, (10, 11, 2017), 'test', 'test', 100)
    REC2 = Record(1001, (10, 11, 2017), 'tes1', 'tes1', 1001)
    jprint(REC1 > REC2, REC1 < REC2, REC1 == REC2, REC1 == REC2)
