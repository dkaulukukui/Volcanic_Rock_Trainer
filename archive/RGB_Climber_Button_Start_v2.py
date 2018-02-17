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

while True:
	try:  
    		GPIO.wait_for_edge(GPIO_switch, GPIO.FALLING)  
    		print "\nFalling edge detected. Now your program can continue with"  
    		print "whatever was waiting for a button press." 
		
		state = not state
		
		if state == True:
			print "\nStart Script"
			rpistr = "sudo python ../rpi_ws281x/python/examples/climb_test1.py "
         		p=subprocess.Popen(rpistr,shell=True, preexec_fn=os.setsid)
		else: 
			print"\nStop Script"
			os.killpg(p.pid, signal.SIGTERM)

		while GPIO.input(GPIO_switch)==0:
			time.sleep(0.1)
 
	except KeyboardInterrupt:  
    		GPIO.cleanup()       # clean up GPIO on CTRL+C exit  

GPIO.cleanup()           # clean up GPIO on normal exit 
