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
int pin_reset = 0;

// the setup function runs once when you press reset or power the board
void setup() {
  Serial.begin(9600);
  while (!Serial);
  Serial.println("Starting ...");
  analogWrite(pin_vRef, 4 * 51); // 255 max value / 5V = 51
  analogWrite(pin_nbLow, 0.5 * 51);
  analogWrite(pin_nbCentral, 1 * 51);
  analogWrite(pin_nbHigh, 2 * 51);
  digitalWrite(pin_reset, LOW);
  delay(1000); 
  digitalWrite(pin_reset, HIGH);
}

// the loop function runs over and over again forever
void loop() {
  val_nLow = analogRead(pin_nLow);
  val_High = analogRead(pin_High);
  val_Diff = analogRead(pin_Diff);
  Serial.print(val_nLow);
  Serial.print("   ");
  Serial.print(val_Diff);
  Serial.print("   ");
  Serial.println(val_High);
  if (val_High >= 512) {
    Serial.println("ON!");
    digitalWrite(pin_reset, LOW);
    delay(1000); 
    digitalWrite(pin_reset, HIGH);    
  }
  if (val_nLow < 512) {
    Serial.println("OFF!");
    digitalWrite(pin_reset, LOW);
    delay(1000); 
    digitalWrite(pin_reset, HIGH);    
  }
  delay(10);
}
