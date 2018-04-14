#!/usr/bin/python
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# init list with pin numbers

pinList = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

# loop through pins and set mode and state to 'low'

for i in pinList: 
		GPIO.setup(i, GPIO.OUT) 
		GPIO.output(i, GPIO.HIGH)

# time to sleep between operations in the main loop

SleepTimeL = 2

# main loop

try:

	while true:
		GPIO.output(2, GPIO.LOW)
		print "OFF"
		time.sleep(SleepTimeL); 
		GPIO.output(2, GPIO.HIGH)
		print "ON"
		time.sleep(SleepTimeL); 
		

	GPIO.cleanup()
	print "Good bye!"

# End program cleanly with keyboard
except KeyboardInterrupt:
	print "  Quit"

	# Reset GPIO settings
	GPIO.cleanup()


# find more information on this script at
# http://youtu.be/oaf_zQcrg7g