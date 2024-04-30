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
	url = "http://192.168.0.100:5000/test"

#Define duty cycle. Must be between 1 and 99 inclusive.
dc = int(input("Duty cycle:\n"))
if dc < 1 or dc > 99:
	raise BaseException("Number not valid dutycycle")

conversion_constant = 5 / 3.2575

attempts = 0

class JSONError(Exception):
	pass

class RPI_output:
	#initialize all pins
	def __init__(self):
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(12, GPIO.OUT)
		GPIO.setup(13, GPIO.OUT)
		GPIO.setup(18, GPIO.OUT)
		GPIO.setup(19, GPIO.OUT)
		GPIO.setup(4, GPIO.OUT)
		GPIO.setup(5, GPIO.OUT)
		GPIO.setup(27, GPIO.OUT)
		GPIO.setup(17, GPIO.OUT)
		GPIO.setup(22, GPIO.OUT)
		GPIO.setup(23, GPIO.OUT)
		GPIO.setup(0, GPIO.OUT)
		GPIO.setup(1, GPIO.OUT)
		GPIO.setup(5, GPIO.OUT)
		GPIO.setup(6, GPIO.OUT)

		self.pin1 = GPIO.PWM(12, 100)
		self.pin2 = GPIO.PWM(13, 100)
		self.pin3 = GPIO.PWM(18, 100)
		self.pin4 = GPIO.PWM(19, 100)

	def main_loop(self) -> None:
		#Speed is constrained to the max number we can multiply by the conversion 
		#	constant and still be under 100. Since the highest speed level is 4 bars,
		#	we divide it by 4.
		speed_constant = 65 / 4
		lr_speed_scalar = 1

		#Threshold voltage
		pwm_thresh_high = 65
		pwm_thresh_low = 1

		print("starting pwm...")
		# self.pin1.start(0 * conversion_constant)
		# self.pin2.start(50 * conversion_constant)
		
		#Calibrate driver board with stop signal to AN pins
		self.pin3.start(0 * conversion_constant)
		self.pin4.start(0 * conversion_constant)
		self.pin1.start(0 * conversion_constant)
		self.pin2.start(0 * conversion_constant)
		GPIO.output(22, False)
		GPIO.output(23, False)
		GPIO.output(5, False)
		sleep(3)
		print("done calibrating")
		self.pin3.ChangeDutyCycle(50 * conversion_constant)
		self.pin4.ChangeDutyCycle(50 * conversion_constant)

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
				
				lr_speed_scalar = int(json["lr_speed"])

				if json["lmotors"] == 1 and json["rmotors"] == 1:
					self.pin3.ChangeDutyCycle((speed_constant * lr_speed_scalar) * conversion_constant)
					self.pin4.ChangeDutyCycle((speed_constant * lr_speed_scalar) * conversion_constant)
					self.pin1.ChangeDutyCycle(pwm_thresh_high * conversion_constant)
					self.pin2.ChangeDutyCycle(pwm_thresh_low * conversion_constant)
					print("forward")
					print((speed_constant * lr_speed_scalar) * conversion_constant)
				elif json["lmotors"] == -1 and json["rmotors"] == -1:
					self.pin3.ChangeDutyCycle((speed_constant * lr_speed_scalar) * conversion_constant)
					self.pin4.ChangeDutyCycle((speed_constant * lr_speed_scalar) * conversion_constant)
					self.pin1.ChangeDutyCycle(pwm_thresh_low * conversion_constant)
					self.pin2.ChangeDutyCycle(pwm_thresh_high * conversion_constant)
					print("back")
					print((speed_constant * lr_speed_scalar) * conversion_constant)
				elif json["lmotors"] == 0 and json["rmotors"] == 0:
					self.pin3.ChangeDutyCycle(0)
					self.pin4.ChangeDutyCycle(0)
					self.pin1.ChangeDutyCycle(0)
					self.pin2.ChangeDutyCycle(0)
					print("stop")
					print((speed_constant * lr_speed_scalar) * conversion_constant)
				elif json["lmotors"] == 1 and json["rmotors"] == -1:
					self.pin3.ChangeDutyCycle((speed_constant * lr_speed_scalar) * conversion_constant)
					self.pin4.ChangeDutyCycle((speed_constant * lr_speed_scalar) * conversion_constant)
					self.pin1.ChangeDutyCycle(pwm_thresh_high * conversion_constant)
					self.pin2.ChangeDutyCycle(pwm_thresh_high * conversion_constant)
					print("right")
					print((speed_constant * lr_speed_scalar) * conversion_constant)
				elif json["lmotors"] == -1 and json["rmotors"] == 1:
					self.pin4.ChangeDutyCycle((speed_constant * lr_speed_scalar) * conversion_constant)
					self.pin3.ChangeDutyCycle((speed_constant * lr_speed_scalar) * conversion_constant)
					self.pin1.ChangeDutyCycle(pwm_thresh_low * conversion_constant)
					self.pin2.ChangeDutyCycle(pwm_thresh_low * conversion_constant)
					print("left")
					print((speed_constant * lr_speed_scalar) * conversion_constant)
				else:
					raise JSONError("A value of lmotors or rmotors is outside the expected range")
				
				if json["back_act"] == 1:
					GPIO.output(22, True)
					GPIO.output(27, True)
					GPIO.output(17, False)
				elif json["back_act"] == -1:
					GPIO.output(22, True)
					GPIO.output(27, False)
					GPIO.output(17, True)
				elif json["back_act"] == 0:
					GPIO.output(22, False)
				
				if json["front_act"] == 1:
					GPIO.output(23, True)
					GPIO.output(17, False)
					GPIO.output(27, True)
				elif json["front_act"] == -1:
					GPIO.output(23, True)
					GPIO.output(17, True)
					GPIO.output(27, False)
				elif json["front_act"] == 0:
					GPIO.output(23, False)
				
				if json["bin_motors"] == 1:
					GPIO.output(6, True)
					GPIO.output(1, False)
					GPIO.output(0, True)
				elif json["bin_motors"] == -1:
					GPIO.output(6, True)
					GPIO.output(1, True)
					GPIO.output(0, False)
				elif json["bin_motors"] == 0:
					GPIO.output(6, False)
				
				if json["le_motors"] == 1:
					GPIO.output(5, True)
					GPIO.output(1, False)
					GPIO.output(0, True)
				elif json["le_motors"] == -1:
					GPIO.output(5, True)
					GPIO.output(1, True)
					GPIO.output(0, False)
				elif json["le_motors"] == 0:
					GPIO.output(5, False)

				sleep(0.25)

		except KeyboardInterrupt as e:
			self.pin1.stop()
			self.pin2.stop()
			self.pin3.stop()
			self.pin4.stop()
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
			dummy_json = {
				"lmotors":0, "rmotors":0, "le_motors":0, "bin_motors":0, "le_speed":0, "lr_speed":0, "back_act":0, "front_act":0
			}
			return dummy_json
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
	pi.main_loop()
