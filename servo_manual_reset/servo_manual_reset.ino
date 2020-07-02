
#include <Servo.h>

Servo myServo;

int potPin = A0;
//int servoPin = D8;
int val = 0;

void setup() {
  myServo.write(78);
  myServo.attach(2);
  Serial.begin(9600);
}

void loop() {
  val = analogRead(potPin);
  Serial.println(val);
  if(val > 632) {
    myServo.write(107);
  }
  else if(val < 120) {
    myServo.write(47);
  }
  else {
    myServo.write(78);
  }
}
