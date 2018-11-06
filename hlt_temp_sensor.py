from brew_lib import sensor 
import time
hlt_temp = sensor("hlt_temp_sensor", "sensor", "temperature")

hlt_temp.start()
print (" ca continue")
while 1:
    time.sleep (10)
