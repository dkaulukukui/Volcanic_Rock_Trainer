#!/usr/bin/python

import time

from neopixel import *

import argparse
import signal
import sys

#imports added by DK
import RPi.GPIO as GPIO

# LED strip configuration:
LED_COUNT      = 50      # Number of LED pixels.
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

#climbing pattern definitions
pattern1 = [2,5,12,16,21,29,30,38,42,46]
pattern2 = [0,6,10,18,22,25,31,36,40,49]
pattern3 = [1,7,11,15,20,27,32,35,44,48]
pattern4 = [4,8,14,17,24,26,33,39,43,47]
pattern5 = [3,9,13,15,20,28,32,35,44,45]

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

def button1Call(input):
	print "button 1 callback"

        if state == True: #only show if syste is "on", fake on/off switch
		clear()

		for i in pattern1:
			strip.setPixelColor(i, Color(255,0,0)) #Red
		strip.show()
		time.sleep(5)


def button2Call(input):
        print "button 2 callback"
        
        if state == True: #only show if syste is "on", fake on/off switch
		clear()

        	for i in pattern2:
                	strip.setPixelColor(i, Color(255,255,0)) #Red
        	strip.show()
        	time.sleep(5)


def button3Call(input):
        print "button 3 callback"

        if state == True: #only show if syste is "on", fake on/off switch
	        clear()

        	for i in pattern3:
                	strip.setPixelColor(i, Color(0,255,0)) #Red
        	strip.show()
        	time.sleep(5)


def button4Call(input):
        print "button 4 callback"

        if state == True: #only show if syste is "on", fake on/off switch
        	clear()

        	for i in pattern4:
                	strip.setPixelColor(i, Color(0,255,255)) #Red
        	strip.show()
        	time.sleep(5)


def button5Call(input):
        print "button 5 callback"
        
	if state == True: #only show if syste is "on", fake on/off switch
		clear()

        	for i in pattern5:
                	strip.setPixelColor(i, Color(0,0,255)) #Red
        	strip.show()
        	time.sleep(5)

def reset(input):
	global state
        print "state"
	print state
	state = not state #reverse state

	if state == True:
		print "Lights On"
		colorWipe(strip, Color(125,5,5), 5)
		
        else:
		print "Lights Off"
		clear()

########### Main Program ####################
def main():

	while True:

		GPIO.add_event_detect(button1, GPIO.FALLING, callback=button1Call, bouncetime=500)            
		GPIO.add_event_detect(button2, GPIO.FALLING, callback=button2Call, bouncetime=500)
		GPIO.add_event_detect(button3, GPIO.FALLING, callback=button3Call, bouncetime=500)
		GPIO.add_event_detect(button4, GPIO.FALLING, callback=button4Call, bouncetime=500)
 		GPIO.add_event_detect(button5, GPIO.FALLING, callback=button5Call, bouncetime=500)
		GPIO.add_event_detect(reset_button, GPIO.FALLING, callback=reset, bouncetime=500)		

		try:
	    		#raw_input()
			time.sleep(0.1)
		except KeyboardInterrupt:
			GPIO.cleanup()
			
	GPIO.cleanup()



if __name__ == "__main__":
	main()


		
