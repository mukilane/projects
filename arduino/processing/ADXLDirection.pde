import processing.serial.*;

float x = 0;
float y = 0;
float z = 0;
String direction = "ADXL";

Serial myPort;

void setup() {
  size(200,200);
  myPort = new Serial(this, Serial.list()[32], 9600);
  myPort.bufferUntil('\n'); 
}

void draw() {
  background(50);
  textSize(32);
  textAlign(CENTER);
  text(direction, 100, 100);
}

void serialEvent(Serial myPort) {
    direction = myPort.readStringUntil('\n');
}