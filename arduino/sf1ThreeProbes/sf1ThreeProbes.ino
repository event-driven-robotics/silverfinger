/* Analog in pins A0-A1 are connected thus:
 *  A0: nLow_0
 *  A1: High_0
 *  A2: nLow_1
 *  A3: High_1
 *  A4: nLow_2
 *  A5: High_2
 *  
 *  PWM pins are dedicated to:
 *  
 *  3: vRef = assuming ground - 4V away from the target of 4V. 
 *  9: nbLow       Guess     0.5 V  Targets:    100p
 *  10: nbCentral             1 V                1n
 *  11: nbHigh                2 V                10n
 *  (might need to go up to compensate for arduino sampling conductance
 *  
 *  Digital pins:
 *  
 *  0: reset_0
 *  1: reset_1
 *  2: reset_2
 *  
 */

int pin_vRef = 5;
int pin_nbLow = 9;
int pin_nbCentral = 10;
int pin_nbHigh = 11;

int pin_nLow_0 = A0;
int pin_High_0 = A1;
int pin_nLow_1 = A2;
int pin_High_1 = A3;
int pin_nLow_2 = A4;
int pin_High_2 = A5;

int val_nLow_0 = 0;
int val_High_0 = 0;
int val_nLow_1 = 0;
int val_High_1 = 0;
int val_nLow_2 = 0;
int val_High_2 = 0;

int refractCountDown_0 = 0;
int refractCountDown_1 = 0;
int refractCountDown_2 = 0;

int pin_reset_0 = 0;
int pin_reset_1 = 0;
int pin_reset_2 = 0;

int periodMs = 10;
int refractMs = 1000;

char strOut[65];

// the setup function runs once when you press reset or power the board
void setup() {
  Serial.begin(9600);
  while (!Serial);
  //Serial.println("Starting ...");
  analogWrite(pin_vRef, 4 * 51); // 255 max value / 5V = 51
  analogWrite(pin_nbLow, 0.5 * 51);
  analogWrite(pin_nbCentral, 1 * 51);
  analogWrite(pin_nbHigh, 2 * 51);
  digitalWrite(pin_reset_0, LOW);
  digitalWrite(pin_reset_1, LOW);
  digitalWrite(pin_reset_2, LOW);
  delay(1000); 
  digitalWrite(pin_reset_0, HIGH);
  digitalWrite(pin_reset_1, HIGH);
  digitalWrite(pin_reset_2, HIGH);
}

// the loop function runs over and over again forever
void loop() {
  val_nLow_0 = analogRead(pin_nLow_0);
  val_High_0 = analogRead(pin_High_0);
  val_nLow_1 = analogRead(pin_nLow_1);
  val_High_1 = analogRead(pin_High_1);
  val_nLow_2 = analogRead(pin_nLow_2);
  val_High_2 = analogRead(pin_High_2);
  //sprintf(strOut, "1: %4d %4d %4d  2: %4d %4d %4d  3: %4d %4d %4d", val_nLow_0, val_High_0, refractCountDown_0, val_nLow_1, val_High_1, refractCountDown_1, val_nLow_2, val_High_2, refractCountDown_2);
  sprintf(strOut, "%4d %4d %4d %4d %4d %4d %4d %4d %4d", val_nLow_0, val_High_0, refractCountDown_0, val_nLow_1, val_High_1, refractCountDown_1, val_nLow_2, val_High_2, refractCountDown_2);
  Serial.println(strOut); 
  if (refractCountDown_0 <= 0) {
    digitalWrite(pin_reset_0, HIGH);
    if (val_High_0 >= 512) {
       refractCountDown_0 = refractMs;
       digitalWrite(pin_reset_0, LOW);
    } else if(val_nLow_0 < 512) {
       refractCountDown_0 = refractMs;
       digitalWrite(pin_reset_0, LOW);
    };
  } else {
    refractCountDown_0 -= periodMs;
  };
  if (refractCountDown_1 <= 0) {
    digitalWrite(pin_reset_1, HIGH);
    if (val_High_1 >= 512) {
       refractCountDown_1 = refractMs;
       digitalWrite(pin_reset_1, LOW);
    } else if(val_nLow_1 < 512) {
       refractCountDown_1 = refractMs;
       digitalWrite(pin_reset_1, LOW);
    };
  } else {
    refractCountDown_1 -= periodMs;
  };
  if (refractCountDown_2 <= 0) {
    digitalWrite(pin_reset_2, HIGH);
    if (val_High_2 >= 512) {
       refractCountDown_2 = refractMs;
       digitalWrite(pin_reset_2, LOW);
    } else if(val_nLow_2 < 512) {
        refractCountDown_2 = refractMs;
       digitalWrite(pin_reset_2, LOW);
    };
  } else {
    refractCountDown_2 -= periodMs;
  };
    
  delay(periodMs);
}
