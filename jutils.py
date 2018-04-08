"""jutils.py
This file contains functions used in the bank.py program.
They are for python2 and python3 compatibility."""
import sys
__all__ = ['jrange', 'jprint', 'jinput']
def jrange():
    """jrange()
    jrange takes no arguments.  It will work only if sys is imported.
    If python version, as by sys.version_info[0] == 2:return xrange
    if sys.version_info[0] == 3:return range
    This always returns the iterable version, without having to worry about
    making it ourselves."""
    if sys.version_info[0] == 3:
        return range
    elif sys.version_info[0] == 2:
        return xrange
    else:
        raise 
def jprint(*args, sep=' ', end='\n', file=sys.stdout):
    """jprint("*args, sep=' ', end='\\n', file=sys.stdout)
    Prints args to a stream, or to sys.stdout be default.
    Optional keyword arguments:
    file:   a file-like object (stream); defaults to the current sys.stdout.
    sep:    string inserted between values, defaults to a space.
    end:    string append after the last value, default a newline."""
    for i in jrange()(len(args)):
        if not isinstance(args[i], str):
            try:
                file.write(str(args[i]))
##                print("***%s***"%sep,end='')
                file.write(sep)
            except (TypeError):
                raise Exception("Arg could not be changed to str")
        else:
            file.write(args[i])
            file.write(sep)
    try:
        file.write(end)
    except:
        pass
    return None
def jinput(prompt=''):
    """Read a string from standard input.  The trailing newline is stripped.
       The prompt string, if given, is printed to standard output without a
       trailing newline before reading input.

       If the user hits EOF, return '\\n'
       This is used instead of input or raw_input, giving compatability.  """
    jprint(prompt, end='')
    text = sys.stdin.readline()#Read from standard input
    text = text.strip()#Strip stuff away
    return text
