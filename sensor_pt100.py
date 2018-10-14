import sys
import pt100
print ("This is HLT temp sensor script")
for arg in sys.argv:
    print (arg)
pt100.init()
