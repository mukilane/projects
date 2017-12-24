
#include <math.h>

const int groundpin = 18;             
const int powerpin = 19;              
const int xpin = A3;                  
const int ypin = A2;                  
const int zpin = A1;                  
int x, y, z;

void setup() { 
  Serial.begin(9600);
  pinMode(groundpin, OUTPUT);
  pinMode(powerpin, OUTPUT);
  digitalWrite(groundpin, LOW);
  digitalWrite(powerpin, HIGH);
}

void loop() {
  // Reading X axis
  x = analogRead(xpin);
  y = analogRead(ypin);
  z = analogRead(zpin);
  // Mapping the raw range of Accelerometer to a fixed range of 0-180
  Serial.print(map(x, 266, 396, -2, 2));
  Serial.print(",");
  Serial.print(map(y, 266, 396, -2, 2));
  Serial.print(",");
  Serial.println(map(z, 266, 396, -2, 2));
  delay(300);
}

