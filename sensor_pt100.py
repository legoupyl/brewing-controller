import sys
from pt100 import PT100
print ("This is HLT temp sensor script")
for arg in sys.argv:
    print (arg)
PT100.init(hlt-sensor)
