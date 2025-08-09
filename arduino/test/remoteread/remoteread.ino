
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
  {12, 0, 0, 0, 0}
};

int TOTAL_HISTORY = 10;
PinInputStatus history[10];

int TOTAL_REMOTE_PINS=1;


// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(19200);  
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(12, INPUT);
  for (int i = 0; i < TOTAL_HISTORY; i++) {
    history[i].val = -1;
    history[i].lastReadTime = 0;
  }
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
    if (val <= 1100) {
        return 1000;
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
int historyAt = 0;
unsigned long maxloops = microsecondsToClockCycles(1000) / 16;
// the loop routine runs over and over again forever:

int LED = HIGH;
unsigned long ledCount = 0;
int curVals[] = {15};
int newVals[] = {15};
void loop() {
  // read the input on analog pin 0:
  ledCount++;
  if (ledCount > 10000) {
    ledCount = 0;
    if (LED == HIGH) LED = LOW; else LED = HIGH;
  }
  digitalWrite(LED_BUILTIN, LED);
  
  
  
  for (int i = 0; i < TOTAL_REMOTE_PINS; i++) {
   PinInputStatus *ps = remotePins + i;
   byte ret = checkPinPwm(ps);
   if (ret == 1)  {
      newVals[i] = roundToNearestHundred(ps->diff);
   }
  }
  
  
    for (int i = 0; i < TOTAL_REMOTE_PINS;i++) {      
      if (newVals[i] != curVals[i]) {
        Serial.println(String("at ")+i+ " " + curVals[i]+" new=" + newVals[i] + " " );
        curVals[i] = newVals[i];
      }
    }
    historyAt = 0;
  
  
  //int d13= pulseIn(12, HIGH);// wait for a second  
  //dsp+= d13;
  //Serial.println(dsp);
}
