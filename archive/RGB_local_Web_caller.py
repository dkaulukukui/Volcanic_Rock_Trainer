#!/usr/bin/env python

import sys
import time
import os
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

def main:

	#start RGB webserver
	os.system('rm recent_snapshots/*')  #remove the last 4 recent images

	#read pattern file

	while


