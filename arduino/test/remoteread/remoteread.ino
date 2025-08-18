
unsigned long time;

byte RMTSIGTOWAIT=1;
byte RMTSIGTOWAIT_NOT=RMTSIGTOWAIT?0:1;
struct PinInputStatus {
  int pin;
  int val; //hig or low
  byte state; //0 -> waiting for start, 1 started, 2 waiting for end
  unsigned long lastReadTime; //micros
  unsigned long  diff;
};

PinInputStatus remotePins []= {
  {2, 0, 0, 0, 0},   //hor, right 2000, left 1000, mind 1500
  {3, 0, 0, 0, 0}    //verticle, up 2000, down 1000, mid 1500
};


const int TOTAL_REMOTE_PINS=2;


#define LEFT_PWM_PIN 9
#define LEFT_DIR_PIN 10
#define RIGHT_PWM_PIN 7
#define RIGHT_DIR_PIN 8


volatile unsigned long risingEdgeTime2 = 0;
volatile unsigned long fallingEdgeTime2 = 0;
volatile unsigned long pulseWidth2 = 0;

volatile unsigned long risingEdgeTime3 = 0;
volatile unsigned long fallingEdgeTime3 = 0;
volatile unsigned long pulseWidth3 = 0;

const byte DEBUG_MODE=0;
void measurePulseWidth2() {
  if (digitalRead(2) == HIGH) {
    // Rising edge detected
    risingEdgeTime2 = micros();
  } else {
    // Falling edge detected
    fallingEdgeTime2 = micros();
    pulseWidth2 = fallingEdgeTime2 - risingEdgeTime2;
  }
}

void measurePulseWidth3() {
  if (digitalRead(3) == HIGH) {
    // Rising edge detected
    risingEdgeTime3 = micros();
  } else {
    // Falling edge detected
    fallingEdgeTime3 = micros();
    pulseWidth3 = fallingEdgeTime3 - risingEdgeTime3;
  }
}
void setup() {  
  Serial.begin(19200);  
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(3, INPUT);
  pinMode(2, INPUT);  

  attachInterrupt(digitalPinToInterrupt(3), measurePulseWidth3, CHANGE);
  attachInterrupt(digitalPinToInterrupt(2), measurePulseWidth2, CHANGE);

  pinMode(LEFT_PWM_PIN, OUTPUT);    //left wheel, mag
  pinMode(LEFT_DIR_PIN, OUTPUT);   //left wheel, pos, 0 forward, 1 back
  pinMode(RIGHT_PWM_PIN, OUTPUT);
  pinMode(RIGHT_DIR_PIN, OUTPUT);


  digitalWrite(LEFT_DIR_PIN, 0);
  digitalWrite(RIGHT_DIR_PIN, 0);
  digitalWrite(LEFT_PWM_PIN, 0);
  digitalWrite(RIGHT_PWM_PIN, 0);
}

//return 0 means waiting
byte checkPinPwm(PinInputStatus * ps) {
     int val = digitalRead(ps->pin);
     if (ps->state == 0){ //wait for start
        if (val == RMTSIGTOWAIT) return 0; //high, waiting for low
        if (val == RMTSIGTOWAIT_NOT) {     //low, flip state to 1 to wait
          if (ps->state == 0) {
            ps->state = 1;
          }
          return 0;
        }
     }else if (ps->state == 1) {
        if (val == RMTSIGTOWAIT_NOT) return 0;   //low, waiting for high
        if (val == RMTSIGTOWAIT) {               //high, mark start time, state to 2 to wait for low       
          ps->lastReadTime = micros();
          ps->state = 2;
        }
        return 0;
     }else if (ps->state == 2) {                 //waiting for low
        if (val == RMTSIGTOWAIT) return 0;
        //else we found it
        ps->diff = micros() - ps->lastReadTime;  //find how long it has been high
        ps->state = 0;
        return 1;
     }
     //this should not happen
     ps->state = 0;
     ps->diff = 0;
     ps->lastReadTime = 0;
     return 0;
}


int roundToNearestHundred(int val) {    
    // Validate input range
    if (val < 1100 || val > 2000) { //if no signal
        return 1500;
    }
    if (val >= 1900) {
        return 2000;
    }
        
    int diff = val - 1500;       
    int roundedDiff = ((diff + 50) / 100) * 100;      
    int result = 1500 + roundedDiff;
    
    if (result < 1000) {
        return 1000;
    }
    if (result > 2000) {
        return 2000;
    }
    
    return result;
}


// the loop routine runs over and over again forever:
const unsigned long PERIOD_MS=100; //10 or 1
int generate_pwm_signal(int duty_cycle, unsigned long current_time_ms) {
    // Ensure duty cycle is within valid range (0 to 100)
    if (duty_cycle < 0) duty_cycle = 0;
    if (duty_cycle > 100) duty_cycle = 100;
    
    // PWM period is 1ms (1000Hz frequency)
    const unsigned long period_ms = PERIOD_MS;
    
    // Calculate the time within the current PWM cycle (0 to period_ms)
    unsigned long cycle_time = current_time_ms % period_ms;
    
    // Calculate the high time based on duty cycle (in microseconds, since period is 1ms = 1000us)
    unsigned long high_time_us = (duty_cycle * period_ms) / 100;
    
    // Return 1 (high) if within high time, 0 (low) otherwise
    return (cycle_time < high_time_us) ? 1 : 0;
}

//from 1000->2000 to -100/100
int scalePwm(int remotePwm) {
  if (remotePwm < 1000) remotePwm = 1000;
  else if (remotePwm > 2000) remotePwm = 2000;
  remotePwm = (remotePwm - 1500) / 5;
  return remotePwm;
}
//between -100 to 100
int generate_pwm_full(int scaledPwm) {
  
  int remotePwmNoSign = scaledPwm;
  if (scaledPwm < 0) remotePwmNoSign = -scaledPwm;
  int on = generate_pwm_signal(remotePwmNoSign, millis());
  //if (scaledPwm < 0) return -on;
  return on;
}

int OLD_LEFT_PWM=0;
int OLD_LEFT_DIR=0;
int OLD_RIGHT_PWM=0;
int OLD_RIGHT_DIR=0;
void control_motors(int x, int y) {
    // x: -100 (left) to 100 (right)
    // y: -100 (reverse) to 100 (forward)
    
    // Compute motor speeds
    int left_speed = y + x;
    int right_speed = y - x;
    
    // Constrain to -100 to 100
    left_speed = constrain(left_speed, -100, 100);
    right_speed = constrain(right_speed, -100, 100);
    
    // Left motor
    int leftPWM = generate_pwm_full(left_speed);
    int leftDIR=(left_speed >= 0) ? LOW : HIGH;
    digitalWrite(LEFT_DIR_PIN, leftDIR);
    digitalWrite(LEFT_PWM_PIN, leftPWM);
    if (DEBUG_MODE) {
      if (OLD_LEFT_PWM != leftPWM) {
        OLD_LEFT_PWM = leftPWM;
        Serial.println(String("LEFT PWM ")+ leftPWM+" left speed "+left_speed+" right speed "+right_speed+" x="+x+" y="+y );;
      }
      if (OLD_LEFT_DIR != leftDIR){
        OLD_LEFT_DIR = leftDIR;
        Serial.println(String("LEFT DIR")+ leftDIR );
      }
    }
          
    // Right motor
    int rightPWM = generate_pwm_full(right_speed);
    int rightDIR = (right_speed >= 0) ? LOW : HIGH;
    digitalWrite(RIGHT_DIR_PIN, rightDIR);
    digitalWrite(RIGHT_PWM_PIN, rightPWM);
    if (DEBUG_MODE) {
      if (OLD_RIGHT_PWM != rightPWM) {
        OLD_RIGHT_PWM = rightPWM;
        Serial.println(String("RIGHT PWM ")+ rightPWM +" right_speed="+right_speed);
      }
      if (OLD_RIGHT_DIR != rightDIR){
        OLD_RIGHT_DIR = rightDIR;
        Serial.println(String("RIGHT DIR")+ rightDIR );
      }
    }
}

int LED = HIGH;
unsigned long ledCount = 0;
int curVals[] = {0, 0};
int newVals[] = {0, 0};
int pulesWidths[] = {1500,1500};
void loop() {
  noInterrupts(); // Temporarily disable interrupts to safely access pulseWidth
  pulesWidths[0] = pulseWidth2;
  pulesWidths[1] = pulseWidth3;
  interrupts(); // Re-enable interrupts
  // read the input on analog pin 0:
  ledCount++;
  if (ledCount > 10000) {
    ledCount = 0;
    if (LED == HIGH) LED = LOW; else LED = HIGH;
  }
  digitalWrite(LED_BUILTIN, LED);
  
  
  
  for (int i = 0; i < TOTAL_REMOTE_PINS; i++) {
   //PinInputStatus *ps = remotePins + i;
   //byte ret = checkPinPwm(ps);
   //if (ret == 1)  {
      //newVals[i] = scalePwm(roundToNearestHundred(ps->diff));      
      //newValsUnscalled[i] = scalePwm(roundToNearestHundred(ps->diff));
   //}
   newVals[i] = scalePwm(roundToNearestHundred(pulesWidths[i]));
  }

    control_motors(newVals[0], newVals[1]);

  if (DEBUG_MODE){
    for (int i = 0; i < TOTAL_REMOTE_PINS;i++) {      
      if (newVals[i] != curVals[i]) {
        Serial.println(String("at ")+i+ " " + curVals[i]+" new=" + newVals[i]+" paulse width="+pulesWidths[i] );
        curVals[i] = newVals[i];
      }
    }    
  } 
}
