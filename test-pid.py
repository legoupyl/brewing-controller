from simple_pid import PID
import time
import threading

temp=64

class controller():
    def __init__(self):
        self.pid=PID(Kp=112.344665712, Ki=0.840663751375, Kd=12.5112685197)
        self.pid.output_limits = (0, 100)
        self.pid.sample_time=5
        self.pid.setpoint = 65
        self.power=0
        self.running=False
        self.pid.proportional_on_measurement = True
    def run (self):
        
        while True:
            self.running = True
            self.power = self.pid (temp)
            print ("temp =" + str (round (temp,2)) + " power=" + str(round (self.power,2) ))
            time.sleep (1)
    def start (self):
            ctrl_thread = threading.Thread(target=self.run)
            ctrl_thread.daemon=True
            ctrl_thread.start()

def get_temp():
    global temp
    delta = (HLT_CTRL.power * 0.01 - 0.3) / 60
    temp=temp + delta
    time.sleep (1)
delta = 0

HLT_CTRL= controller()
HLT_CTRL.start()

while True:
    get_temp()