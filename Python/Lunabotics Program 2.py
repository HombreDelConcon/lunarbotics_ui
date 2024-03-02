# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 19:47:06 2024

@author: Corin
"""
import sys
import RPi.GPIO as GPIO
import requests
import json

url = str(input("Input the URL of the host of the server"))
if url == "":
	url = "http://127.0.0.1:5000/test"

class RPI_output:
	def __init__(self):
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(12, GPIO.OUT)
		GPIO.setup(13, GPIO.OUT)
		self.pin1 = GPIO.PWM(12,60)
		self.pin2 = GPIO.PWM(13,60)

		for pin in [4, 5, 27, 25]:
			GPIO.setup(pin, GPIO.OUT)
	
	def main_loop(self):
		try:
			while True:
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
				while 6 >= int(sys.argv[1]) >= 5:
					#Hz = (float(sys.argv[1]) - 5)
					
					self.pin1.start(50)
					self.pin2.start(50)
					# This is PWM for the wheels
					# range (0-1000000) for duty cycle
		except KeyboardInterrupt as e:
			self.pin1.stop()
			self.pin2.stop()
			GPIO.cleanup()
			print('ports cleaned')
			print('closing program')
	
	def send_request(self):
		url = "http://127.0.0.1:5000/test"
		try:
			resp = requests.get(url)
			print("Status code: " + str(resp.status_code))
			json_data = json.loads(resp.content)
			print(json_data["Stuf"])
		except requests.exceptions.ConnectionError as e:
			print("Could not connect")
		except KeyError as f:
			print("You have provided an invalid key")			

if __name__ == "__main__":
	pi = RPI_output()
	pi.main_loop()
	# pi.send_request()
