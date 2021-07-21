/*  Using Arduino to interface to AD7147 capacitance sensor
 *  Using Arduino 'Due', because 3.3V operation required for AD7147
 *  Not using dedicated i2c lines but rather using 2 selected digital pins for scl and sda.
 *  Both wires have external pull-up resistor (used 5.1 k-Ohm). 
 *  Using 2 different pins to read in those same wires - this is for debugging - to check wiring integrity.
 */

int scl_write_pin = 2; 
int sda_write_pin = 3;

int scl_read_pin = 4;
int sda_read_pin = 5;


/* A generic delay between protocol steps 
 * Perhaps this could be lowered - depends on wiring quality; ad7147 can accept up to 400kHz clock
 * The AD7147 also has different timing constraints for up and down clock phases. 
 */
void wait() {
  delayMicroseconds(10); 
}


void startAd() {
  // clock should be high coming into this - make sure it is
  pinMode(scl_write_pin, INPUT);
  wait();
  //Now lower sda to initiate comm
  pinMode(sda_write_pin, OUTPUT);
  digitalWrite(sda_write_pin, 0);
  wait();
}


void stopAd() {
  // when entering, clock should be high
  // take control of data and pull it low, if it is not already
  pinMode(sda_write_pin, OUTPUT);
  digitalWrite(sda_write_pin, 0);
  wait();
  // cycle the clock - lower
  pinMode(scl_write_pin, OUTPUT);
  digitalWrite(scl_write_pin, 0);
  wait();
  // cycle the clock - raise
  pinMode(scl_write_pin, INPUT);
  wait();
  // data goes high
  pinMode(sda_write_pin, INPUT);
  wait();
}


void sendBit(int bit) {
  //Lower clock 
  pinMode(scl_write_pin, OUTPUT);
  digitalWrite(scl_write_pin, 0);
  wait();
  // Write data  
  if (bit == 1) {
    pinMode(sda_write_pin, INPUT);
  } else {
    pinMode(sda_write_pin, OUTPUT);
    digitalWrite(sda_write_pin, 0);
  }
  wait();
  // Raise clock
  pinMode(scl_write_pin, INPUT);
  wait();
}

// Hardcoded address of AD7147 - the last two bits are wirable
void addressAd() {
  sendBit(0);
  sendBit(1);
  sendBit(0);
  sendBit(1);
  sendBit(1);
  sendBit(0);
  sendBit(0);  
}


void receiveAcknowledge() {
  pinMode(scl_write_pin, OUTPUT);
  digitalWrite(scl_write_pin, 0);
  wait();
  pinMode(sda_write_pin, INPUT);
  wait();
  // Raise clock
  pinMode(scl_write_pin, INPUT);
  wait();
  // at this point, the acknowledge should be pulled low by the device
  int sda_state = digitalRead(sda_read_pin);
  if (sda_state == 1) {
    Serial.println("acknowledge failed!");
  }
}


void sendByteAd(int dataByte) {
  int currentBit;
  currentBit = (dataByte & 0x80) != 0;
  sendBit(currentBit);
  currentBit = (dataByte & 0x40) != 0;
  sendBit(currentBit);
  currentBit = (dataByte & 0x20) != 0;
  sendBit(currentBit);
  currentBit = (dataByte & 0x10) != 0;
  sendBit(currentBit);
  currentBit = (dataByte & 0x8) != 0;
  sendBit(currentBit);
  currentBit = (dataByte & 0x4) != 0;
  sendBit(currentBit);
  currentBit = (dataByte & 0x2) != 0;
  sendBit(currentBit);
  currentBit = (dataByte & 0x1) != 0;
  sendBit(currentBit);
  receiveAcknowledge();
}

int readBit() {
  pinMode(scl_write_pin, OUTPUT);
  digitalWrite(scl_write_pin, 0); // lower clock
  wait();
  pinMode(sda_write_pin, INPUT);
  wait();
  // Raise clock
  pinMode(scl_write_pin, INPUT); // raise clock
  wait();
  // at this point, sda has the bit from the AD
  int sda_state = digitalRead(sda_read_pin);
  return sda_state;
}


int readByteAd() {
  int value = 0;
  value = value + readBit() * 0x80;
  value = value + readBit() * 0x40;
  value = value + readBit() * 0x20;
  value = value + readBit() * 0x10;
  value = value + readBit() * 0x8;
  value = value + readBit() * 0x4;
  value = value + readBit() * 0x2;
  value = value + readBit() * 0x1;
  return value;
}


void writeAd(int regMsb, int regLsb, int dataMsb, int dataLsb) {
  startAd();
  addressAd(); // 7 bit I2C address
  // write bit
  sendBit(0); // write bit
  receiveAcknowledge();  
  // break regAddr into bytes
  sendByteAd(regMsb);
  sendByteAd(regLsb);
  sendByteAd(dataMsb);
  sendByteAd(dataLsb);
  stopAd();
}

void readAd(int regMsb, int regLsb) {
  startAd();
  addressAd(); // 7 bit I2C address
  // write bit
  sendBit(0);
  receiveAcknowledge();  
  // break regAddr into bytes
  sendByteAd(regMsb);
  sendByteAd(regLsb);
  stopAd();

  startAd();
  addressAd(); // 7 bit I2C address
  // read bit
  sendBit(1); // read bit
  receiveAcknowledge();
  int msb = readByteAd();
  // We acknowledge the first bit, by  clocking in a 0 - this means we want more data
  sendBit(0);
  int lsb = readByteAd();
  // We acknowledge the second bit, by  clocking in a 1 - this means we don't want any more data
  sendBit(1);
  stopAd();
  // output timestamp and value as array, to copy and paste straight into python IDE
  int result = msb * 256 + lsb;
  Serial.print("[");
  Serial.print(millis());
  Serial.print(", ");
  Serial.print(result);
  Serial.println("],");
  
}


// Debugging: Use this function at any point to check the state of the two wires
void serialState() {
  int scl_state = digitalRead(scl_read_pin);
  int sda_state = digitalRead(sda_read_pin);
  Serial.print("current state: sclk: ");
  Serial.print(scl_state);
  Serial.print(" sda: ");
  Serial.print(sda_state);
  Serial.println(" ");
}


// the setup function runs once when you press reset or power the board
void setup() {
  // initialize digital pins
  pinMode(scl_write_pin, INPUT);
  pinMode(sda_write_pin, INPUT);
  pinMode(scl_read_pin, INPUT);
  pinMode(sda_read_pin, INPUT);

  // make sure power has gotten to AD7147
  delay(1000);

  Serial.begin(9600);
  while (!Serial);
  Serial.println("Programming AD7147 ...");
  // This programmes the Phase 0 registers to do single sided measurement from input 0. 
  writeAd(0, 128, 0, 2);
  writeAd(0, 129, 0b11010000, 0);
  writeAd(0, 130, 0, 0); // not sure if from here onwards is necessary.
  writeAd(0, 131, 0, 0);
  Serial.println("Programmed");
}


void loop() {
  //Serial.println("Reading ... ");
  readAd(0, 0xE0);
  //delay(1);
}
