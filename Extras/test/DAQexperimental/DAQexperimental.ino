// Read Pot Adjustable Analog Voltage
// Use External voltage source
// Wire Potentiomenter to potPin

const int P1in = A0;
const int P2in = A5;
unsigned long ti;

void setup() {

  // Initiate serial Communications
  Serial.begin(9600);

  pinMode(P1in, INPUT); 
  pinMode(P2in, INPUT); 

}

// Code Start
void loop() {

  ti = millis();
  // Read Pot Value
  int val1 = analogRead(P1in);
  int val2 = analogRead(P2in);
  
  // Display Voltage in serial monitor
  Serial.print(ti);
  Serial.print(" ");
  Serial.print(val1);
  Serial.print(" ");  
  Serial.println(val2);

  // Delay for stability
  delay(1);

}
