from numpy import diff
import datetime , time
t = []
temp = []
diff_t2=[]
i=0
while i < 10:
    t.append (datetime.datetime.now())
    temp.append (i * 2)
    i=i+1
    time.sleep(1)


diff_temp=diff(temp)
diff_t=diff(t)

for delta_time in diff_t:
    diff_t2.append (delta_time.total_seconds())

print (diff_t2)

dydx = diff_temp/diff_t2
print (dydx)