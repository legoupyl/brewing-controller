# Modules importation 

import threading
import time
import PT100
##  Variable definition

hlt_temp = 0
mlt_temp = 0
bk_temp = 0

hlt_ctrl_run = False
bk_ctrl_run = False

hlt_temp_set_point = 65.0
bk_power = 100

def function get_hlt_temp():
    global hlt_temp
    gpio=5

def function get_mlt_temp():
    global mlt_temp
    gpio=6

def function get_bk_temp():
    global bk_temp
    gpio=7

def function hlt_ctrl ()
    global hlt_ctrl_run



