#include <Servo.h>
Servo s1;
Servo s2;

int motorPin1   = 3;
int Laser1      = 7;
int Detector1   = 12;
int servo1      = 5;

int motorPin2   = 11;
int Laser2      = 4;
int Detector2   = 2;
int servo2      = 6;

int motorSpeed1 = 255;
int motorSpeed2 = 255;

void setup() {
  s1.attach(servo1);
  s2.attach(servo2);
  pinMode(motorPin1, OUTPUT);
  pinMode(motorPin2, OUTPUT);
  pinMode(Laser1, OUTPUT);
  pinMode(Detector1, INPUT);
  pinMode(Laser2, OUTPUT);
  pinMode(Detector2, INPUT);

  analogWrite(motorPin1, 0);
  analogWrite(motorPin2, 0);
  Serial.begin(9600);
  Serial.print("Hello Computer");
}

void loop() {
  digitalWrite(Laser1, HIGH);
  digitalWrite(Laser2, HIGH);
  s1.write(0);
  s2.write(180);

  int win1 = digitalRead(Detector1);
  int win2 = digitalRead(Detector2);

//  if ( win1 == 0 ) {
//    analogWrite(motorPin1, 0);
//    analogWrite(motorPin2, 0);
//    s2.write(90);
//    delay(2000);
//    s2.write(180);
//    Serial.println("Player 1 won");
//    while (1) {}
//  }
//
//  if ( win2 == 0 ) {
//    analogWrite(motorPin1, 0);
//    analogWrite(motorPin2, 0);
//    s1.write(90);
//    delay(2000);
//    s1.write(0);
//    Serial.println("Player 2 won");
//    while (1) {}
//  }
//
  if (Serial.available()) {
    String data = Serial.readString();
    String dataP1 = data.substring(0, 3);
    String dataP2 = data.substring(3, 6);
    int museDataP1 = dataP1.toInt();
    int museDataP2 = dataP2.toInt();
    Serial.println("RECEIVED : " + data);
    if (museDataP1 >= 100 and museDataP2 >= 100) {
      motorSpeed1 = museDataP1 - 50;
      motorSpeed2 = museDataP2 - 50;
    }
  }
  analogWrite(motorPin1, motorSpeed1);
  analogWrite(motorPin2, motorSpeed2);
  delay(100);
}
