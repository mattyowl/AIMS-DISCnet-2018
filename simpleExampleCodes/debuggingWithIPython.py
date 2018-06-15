"""

Simple example of using IPython for debugging

"""

import sys
import IPython

#------------------------------------------------------------------------------
def divide(a, b):
    """Divide two numbers
    
    Returns a float
    
    """
    return a/b

#------------------------------------------------------------------------------
# Main

a=5.0
b=2.0

c=divide(a, b)

b=0.0
try:
    c=divide(a, b)
except ZeroDivisionError:
    print("Ignoring a divide by zero error ...")

b="a"
c=divide(a, b)

#except:
#    print("This would have triggered a TypeError exception")
#    IPython.embed()
#    sys.exit()

