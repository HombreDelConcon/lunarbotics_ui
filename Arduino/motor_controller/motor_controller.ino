#include <WiFiS3.h>

//Wheel motors
const int motor_AN_1_2 = 3;
const int motor_IN_1 = 5;
const int motor_IN_2 = 6;

//Excavator 
const int excavator_AN_1 = 2;
const int excavator_IN_1 = 4;

//Actuators
const int bin_act_AN_1 = 7; 
const int bin_act_IN_1 = 8;
const int excavator_act_AN1 = 9;
const int excavator_act_AN2 = 10;
const int excavator_act_IN1 = 11;
const int excavator_act_IN2 = 12;

//Router Login
const char ssid[] = "No Hotspot For U";
const char pw[] = "Extr@cto700";

int status = WL_IDLE_STATUS;

void setup() {
  Serial.println("Starting program");
  //Setup pins
  pinMode(motor_AN_1_2, OUTPUT);
  pinMode(motor_IN_1, OUTPUT);
  pinMode(motor_IN_2, OUTPUT);
  pinMode(excavator_AN_1, OUTPUT);
  pinMode(excavator_IN_1, OUTPUT);
  pinMode(bin_act_AN_1, OUTPUT);
  pinMode(bin_act_IN_1, OUTPUT);
  pinMode(excavator_act_AN1, OUTPUT);
  pinMode(excavator_act_AN2, OUTPUT);
  pinMode(excavator_act_IN1, OUTPUT);
  pinMode(excavator_act_IN2, OUTPUT);

  Serial.begin(9600);
  Serial.print("Idle Code: ");
  Serial.println(WL_IDLE_STATUS);
  Serial.print("Connected Code: ");
  Serial.println(WL_CONNECTED);

  // String fv = WiFi.firmwareVersion();
  // if (fv < WIFI_FIRMWARE_LATEST_VERSION) {
  //   Serial.print("Please upgrade the firmware to");
  //   Serial.println(WIFI_FIRMWARE_LATEST_VERSION);
  //   Serial.println(fv);
  // }
  listNetworks();

  // attempt to connect to WiFi network:
  while (status != WL_CONNECTED) {
    Serial.print(status);
    // Connect to WPA/WPA2 network. Change this line if using open or WEP network:
    status = WiFi.begin(ssid, pw);

    // wait 10 seconds for connection:
    delay(200);
  } 

  Serial.println();
  Serial.println("Connected");
}

void loop() {
  // put your main code here, to run repeatedly:

}

void listNetworks() {
  // scan for nearby networks:
  Serial.println("** Scan Networks **");
  int numSsid = WiFi.scanNetworks();
  if (numSsid == -1) {
    Serial.println("Couldn't get a wifi connection");
    while (true);
  }

  // print the list of networks seen:
  Serial.print("number of available networks:");
  Serial.println(numSsid);

  // print the network number and name for each network found:
  for (int thisNet = 0; thisNet < numSsid; thisNet++) {
    Serial.print(thisNet);
    Serial.print(") ");
    Serial.print(WiFi.SSID(thisNet));
    Serial.print("\tSignal: ");
    Serial.print(WiFi.RSSI(thisNet));
    Serial.print(" dBm");
    Serial.print("\tEncryption: ");
  }
}

