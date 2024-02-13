# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 19:47:06 2024

@author: Corin
"""
import sys
# from time import sleep
import RPi.GPIO as GPIO
# import keyboard
import pigpio as  pi

while True:
    while sys.argv[1] == 1:
        GPIO.output(4,1)
        # This is to run the motor on the raised bit
    while sys.argv[1] == 2:
        GPIO.output(5,1)
        # This is to lift the raised bit (front)
    while sys.argv[1] == 3:
        GPIO.output(27,1)
        # This is to lift the raised bit (back)
    while sys.argv[1] == 4:
        GPIO.output(25,1)
        # This is to lift the bucket
    while 6 >= sys.argv[1] >= 5:
        Hz = (float(sys.argv[1]) - 5)
        pi.set_PWM_dutycycle(12, (1000000 * Hz))
        pi.set_PWM_dutycycle(13, abs(1000000 - (1000000 * Hz)))
        GPIO.PWM(12,60)
        GPIO.PWM(13,60)
        # This is PWM for the wheels
        # range (0-1000000) for duty cycle
    