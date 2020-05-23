
#include <VarSpeedServo.h>

VarSpeedServo myServo;
int startingPos = 90;
int howFast = 35;
int endingPos = 20;

void setup() {
  myServo.write(startingPos);
  
  myServo.attach(8);
//  myServo.write(startingPos, howFast, true);
  myServo.write(endingPos, howFast, true);
}

void loop() {
  // put your main code here, to run repeatedly:
}
