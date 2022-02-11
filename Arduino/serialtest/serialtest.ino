#include <SPI.h>
#include <SD.h>

#define FILE_NAME "inc.txt" //file with next file name (unique naming per file)

//FILE NAMING VARIABLES
File myFile;
String fileNm = "";
const int INTERVAL = 10; //interval to read at (milliseconds) set at 10 for 100hz 
unsigned long start;
int num;

//RELAY CONTROL Variables
const int relayPins[] = {10, 9, 6, 14};
char in;
int state = 0;
int pin;


//Sensor analog Read variables
int a0, a1, a2, a3;

//boolean controls whether file can be written tos
bool fil = true;



void setup() {
  //Initialize Serial Monitor
  Serial.begin(115200);

  // test on board LED
  pinMode(13, OUTPUT);

  Serial.println("START");

  delay(3000);

  Serial.println("TURNON");
  pinMode(13, LOW);
  delay(2000);
  Serial.println("TURNOFF");
  pinMode(13, HIGH);


  /*
  //Declare relay pins as OUTPUTS
  for (int i = 0; i < sizeof(relayPins); i++) {
    pinMode(relayPins[i], OUTPUT);
  }
  
  //INITIALIZE SD CARD
  Serial.print("Initializing SD card...");
  if (!SD.begin(4)) {
    Serial.println("initialization failed!");
    for(int i = 3; i >= 1; i--) {
      Serial.println(i);
      delay(1000);
    }
    Serial.println("Logger START");
    delay(1000);
    Serial.println("Time\tA0\tA1\tA2\tA3");
    
    //CALIBRATION
    pinMode(A0, INPUT);
    pinMode(A1, INPUT);
    pinMode(A2, INPUT);
    pinMode(A3, INPUT);
    fil = false;
    start = millis();
    return;
  }

  //READING FILE_NAME to name current file
  myFile = SD.open(FILE_NAME);
  if(myFile) {
    while (myFile.available()) {
      num = myFile.parseInt();
      Serial.println(num);
    }
    myFile.close();
  }else{
    Serial.println("error opening");
  }

  //.txt or .dat file
  fileNm = String(num) + ".txt";
  Serial.println("File Name: " + String(fileNm));
  num++;

  //WRITING TO FILE
  myFile = SD.open(FILE_NAME, FILE_WRITE);
  if(myFile) {
    myFile.println();
    myFile.print(int(num));
    myFile.close();
  }else{
    Serial.println("error opening");
  }

  //INITIALIZE NEW FILE
  myFile = SD.open(String(fileNm), FILE_WRITE);
  myFile.println("Time\tA0\tA1\tA2\tA3");
  myFile.close();
  
  //CALIBRATION
  pinMode(A0, INPUT);
  pinMode(A1, INPUT);
  pinMode(A2, INPUT);
  pinMode(A3, INPUT);
  
  //3 second delay
  for(int i = 3; i >= 1; i--) {
    Serial.println(i);
    delay(1000);
  }
  
  Serial.println("Logger START");
  delay(1000);
  Serial.println("Time\tA0\tA1\tA2\tA3");
  start = millis(); //Initialized timer zero

  */
}

void loop() {

  //save analog values to variables (0 - 1023)
  a0 = analogRead(A0);
  a1 = analogRead(A1);
  a2 = analogRead(A2);
  a3 = analogRead(A3);
  
  //record data values at every INTERVAL
  if((millis()- start) % INTERVAL == 0){

    //PRINT ANALOG INPUT TO SERIAL
    Serial.print(String(millis() - start) + "\t");
    Serial.print(String(a0) + "\t");
    Serial.print(String(a1) + "\t");
    Serial.print(String(a2) + "\t");
    Serial.print(String(a3));
    
    /*
    if(fil){ //Check if file has been made
      myFile = SD.open(String(fileNm), FILE_WRITE);
      if(myFile) {
        myFile.println(String(millis() - start) + "\t" + String(a0) + "\t" + String(a1) + "\t" + String(a2) + "\t" + String(a3));
      }else{
        Serial.print("\terror opening " + String(fileNm));
      }
      myFile.close();
    }

    Serial.println();

    */
    
  }


  //SWITCHBOX CONTROL
  if(Serial.available() > 0) {
      //READ SERIAL MONITOR USER INPUT
      in = Serial.read(); //.read() is non-blocking function (minimal delay 
      Serial.println(in);

      Serial.println("yo");
      
      if (in == 'T') {
        delay(1000);
        Serial.println("TURNON LED");
        digitalWrite(13, HIGH);
        delay(5000);
        digitalWrite(13, LOW);
        delay(1000);
      }

      if(in == '0'){
        
        digitalWrite(relayPins[0], LOW);
        
      }else if(in == '1'){
        
        digitalWrite(relayPins[0], HIGH);
        
      }else if(in == '2'){
        
        digitalWrite(relayPins[1], LOW);
        
      }else if(in == '3'){
        
        digitalWrite(relayPins[1], HIGH);
        
      }else if(in == '4'){
        
        digitalWrite(relayPins[2], LOW);
        
      }else if(in == '5'){
        
        digitalWrite(relayPins[2], HIGH);
        
      }else if(in == '6'){
        
        digitalWrite(relayPins[3], LOW);
        
      }else if(in == '7'){
        
        digitalWrite(relayPins[3], HIGH);
        
      }else if(in == '8'){
        
        //All RELAY OFF
        for(int i = 0; i < sizeof(relayPins); i++){
          digitalWrite(relayPins[i], LOW);
        }
        
      }else if(in == '9'){
        Serial.println("Startup Sequence");
      }
      
  }

}
