//borrowed from https://github.com/arduino-libraries/Stepper/blob/master/src/Stepper.h
#ifndef CustStepper_h
#define CustStepper_h

// library interface description
class CustStepper {
  public:        
    CustStepper(int steps, int pin1, int pin2,
                                 int pin3, int pin4);    
    // speed setter method:
    void setSpeed(long whatSpeed);

    // mover method:
    void step(int number_of_steps);

  private:
    void stepMotor(int this_step);

    int direction;            // Direction of rotation
    unsigned long stepDelay; // delay between steps, in us, based on speed
    int numSteps;      // total number of steps this motor can take    
    int stepNumber;          // which step the motor is on

    // motor pin numbers:
    int pin1;
    int pin2;
    int pin3;
    int pin4;    

    unsigned long lastStepTime; // timestamp in us of when the last step was taken
};

#endif