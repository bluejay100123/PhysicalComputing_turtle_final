#include <SoftwareSerial.h>
SoftwareSerial bluetooth(10, 11);

int flexPin = A2;
int flexValue = 0;

void setup(){
  Serial.begin(9600);
  bluetooth.begin(9600);
  pinMode(flexPin, INPUT);
}

void loop(){
  flexValue = analogRead(flexPin);
  //Serial.println(flexValue);
  bluetooth.println(flexValue);
  delay(100);
}

/* How to use a flex sensor/resistro - Arduino Tutorial
   Fade an LED with a flex sensor
   More info: http://www.ardumotive.com/how-to-use-a-flex-sensor-en.html
   Dev: Michalis Vasilakis // Date: 9/7/2015 // www.ardumotive.com  */
   
/*
//Constants:
const int flexPin = A2; //pin A0 to read analog input

//Variables:
int value; //save analog value

void setup(){
  Serial.begin(9600);       //Begin serial communication
}

void loop(){
  
  value = analogRead(flexPin);         //Read and save analog value from potentiometer
  Serial.println(value);               //Print value
  delay(100);                          //Small delay
}

*/