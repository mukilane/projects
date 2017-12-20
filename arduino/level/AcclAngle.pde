import processing.serial.*;

int x; // 0-180 value
int deg = 0; // -90 to 90 value

Serial myPort;

void setup() {
  size(400,200);
  myPort = new Serial(this, Serial.list()[32], 9600);
  myPort.bufferUntil('\n'); 
}

void draw() {
  background(50);
  // Angle value
  textAlign(CENTER);
  textSize(32);
  text(deg, x*2+20, 50);
  
  // Pointer
  strokeWeight(5);
  stroke(255, 0, 0, 255);
  line(x*2+20, 70, x*2+20, 100);
  
  // Scale Markings 
  stroke(240);
  textSize(18);
  line(20, 100, 380, 100); 
  line(20, 100, 20, 120); 
  line(380, 100, 380, 120); 
  text("-90°", 20, 150);
  text("90°", 380, 150);
  text("0°", 200, 150);
}

void serialEvent(Serial myPort) {
    String val = myPort.readStringUntil('\n');
    // null check
    if ( val != null) {
      int[] data = int(split(val, ","));
      if(data.length >= 1) {
        x = data[0];
        // Map the 0-180 to -90to90 range
        deg = int(map(x, 0, 180, -90, 90));
      }
    }
}