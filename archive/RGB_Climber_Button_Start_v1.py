import RPi.GPIO as GPIO  
import time

GPIO.setmode(GPIO.BCM)  

# GPIO 4 set up as input. It is pulled up to stop false signals  
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)  

#set state variable

state = 0 #state FALSE means nothing is running, state 1 means other python is running

while True:
	try:  
    		GPIO.wait_for_edge(4, GPIO.FALLING)  
    		print "\nFalling edge detected. Now your program can continue with"  
    		print "whatever was waiting for a button press." 
		
		state = not state
		
		if state == True:
			print "\nStart Script"
		else: 
			print"\nStop Script"

		time.sleep(0.5)
 
	except KeyboardInterrupt:  
    		GPIO.cleanup()       # clean up GPIO on CTRL+C exit  

GPIO.cleanup()           # clean up GPIO on normal exit 
