#!/usr/bin/python

import time

from neopixel import *

import argparse
import signal
import sys

#imports added by DK
import RPi.GPIO as GPIO

# LED strip configuration:
LED_COUNT      = 29      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 125     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_RGB   # Strip type and colour ordering

#RGB_Trainer constants
# Button input pin definitions
button1 = 21
button2 = 20
button3 = 16
button4 = 12
button5 = 23
reset_button = 4

#program state button
state = 0 #state FALSE means nothing is running, state 1 means other python is running

#filenames for the configuration files, one for button patterns, one for button colors
pattern_filename = 'climbing_patterns.cfg'
color_filename = 'colors.cfg' 
working_dir = '/home/pi/RGB_LED_Climb_project/'

#Training board LED mappings
LED_OFFSET = 2
LED_MAP =[18,17,0],[19,16,1],[20,15,2],[21,14,3],[22,13,4],[23,12,5],[24,11,6],[25,10,7],[26,9,8]

#GPIO setup
GPIO.setmode(GPIO.BCM)

#set all buttons to pull-ups
GPIO.setup(button1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(reset_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#start RGB strip
# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
# Intialize the library (must be called once before other functions).
strip.begin()

# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
	"""Wipe color across display a pixel at a time."""
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, color)
		strip.show()
		time.sleep(wait_ms/1000.0)


def theaterChase(strip, color, wait_ms=50, iterations=10):
	"""Movie theater light style chaser animation."""
	for j in range(iterations):
		for q in range(3):
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, color)
			strip.show()
			time.sleep(wait_ms/1000.0)
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, 0)

def wheel(pos):
	"""Generate rainbow colors across 0-255 positions."""
	if pos < 85:
		return Color(pos * 3, 255 - pos * 3, 0)
	elif pos < 170:
		pos -= 85
		return Color(255 - pos * 3, 0, pos * 3)
	else:
		pos -= 170
		return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=20, iterations=1):
	"""Draw rainbow that fades across all pixels at once."""
	for j in range(256*iterations):
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, wheel((i+j) & 255))
		strip.show()
		time.sleep(wait_ms/1000.0)

def rainbowCycle(strip, wait_ms=20, iterations=5):
	"""Draw rainbow that uniformly distributes itself across all pixels."""
	for j in range(256*iterations):
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
		strip.show()
		time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
	"""Rainbow movie theater light style chaser animation."""
	for j in range(256):
		for q in range(3):
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, wheel((i+j) % 255))
			strip.show()
			time.sleep(wait_ms/1000.0)
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, 0)

#clear matrix
def clear():
        """Wipe color across display a pixel at a time."""
        for i in range(strip.numPixels()):
                strip.setPixelColor(i, Color(0,0,0))
                
	strip.show()

#### Button call back functions###

def reset():
	global state
	state = not state #reverse state

	if state == True:
		colorWipe(strip, Color(125,5,5), 5)
		
        else:
		clear()

def buttonCall(SW_input): 
        if state == True: #only show if syste is "on", fake on/off switch
                clear()		

	#open pattern file for specific button pressed
	pattern_filename = working_dir + "pattern"+ str(SW_input) +".cfg" 

	#print pattern_filename
	pattern = read_from_file(pattern_filename)

	#iterate through all items in pattern file setting each LED specified
	for x in range(0, len(pattern)):
		#print "x is " + str(x)

		pixel_v1 = pattern[x][0] #get pixel mapping first value
		pixel_v2 = pattern[x][1] #get pixel mapping second value
		pixel = LED_MAP[pixel_v1][pixel_v2]+LED_OFFSET #map pixels to installed leds
		R = pattern[x][2] #set Red value from file
		G = pattern[x][3] #set Green value from file
		B = pattern[x][4] #set Blue value from file

		#print "pixel is LED_MAP[" + str(pixel_v1) +"]"+"["+str(pixel_v2)+"]="+ str(pixel)
		#print "Red value is " + str(R)
		#print "Green value is " + str(G)
		#print "Blue value is " + str(B)

		strip.setPixelColor(pixel, Color(R,G,B))  #set pixel
        
	strip.show()
        time.sleep(0.5)

######### Read climbing patterns from file########
def read_from_file(filename):

	with open(filename) as f:
    		patterns_array = []
    		for line in f:
        		line = line.split() # split lines at blanks 
        		if line:            # skip blanks)
            			line = [int(i) for i in line]
            			patterns_array.append(line)
	return patterns_array


########### Main Program ####################
def main():

	#pattern = read_from_file(pattern_filename) # read config file patters into array
	#colors = read_from_file(color_filename)

	while True:
		
		if(GPIO.input(reset_button) == False):
			reset()  # call reset function, reset acts as a state switch
		elif(GPIO.input(button1) == False):
			buttonCall(0)
                elif(GPIO.input(button2) == False):
                        buttonCall(1)
                elif(GPIO.input(button3) == False):
                        buttonCall(2)
                elif(GPIO.input(button4) == False):
                        buttonCall(3)
                elif(GPIO.input(button5) == False):
                        buttonCall(4)

		time.sleep(0.2)
			
	GPIO.cleanup()



if __name__ == "__main__":
	main()


		
