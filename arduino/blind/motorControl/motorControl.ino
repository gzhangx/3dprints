
#include <custStepper.h>

CustStepper stepper(64, 5,6,7,8);
void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }

  // prints title with ending line break
  Serial.println("ASCII Table ~ Character Map");    
}

int counter = 0;
int SCALE = 10;
void loop() {
  stepper.step(200);
  stepper.step(-200);
}
