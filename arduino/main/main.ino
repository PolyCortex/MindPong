#include <Servo.h>

const int NB_PLAYERS = 2;
const int BAUD_RATE = 9600;

const int MIN_FAN_SPEED = 50;
const int SERVO_RAISED_POSITION = 90;

struct Player {
  Servo servo;
  int fanSpeed;
  int fanPin;
  int laserPin;
  int detectorPin;
  int servoPin;
  int servoRestingPosition;
};
Player players[NB_PLAYERS] = {
  { Servo(), 255, 3, 7, 12, 5, 0},
  { Servo(), 255, 11, 4, 2, 6, 180}
};

void setup() {
  for(int i = 0; i < NB_PLAYERS; i++) {
    initializePinMode(players[i]);
    initializeState(players[i]);
  }
  
  Serial.begin(BAUD_RATE);
}

void initializePinMode(Player player) {
  pinMode(player.fanPin, OUTPUT);
  pinMode(player.laserPin, OUTPUT);
  pinMode(player.detectorPin, INPUT);
  player.servo.attach(player.servoPin);
}

void initializeState(Player player) {
  digitalWrite(player.laserPin, HIGH);
  analogWrite(player.fanPin, player.fanSpeed);
  player.servo.write(player.servoRestingPosition);
}

void loop() {
  //  Lasers are currently broken
  //  for(int i = 0; i < NB_PLAYERS; i++) {
  //    checkEndGame(players[i]);
  //  }

  waitUntilDataIsAvailable();
  updateFanSpeed();
}

void checkEndGame(Player player) {
  if (hasWon(player)) {    
    analogWrite(player.fanPin, 0);
    analogWrite(player.fanPin, 0);
    player.servo.write(SERVO_RAISED_POSITION);
    delay(2000);
    player.servo.write(player.servoRestingPosition);
    while (true) { /* The game is finished */ }
  }
}

bool hasWon(Player player) {
  return digitalRead(player.detectorPin) == LOW;
}

void waitUntilDataIsAvailable() {
  while (Serial.available() < NB_PLAYERS) {
    delay(10);
  }
}

void updateFanSpeed() {
  for(int i = 0; i < NB_PLAYERS; i++) {
    players[i].fanSpeed = Serial.read();
    Serial.write(players[i].fanSpeed);
    analogWrite(players[i].fanPin, constrain(players[i].fanSpeed + MIN_FAN_SPEED, 0, 255));
  }
}
