#include <Servo.h>
#define NB_PLAYERS 2

int MIN_FAN_SPEED = 50;
Servo s1;
Servo s2;

struct Player {
  Servo servo;
  int fanSpeed;
  int fanPin;
  int laserPin;
  int detectorPin;
  int servoPin;
  int servoValue;
};
Player players[NB_PLAYERS] = {
  { s1, 255, 3, 7, 12, 5, 0},
  { s2, 255, 11, 4, 2, 6, 180}
};

void setup() {
  initializePins();
  Serial.begin(9600);
}

void initializePins() {
  for(int i = 0; i < NB_PLAYERS; i++) {
    pinMode(players[i].fanPin, OUTPUT);
    pinMode(players[i].laserPin, OUTPUT);
    pinMode(players[i].detectorPin, INPUT);
    digitalWrite(players[i].laserPin, HIGH);
    analogWrite(players[i].fanPin, players[i].fanSpeed);
    players[i].servo.attach(players[i].servoPin);
    players[i].servo.write(players[i].servoValue);
  }
}

void loop() {
  //  Lasers are currently broken
  //  for(int i = 0; i < NB_PLAYERS; i++) {
  //    checkEndGame(players[i], i);
  //  }

  waitUntilDataIsAvailable();
  updateFanSpeed();
  delay(100);
}

void checkEndGame(Player player, int id) {
  // The player wins if the phototransistor doesn't detect the laser anymore.
  if ( digitalRead(player.detectorPin) == 0 ) {    
    analogWrite(player.fanPin, 0);
    analogWrite(player.fanPin, 0);

    player.servo.write(90);
    delay(2000);
    player.servoValue = id == 0 ? 180: 0;
    player.servo.write(player.servoValue);

    Serial.println("Player won : " + id);
    while (1) { /* The game is finished */ }
  }
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
    analogWrite(players[i].fanPin, players[i].fanSpeed + MIN_FAN_SPEED);
  }
}
