/* Each of analog pins A0-A11 is connected to one metal plate of the silverfinger.
 *  We come into the algorithm with all plates set to MODE = OUTPUT = 0
 *  One at a time the pins are read. Each read consists of 11 cycles, one for each of the other plates.
 *  Firstly, switch the main pin to INPUT and do an analog read from it (discard this read). This should set the mux to accept it.
 *  For each other plate:
 *  (b) set main plate to INPUT
 *  (c) switch second plate to OUT = HIGH
 *  (d) read main plate
 *  (e) set the main plate back to OUTPUT = LOW, and set the second plate bac to OUTPUT = LOW
 */

static const uint8_t analog_pins[] = {A0,A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,A11};

// the setup function runs once when you press reset or power the board
void setup() {
  analogReadResolution(12);
  // Setup pins for input
  for (int i = 0; i < 12; i++) {
    pinMode(analog_pins[i], OUTPUT);
    digitalWrite(analog_pins[i], 0);
  }
  Serial.begin(9600);
  while (!Serial);
  Serial.println("Starting ...");
}


// the loop function runs over and over again forever
void loop() {
  Serial.print("[");
  Serial.print(millis());
  Serial.print(", ");
  for (int receiver = 0; receiver < 12; receiver++) {
    // Make sure the receiver pin is low 
    pinMode(analog_pins[receiver], OUTPUT);
    digitalWrite(analog_pins[receiver], 0);
    // switch the main pin to INPUT and do an analog read from it (discard this read). This should set the mux to accept it.
    pinMode(analog_pins[receiver], INPUT);
    int value;
    value = analogRead(analog_pins[receiver]); // discard this read
    //Serial.print("|");
    //Serial.print(receiver);
    //Serial.print("|, ");
    for (int sender = 0; sender < 12; sender++) {
      if (   (sender == 0 && ((receiver == 2) ||  (receiver == 3) || (receiver == 5)))
          || (sender == 1 && ((receiver == 2) ||  (receiver == 4) ))
          || (sender == 2 && ((receiver == 0) ||  (receiver == 1) ||  (receiver == 4) ||  (receiver == 5) ))
          || (sender == 3 && ((receiver == 0) ||  (receiver == 5) ||  (receiver == 6) ))
          || (sender == 4 && ((receiver == 0) ||  (receiver == 1) ||  (receiver == 2) ||  (receiver == 5) ||  (receiver == 7) ||  (receiver == 8) ))
          || (sender == 5 && ((receiver == 0) ||  (receiver == 2) ||  (receiver == 3) ||  (receiver == 4) ||  (receiver == 6) ||  (receiver == 8) ))
          || (sender == 6 && ((receiver == 3) ||  (receiver == 4) ||  (receiver == 5) ||  (receiver == 8) ||  (receiver == 9) ))
          || (sender == 7 && ((receiver == 4) ||  (receiver == 8) ||  (receiver == 10) ||  (receiver == 11) ))
          || (sender == 8 && ((receiver == 4) ||  (receiver == 5) ||  (receiver == 6) ||  (receiver == 7)  ||  (receiver == 9)  ||  (receiver == 10)  ||  (receiver == 11) ))
          || (sender == 9 && ((receiver == 6) ||  (receiver == 8) ||  (receiver == 11) ))
          || (sender == 10 && ((receiver == 7) ||  (receiver == 11) ))
          || (sender == 11 && ((receiver == 7) ||  (receiver == 8) ||  (receiver == 9) ||  (receiver == 10) ))
          ) {
        pinMode(analog_pins[sender], OUTPUT);
        //delay(1);
        pinMode(analog_pins[receiver], INPUT);
        //delay(1);
        digitalWrite(analog_pins[sender], 1);
        //delay(1);
        value = analogRead(analog_pins[receiver]); 
        Serial.print(value);
        Serial.print(", ");
        pinMode(analog_pins[receiver], OUTPUT);
        digitalWrite(analog_pins[receiver], 0);
        pinMode(analog_pins[sender], OUTPUT);
        digitalWrite(analog_pins[sender], 0);
      }
    }

  }
  Serial.println("],");
}
