
#include <math.h>

const int groundpin = 18;             
const int powerpin = 19;              
const int xpin = A3;                  
const int ypin = A2;                  
const int zpin = A1;                  
int x;

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
  // Mapping the raw range of Accelerometer to a fixed range of 0-180
  Serial.println(map(x, 266, 396, 0, 180));
  delay(300);
}

