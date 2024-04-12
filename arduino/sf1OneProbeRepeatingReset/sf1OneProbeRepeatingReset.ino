/* Analog in pins A0-A1 are connected thus:
 *  A0: nLow_0
 *  A1: High_0
 *  A2: Diff
 *  
 *  The PWM pins are dedicated to:
 *  
 *  3: vRef = assuming ground - 4V away from the target of 4V. 
 *  
 *  9: nbLow       Guess     0.5 V  Targets:    100p
 *  10: nbCentral             1 V                1n
 *  11: nbHigh                2 V                10n
 *  (might need to go up to compensate for arduino sampling conductance
 */

int pin_vRef = 5;
int pin_nbLow = 9;
int pin_nbCentral = 10;
int pin_nbHigh = 11;

int pin_nLow = A0;
int pin_High = A1;
int pin_Diff = A2;

int val_nLow = 0;
int val_High = 0;
int val_Diff = 0;

int pin_reset = 2;

int countDown = 0;
int periodMs = 200;

char strOut[65];

// the setup function runs once when you press reset or power the board
void setup() {
  Serial.begin(9600);
  while (!Serial);
  Serial.println("Starting ...");
  analogWrite(pin_vRef, 4 * 51); // 255 max value / 5V = 51
  analogWrite(pin_nbLow, 0.5 * 51);
  analogWrite(pin_nbCentral, 3 * 51);
  analogWrite(pin_nbHigh, 2 * 51);
  pinMode(2, OUTPUT);
  digitalWrite(pin_reset, LOW);
  delay(1000); 
  digitalWrite(pin_reset, HIGH);
}

// the loop function runs over and over again forever
void loop() {
  val_nLow = analogRead(pin_nLow);
  val_High = analogRead(pin_High);
  val_Diff = analogRead(pin_Diff);
  sprintf(strOut, "%4d %4d %4d %4d", val_nLow, val_Diff, val_High, countDown);
  Serial.println(strOut);
    
  if (countDown <= 0) {
    Serial.println("Reset...");
    digitalWrite(pin_reset, LOW);
    countDown = 10000;
    }
  if (countDown == 5000) {
      Serial.println("Running...");
      digitalWrite(pin_reset, HIGH);
    }
    countDown -= periodMs;
  
  delay(periodMs);
}
