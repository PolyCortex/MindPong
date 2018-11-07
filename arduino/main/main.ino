#include <Servo.h>

int PLAYER_1 = 1;
int PLAYER_2 = 2;

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

  digitalWrite(Laser1, HIGH);
  digitalWrite(Laser2, HIGH);
  s1.write(0);
  s2.write(180);
  Serial.begin(9600);
}

void loop() {
  //  Lasers are currently broken
  // checkEndGame(digitalRead(Detector1), PLAYER_1);
  // checkEndGame(digitalRead(Detector2), PLAYER_2);

  if (Serial.available()) {
    motorSpeed1 = Serial.read();
    motorSpeed2 = Serial.read();
    Serial.println("RECEIVED : " + motorSpeed1);
  }
    
  analogWrite(motorPin1, motorSpeed1);
  analogWrite(motorPin2, motorSpeed2);

  delay(100);
}

void checkEndGame(int winPlayer, int playerID) {
  Servo servo = playerID == PLAYER_1 ? s1: s2;
  int lastServoPosition = playerID == PLAYER_1 ? 180: 0;
  if ( winPlayer == 0 ) {

    analogWrite(motorPin1, 0);
    analogWrite(motorPin2, 0);

    servo.write(90);
    delay(2000);
    servo.write(lastServoPosition);

    Serial.println("Player won : " + playerID);
    while (1) {}
  }
}
