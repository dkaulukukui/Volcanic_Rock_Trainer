#!/usr/bin/python

import RPi.GPIO as GPIO  
import time
import subprocess, os
import signal

GPIO.setmode(GPIO.BCM)  
GPIO_switch = 4

# GPIO_switch set up as input. It is pulled up to stop false signals  
GPIO.setup(GPIO_switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)  

#set state variable


state = 0 #state FALSE means nothing is running, state 1 means other python is running

#command to call script if state is true
str_true = "/usr/bin/python /home/pi/RGB_LED_Climb_project/Main_RGB_Trainer_v1.py"

#command to clear matrix after killing script
str_clear = "/usr/bin/python /home/pi/RGB_LED_Climb_project/RGB_clear_v1.py"

while True:
	try:  
    		GPIO.wait_for_edge(GPIO_switch, GPIO.FALLING)  

		state = not state #reverse state
		
		if state == True:
			print "\nStart Script"
         		p=subprocess.Popen(str_true,shell=True, preexec_fn=os.setsid)
		else: 
			print"\nStop Script"
			os.killpg(p.pid, signal.SIGTERM)
			p=subprocess.Popen(str_clear,shell=True)

		while GPIO.input(GPIO_switch)==0:
			time.sleep(0.1)
	except KeyboardInterrupt:  
    		GPIO.cleanup()       # clean up GPIO on CTRL+C exit  

GPIO.cleanup()           # clean up GPIO on normal exit 
