import sys
import RPi.GPIO as GPIO
import requests
import json
from time import sleep

#For test, the following pins will be mapped to the follwing keys
#	 4: lmotors - Left motors
#	 5: rmotors - Right motors
#	12: le_motors - Linear excavator speed
#	13: bin_motors - Left & right motors speed
#	25: back_act - Back linear actuator
#	27: front_act - Front linear actuator


url = str(input("Input the URL of the host of the server"))
if url == "":
	url = "http://127.0.0.1:5000/test"

#Define duty cycle. Must be between 1 and 99 inclusive.
dc = int(input("Duty cycle:\n"))
if dc < 1 or dc > 99:
	raise BaseException("Number not valid dutycycle")

conversion_constant = 5 / 3.2575

class JSONError(Exception):
	pass

class RPI_output:

	#initialize all pins
	def __init__(self):
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(12, GPIO.OUT)
		GPIO.setup(13, GPIO.OUT)
		GPIO.setup(18, GPIO.OUT)
		GPIO.setup(4, GPIO.OUT)
		GPIO.setup(5, GPIO.OUT)
		GPIO.setup(27, GPIO.OUT)
		GPIO.setup(25, GPIO.OUT)
		self.pin1 = GPIO.PWM(12,100)
		self.pin2 = GPIO.PWM(13,100)
		self.pin3 = GPIO.PWM(18, 100)

	def main_loop(self):
		print("starting pwm")
		self.pin1.start(0 * conversion_constant)
		self.pin2.start(50 * conversion_constant)
		self.pin3.start(0 * conversion_constant)

		try:
			while True:
				#UI control data in JSON format
				json = self.send_request()

				#Test that all keys exist in the response and that they are within the expected range
				#	I'm stupid and will end up sending some bogus at some point so this will protect
				#	the robot... from me.
				for key in ["lmotors", "rmotors", "le_motors", "bin_motors", "le_speed", "lr_speed", "back_act", "front_act"]:
					try:
						json[key]
					except KeyError:
						print("Key %s does not exist" % (key))
						quit()
					else:
						if key not in ["le_speed", "lr_speed"]:
							if not (-1 <= json[key] <= 1):
								raise JSONError("Value for json is not valid\nKey: %s\nValue: %d" % (key, json[key]))

				while int(sys.argv[1]) == 1:
					GPIO.output(4,1)
				while int(sys.argv[1]) == 2:
					GPIO.output(5,1)
				while int(sys.argv[1]) == 3:
					GPIO.output(27,1)
				while int(sys.argv[1]) == 4:
					GPIO.output(25,1)
				while int(sys.argv[1]) in [5, 6]:
					print("starting pwm")
					self.pin1.start(50)
					self.pin2.start(50)
					sleep(3)
					self.pin1.ChangeDutyCycle(dc)
					self.pin2.ChangeDutyCycle(dc)
					sleep(3)

		except KeyboardInterrupt as e:
			self.pin1.stop()
			self.pin2.stop()
			self.pin3.stop()
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
	def test(self):
		print("starting pwm")
		self.pin1.start(0 * conversion_constant)
		self.pin2.start(50 * conversion_constant)
		self.pin3.start(0 * conversion_constant)
		try:
			while True:
				sleep(5)
				print("changing signal")
				self.pin3.ChangeDutyCycle(50 * conversion_constant)
				self.pin1.ChangeDutyCycle(65 * conversion_constant)				
				sleep(5)
				self.pin1.ChangeDutyCycle(0 * conversion_constant)
		except KeyboardInterrupt:
			self.pin1.stop()
			self.pin2.stop()
			self.pin3.stop()
			GPIO.cleanup()
			print('ports cleaned')
			print('closing program')

if __name__ == "__main__":
	pi = RPI_output()
	pi.test()
