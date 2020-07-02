
// #include <VarSpeedServo.h>
#include <Servo.h>

// VarSpeedServo myServo;
// int startingPos = 90;
// int howFast = 35;
// int endingPos = 20;

Servo myServo;

void setup() {
//   myServo.write(startingPos);
  
//   myServo.attach(8);
// //  myServo.write(startingPos, howFast, true);
//   myServo.write(endingPos, howFast, true);

  myServo.write(78);
  myServo.attach(2);
  myServo.write(47);
  delay(900);
  myServo.write(78);
}

void loop() {
  // put your main code here, to run repeatedly:
}
