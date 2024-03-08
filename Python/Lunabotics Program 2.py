# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 19:47:06 2024

@author: Corin
"""
import sys
import RPi.GPIO as GPIO
import requests
import json
from time import sleep

url = str(input("Input the URL of the host of the server"))
if url == "":
	url = "http://127.0.0.1:5000/test"

dc = int(input("Duty cycle:\n"))
if dc < 0 or dc > 100:
	raise BaseException("Number not valid dutycycle")

class RPI_output:
	def __init__(self):
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(12, GPIO.OUT)
		GPIO.setup(13, GPIO.OUT)
		self.pin1 = GPIO.PWM(12,100)
		self.pin2 = GPIO.PWM(13,100)

		for pin in [4, 5, 27, 25]:
			GPIO.setup(pin, GPIO.OUT)
	
	def main_loop(self):
		try:
			while True:
				json = self.send_request()
				while int(sys.argv[1]) == 1:
					GPIO.output(4,1)
					# This is to run the motor on the raised bit
				while int(sys.argv[1]) == 2:
					GPIO.output(5,1)
					# This is to lift the raised bit (front)
				while int(sys.argv[1]) == 3:
					GPIO.output(27,1)
					# This is to lift the raised bit (back)
				while int(sys.argv[1]) == 4:
					GPIO.output(25,1)
					# This is to lift the bucket
				while int(sys.argv[1]) in [5, 6]:
					print("starting pwm")
					#Hz = (float(sys.argv[1]) - 5)
					self.pin1.start(100)
					self.pin2.start(100)
					sleep(3)
					self.pin1.ChangeDutyCycle(50)
					self.pin2.ChangeDutyCycle(50)

					sleep(3)
					# This is PWM for the wheels
					# range (0-1000000) for duty cycle
		except KeyboardInterrupt as e:
			self.pin1.stop()
			self.pin2.stop()
			GPIO.cleanup()
			print('ports cleaned')
			print('closing program')
	
	def send_request(self):
		json_data = None
		try:
			resp = requests.get(url)
			print("Status code: " + str(resp.status_code))
			json_data = json.loads(resp.content)
			print(json_data)
		except requests.exceptions.ConnectionError as e:
			print("Could not connect")
		except KeyError as f:
			print("You have provided an invalid key")		
		else:
			return json_data

if __name__ == "__main__":
	pi = RPI_output()
	pi.main_loop()
