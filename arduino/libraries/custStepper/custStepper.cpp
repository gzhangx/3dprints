/*
 *
 * https://docs.arduino.cc/learn/electronics/stepper-motors#circuit
  Stepper motor and ULN2003 driver board compatible with 2560 1280 DSP ARM PIC AVR STM32 Raspberry Pi
Rated voltage: 12V DC; Stepping angle 5.625°/64, DC resistance 200Ω±7%, 4 phase 5 wire
A, B, C, D fou phases of the stepper motor work. 
 */

#include "Arduino.h"
#include "custStepper.h"

/*
 *   constructor for four-pin version
 *   Sets which wires should control the motor.
 */
CustStepper::CustStepper(int numSteps, int pin_1, int pin_2,
                                      int pin_3, int pin_4)
{
  this->stepNumber = 0;    // which step the motor is on
  this->direction = 0;      // motor direction
  this->lastStepTime = 0; // timestamp in us of the last step taken
  this->numSteps = numSteps; // total number of steps for this motor, 64 for 28BYJ-48

  // Arduino pins for the motor control connection:
  this->pin1 = pin_1;
  this->pin2 = pin_2;
  this->pin3 = pin_3;
  this->pin4 = pin_4;

  // setup the pins on the microcontroller:
  pinMode(this->pin1, OUTPUT);
  pinMode(this->pin2, OUTPUT);
  pinMode(this->pin3, OUTPUT);
  pinMode(this->pin4, OUTPUT);  

  setSpeed(28);
}

/*
 * Sets the speed in revs per minute
 */
void CustStepper::setSpeed(long whatSpeed)
{
  this->stepDelay = 60L * 1000L * 1000L / this->numSteps / whatSpeed;
}

/*
 * Moves the motor steps_to_move steps.  If the number is negative,
 * the motor moves in the reverse direction.
 */
void CustStepper::step(int steps_to_move)
{
  int steps_left = abs(steps_to_move);  // how many steps to take

  // determine direction based on whether steps_to_mode is + or -:
  if (steps_to_move > 0) { this->direction = 1; }
  if (steps_to_move < 0) { this->direction = 0; }


  // decrement the number of steps, moving one step each time:
  while (steps_left > 0)
  {
    unsigned long now = micros();
    // move only if the appropriate delay has passed:
    if (now - this->lastStepTime >= this->stepDelay)
    {
      // get the timeStamp of when you stepped:
      this->lastStepTime = now;
      // increment or decrement the step number,
      // depending on direction:
      if (this->direction == 1)
      {
        this->stepNumber++;
        if (this->stepNumber == this->numSteps) {
          this->stepNumber = 0;
        }
      }
      else
      {
        if (this->stepNumber == 0) {
          this->stepNumber = this->numSteps;
        }
        this->stepNumber--;
      }
      // decrement the steps left:
      steps_left--;            
      stepMotor(this->stepNumber % 4);
    } else {
      yield();
    }
  }
}

/*
 * Moves the motor forward or backwards.
 */
void CustStepper::stepMotor(int thisStep)
{
    switch (thisStep) {
      case 0:  // 1010
        digitalWrite(pin1, HIGH);
        digitalWrite(pin2, LOW);
        digitalWrite(pin3, HIGH);
        digitalWrite(pin4, LOW);
      break;
      case 1:  // 0110
        digitalWrite(pin1, LOW);
        digitalWrite(pin2, HIGH);
        digitalWrite(pin3, HIGH);
        digitalWrite(pin4, LOW);
      break;
      case 2:  //0101
        digitalWrite(pin1, LOW);
        digitalWrite(pin2, HIGH);
        digitalWrite(pin3, LOW);
        digitalWrite(pin4, HIGH);
      break;
      case 3:  //1001
        digitalWrite(pin1, HIGH);
        digitalWrite(pin2, LOW);
        digitalWrite(pin3, LOW);
        digitalWrite(pin4, HIGH);
      break;
    }
}

