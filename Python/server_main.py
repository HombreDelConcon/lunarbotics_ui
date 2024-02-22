from flask import Flask, jsonify, request, Response, make_response

app = Flask(__name__)

#Define a class which will store robot state to post onto the server. The
#   RasPi will be able to post to the server and 
class RobotState:
   def __init__(self, **control):
      self._motor1 = False
      self._motor2 = False
      self._lin_act = False
      self._misc = False
      if control["motor1"] and type(control["motor1"]) == bool:
         self._motor1 = control["motor1"]
         print("Set motor 1")
      if control["motor2"] and type(control["motor2"]) == bool:
         self._motor2 = control["motor2"]
         print("Set motor 2")
      if control["lin_act"] and type(control["lin_act"]) == bool:
         self._lin_act = control["lin_act"]
         print("Set linear actuators")
      if control["misc"] and type(control["misc"]) == bool:
         self._misc = control["misc"]
         print("Set misc")

   def set_motor1(self, new_value:bool) -> None:
      if not type(new_value) == bool:
         raise TypeError("Passed in wrong type for set_motor1. Function only takes bool as parameter")
      self._motor1 = new_value
   
   def set_motor2(self, new_value:bool) -> None:
      if not type(new_value) == bool:
         raise TypeError("Passed in wrong type for set_motor2. Function only takes bool as parameter")
      self._motor2 = new_value
      
@app.route('/test', methods=["GET"])
def get_req():
   if (request.method == "GET"):
      data = {
         "stat": 200,
         "man": True,
         "Stuff": "st"
      }
      response = make_response(jsonify(data))
      response.headers["Access-Control-Allow-Origin"] = "*"
      return response

if __name__ == '__main__':
   app.run(debug=True)