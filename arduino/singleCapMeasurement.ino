/* Pin2 has external pu resistor 5k. 
 * Pin2 alternatives between low and input at period 1 s.
 * Pin4 is input wired from pin 2
 * Pin4 output copied to LED state
 */

int scl_write_pin = 2; 
int sda_write_pin = 3;

int scl_read_pin = 4;
int sda_read_pin = 5;


void delayy() {
  delayMicroseconds(10);
}


void startAd() {
  // clock should be high anyway - check this
  pinMode(scl_write_pin, INPUT);
  delayy();
  //Now lower sda to initiate comm
  pinMode(sda_write_pin, OUTPUT);
  digitalWrite(sda_write_pin, 0);
  delayy();
}


void stopAd() {
  // when entering, clock should be high
  // take control of data and pull it low, if it is not already
  pinMode(sda_write_pin, OUTPUT);
  digitalWrite(sda_write_pin, 0);
  delayy();
  // cycle the clock - lower
  pinMode(scl_write_pin, OUTPUT);
  digitalWrite(scl_write_pin, 0);
  delayy();
  // cycle the clock - raise
  pinMode(scl_write_pin, INPUT);
  delayy();
  // data goes high
  pinMode(sda_write_pin, INPUT);
  delayy();
}


void clockInABit(int bit) {
  //Lower clock 
  pinMode(scl_write_pin, OUTPUT);
  digitalWrite(scl_write_pin, 0);
  delayy();
  // Write data  
  if (bit == 1) {
    pinMode(sda_write_pin, INPUT);
  } else {
    pinMode(sda_write_pin, OUTPUT);
    digitalWrite(sda_write_pin, 0);
  }
  delayy();
  // Raise clock
  pinMode(scl_write_pin, INPUT);
  delayy();
}


void addressAd() {
  clockInABit(0);
  clockInABit(1);
  clockInABit(0);
  clockInABit(1);
  clockInABit(1);
  clockInABit(0);
  clockInABit(0);  
}


void acknowledge() {
  pinMode(scl_write_pin, OUTPUT);
  digitalWrite(scl_write_pin, 0);
  delayy();
  pinMode(sda_write_pin, INPUT);
  delayy();
  // Raise clock
  pinMode(scl_write_pin, INPUT);
  delayy();
  // at this point, the acknowledge should be pulled low by the device
  int sda_state = digitalRead(sda_read_pin);
  if (sda_state == 1) {
    Serial.println("acknowledge failed!");
  }
}


void sendByteAd(int dataByte) {
  int currentBit;
  currentBit = (dataByte & 0x80) != 0;
  clockInABit(currentBit);
  currentBit = (dataByte & 0x40) != 0;
  clockInABit(currentBit);
  currentBit = (dataByte & 0x20) != 0;
  clockInABit(currentBit);
  currentBit = (dataByte & 0x10) != 0;
  clockInABit(currentBit);
  currentBit = (dataByte & 0x8) != 0;
  clockInABit(currentBit);
  currentBit = (dataByte & 0x4) != 0;
  clockInABit(currentBit);
  currentBit = (dataByte & 0x2) != 0;
  clockInABit(currentBit);
  currentBit = (dataByte & 0x1) != 0;
  clockInABit(currentBit);
  acknowledge();
}

int readBit() {
  pinMode(scl_write_pin, OUTPUT);
  digitalWrite(scl_write_pin, 0); // lower clock
  delayy();
  pinMode(sda_write_pin, INPUT);
  delayy();
  // Raise clock
  pinMode(scl_write_pin, INPUT); // raise clock
  delayy();
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
  clockInABit(0); // write bit
  acknowledge();  
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
  clockInABit(0); // write bit
  acknowledge();  
  // break regAddr into bytes
  sendByteAd(regMsb);
  sendByteAd(regLsb);
  stopAd();

  startAd();
  addressAd(); // 7 bit I2C address
  // read bit
  clockInABit(1); // read bit
  acknowledge();
  int msb = readByteAd();
  // We acknowledge the first bit, by  clocking in a 0 - this means we want more data
  clockInABit(0);
  int lsb = readByteAd();
  // We acknowledge the second bit, by  clocking in a 1 - this means we don't want any more data
  clockInABit(1);
  stopAd();
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
  Serial.println("Programme AD7147 ...");

  // programme AD7147
  writeAd(0, 128, 0, 2);
  writeAd(0, 129, 0b11010000, 0);
  writeAd(0, 130, 0, 0);
  writeAd(0, 131, 0, 0);
}


// the loop function runs over and over again forever
void loop() {
  //Serial.println("Reading ... ");
  readAd(0, 0xE0);
  delay(1);
}
