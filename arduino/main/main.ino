#include <Servo.h>

const int NB_PLAYERS = 2;
const int BAUD_RATE = 9600;
const int SERVO_RAISED_POSITION = 90;
const int MIN_FAN_SPEED = 50;
const int READ_TIMEOUT = 100;
const int READ_DELAY = 10;

enum GameState {
  INITIAL,
  IN_PLAY,
  FINISHED
};
GameState gameState;

struct Player {
  Servo servo;
  int fanSpeed;
  int fanPin;
  int laserPin;
  int detectorPin;
  int servoPin;
  int servoRestingPosition;
};

// Arduino Uno pins configuration:
// Only pins 2 and 3 can generate interrupts. They must connect with the laser receivers.
// Only pins 3, 11 (Timer2), 9, 10 (Timer1), 5 and 6 (Timer0) have PWM capability.
// The fans have to be connected to one that has the same configuration as Timer2.
// https://www.arduino.cc/en/Tutorial/SecretsOfArduinoPWM 
Player players[NB_PLAYERS] = {
  { Servo(), 255, 3, 7, 12, 5, 0},
  { Servo(), 255, 11, 4, 2, 6, 180}
};
volatile Player winner;

/************** Interruption Routines (ISR) ******************/


void interruption_player_one() {
  if(gameState == IN_PLAY) {
    gameState = FINISHED;
    winner = players[0];
  }
}


void interruption_player_two() {
  if(gameState == IN_PLAY) {
    gameState = FINISHED;
    winner = players[1];
  }
}

/***************** Initialization ***************************/

void setup() {
  for(int i = 0; i < NB_PLAYERS; i++) {
    initializePinMode(players[i]);
    initializeState(players[i]);
  }

  //initializeInterruptions();
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
  gameState = INITIAL;
}

void initializeInterruptions(){
  // the attachInterrupt will currently not work because the first player's pin doesnt support interruption
  // we have to configure timer1 (pin9,10) like timer2 (pin3,11), since we need to use the pin 3 for interruptions
  attachInterrupt(digitalPinToInterrupt(players[0].detectorPin), interruption_player_one, FALLING);
  attachInterrupt(digitalPinToInterrupt(players[1].detectorPin), interruption_player_two, FALLING);
}

/***************** Main Routine ******************************/

void loop() {
  switch(gameState) {
    case INITIAL: {
      if(!waitUntilDataIsAvailable()){
        return;
      }
      startGameFlags();
      gameState = IN_PLAY;
      updateFanSpeed();
      break;
    }

    case IN_PLAY: {
      if(!waitUntilDataIsAvailable()){
        return;
      }
      updateFanSpeed();
      break;
    }
    
    case FINISHED:{
      Serial.write(winner.fanPin == players[0].fanPin ? "WINNER:0\n": "WINNER:1\n");
      endGameRoutine();
      gameState = INITIAL;
      break;      
    }
  }
}

void startGameFlags() {
  for(int i = 0; i < NB_PLAYERS; i++) {
    players[i].servo.write(SERVO_RAISED_POSITION);
  }
  delay(500);
  
  for(int i = 0; i < NB_PLAYERS; i++) {
    players[i].servo.write(players[i].servoRestingPosition);
  }
}

// Returns false when read timeout is reached
bool waitUntilDataIsAvailable() {
  int i = 0;
  while (Serial.available() < NB_PLAYERS) {
    if((i += READ_DELAY) > READ_TIMEOUT) {
      return false;
    }
    delay(READ_DELAY);
  }
  return true;
}

void updateFanSpeed() {
  for(int i = 0; i < NB_PLAYERS; i++) {
    players[i].fanSpeed = Serial.read();
    Serial.write(players[i].fanSpeed);
    analogWrite(players[i].fanPin, constrain(players[i].fanSpeed + MIN_FAN_SPEED, 0, 255));
  }
}

void endGameRoutine() {
  analogWrite(players[0].fanPin, 0);
  analogWrite(players[1].fanPin, 0);
  winner.servo.write(SERVO_RAISED_POSITION);
  delay(5000);
  winner.servo.write(winner.servoRestingPosition);
}
