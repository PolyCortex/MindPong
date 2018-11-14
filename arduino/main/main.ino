#include <Servo.h>

enum Players {
  PLAYER_ONE,
  PLAYER_TWO
};

int MIN_FAN_SPEED = 50;

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
  analogWrite(motorPin1, motorSpeed1);
  analogWrite(motorPin2, motorSpeed2);
  s1.write(0);
  s2.write(180);
  Serial.begin(9600);
}

void loop() {
  //  Lasers are currently broken
  // checkEndGame(digitalRead(Detector1), PLAYER_ONE);
  // checkEndGame(digitalRead(Detector2), PLAYER_TWO);

  waitUntilDataIsAvailable();
  updateFanSpeed();
  delay(100);
}

void checkEndGame(int winPlayer, Players player) {
  Servo servo = player == PLAYER_ONE ? s1: s2;
  int finalFlagPosition = player == PLAYER_ONE ? 180: 0;

  // The player wins if the phototransistor doesn't detect the laser anymore.
  if ( winPlayer == 0 ) {
    analogWrite(motorPin1, 0);
    analogWrite(motorPin2, 0);

    servo.write(90);
    delay(2000);
    servo.write(finalFlagPosition);

    Serial.println("Player won : " + player);
    while (1) { /* The game is finished */ }
  }
}

void waitUntilDataIsAvailable() {
  while (Serial.available() < 2) {
    delay(10);
  }
}

void updateFanSpeed() {
  motorSpeed1 = Serial.read();
  motorSpeed2 = Serial.read();
  Serial.write(motorSpeed1);
  Serial.write(motorSpeed2);
  analogWrite(motorPin1, motorSpeed1 + MIN_FAN_SPEED);
  analogWrite(motorPin2, motorSpeed2 + MIN_FAN_SPEED);
}
