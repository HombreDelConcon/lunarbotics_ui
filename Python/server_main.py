from flask import Flask, jsonify, request, Response, make_response
from flask_cors import CORS

app = Flask(__name__)
CORS(app=app)

origin = str(input("type out the origin's URL:\n"))
if origin == "":
   origin = "http://127.0.0.1:5500"
   print("Origin set to default of localhost on port 5500")
server_route = "/test"
server_host = "0.0.0.0"
server_port = 5000

#Define a class which will store robot state to post onto the server. The
#   RasPi will be able to post to the server and 
class RobotState:
   def __init__(self):
      self.lmotors = 0
      self.rmotors = 0
      self.le_motor = 0
      self.bin_motor = 0
      self.le_speed = 1
      self.lr_motor_speed = 1
      self.back_act = 0
      self.front_act = 0

   def setAttributes(self, attributes:dict):
      try:
         self.rmotors = attributes["rmotors"]
         self.lmotors = attributes["lmotors"]
         self.le_motor = attributes["lemotors"]
         self.bin_motor = attributes["binmotor"]
         self.le_speed = attributes["lespeed"]
         self.lr_motor_speed = attributes["lrspeed"]
         self.back_act = attributes["backact"]
         self.front_act = attributes["frontact"]
      except KeyError as e:
         print("you missed an attribute")
         print("error %s" % (e))
         quit()

state = RobotState()

@app.route(server_route, methods=["GET", "POST"])
def main_endpoint():
   if (request.method == "GET"):
      data = {
         "forward/back": state.lmotors,
         "right/left": 0,
      }
      response = make_response(jsonify(data))
      response.headers["Access-Control-Allow-Origin"] = "*"
      return response
   elif (request.method == "POST"):
      print(state.__dict__)
      response = make_response("Ok")
      response.headers["Access-Control-Allow-Origin"] = "http://127.0.0.1:5500"
      return response

if __name__ == '__main__':
   app.run(debug=True, host=server_host, port=server_port)