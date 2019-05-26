# MindPong

  

MindPong is a fantastic EEG multiplayer game requiring two Muse headbands and an arduino board. The goal is to move a ball by controlling a fan with your brain. The more you are focused, the more the fan rotates. We are interested in beta waves in order to establish how much you are focused. It relies entirely on the [pyMuse](https://github.com/PolyCortex/pyMuse) library. It is mainly used as a mean to popularize EEG technologies and neurosciences to the public.  Visit the MindPong wiki for a detailed description of MindPong related projects and ongoing developments (https://github.com/PolyCortex/MindPong/wiki).
  
## Game

To play a game of Mindpong, we'll need two players and an operator. The role of the players are to answers the randomly generated math questions and to relax when it is asked. The role of the operator is to start a game, to control the flow of the game and to ask the players to relax when he wants to.

The Mindpong interface displays three sections:

- A play tab where the game takes place.
- An analysis tab that features eeg signal graphics and spectrograms.
- A settings tab to setup the communication.

![Interface of Mindpong](https://lh3.googleusercontent.com/B1HaWQ-g6CeQk5Wn0FcjbYWXwTdrNBvXyfggDLommGk11zaciuiIpC7W1LnE8SFuzzOwKTqNOr57)

*Figure 1: Play section of the mindpong app.*

The goal of the game is to compare the EEG activity when a subject is doing calculation v.s. when the subject is relaxing. To do so, the application generates random math questions and feature a relaxing mode.

## Hardware setup

  

![](https://lh3.googleusercontent.com/hYLyprlF2NU10iol23kcK9le9mxZFwJHhowW4WIG_MiD-Xwt7dxBypljR12KK2bUvDECs3nIVfNz  "Mindpong")

  

*Figure 2 : rough idea of our hardware setup*

  

The necessary setup is a ping pong ball in a transparent plastic tube with two fans at the edges of the tube. They are connected to an Arduino Uno which is linked to a computer which then receives the signal from two Muse headbands via bluetooth. We use Muse Direct to obtain beta waves from the headbands.

  

### Electrical circuits

  

We use two independent circuits to make the game work. The first one allows the arduino to control the fans and the second one allows the microcontroller to raise a cute little flag for the winner.

  

#### Fan control circuit

  

The circuit makes it possible to use a [PWM](https://en.wikipedia.org/wiki/Pulse-width_modulation) to control the fans' speed. To do so, a transistor (N-MOSFET) blocks and enables the 12V current to flow to the fans. We are using a [flyback diode](https://en.wikipedia.org/wiki/Flyback_diode) to provide a path to dissipate energy stored by the motor inductance.

  

![Fan Circuit](https://lh3.googleusercontent.com/FvU2NcXTf2U4deSbWsVEagh_gK9IJBwsLBZUwifjeJtzx3YXEerjKFWneWsKj4rK-UNyDokOJA0V  "Fan Circuit")

We need two of this circuit to power the two fans.

  

#### Laser and laser receiver circuit

  

The flags circuit is really simple. It is composed of three components for each of the two flags: a laser emitter, a laser receiver and a servomotor with the flag affixed to it. They are all linked to the arduino's GPIOs (digital pins) and powered by the 5V output of the arduino. The software reproduces the following behavior: when the laser emitter loses the light signal (the ball passes over it), the flag is raised.

  

## Installation

You will need a few tools to get started with Muse headset and pyMuse:

  

*  [MuseDirect](https://www.microsoft.com/en-us/p/muse-direct/9p0mbp6nv07x?activetab=pivot:overviewtab) (Windows)

  

*  [Python 3.7](https://www.python.org/downloads/release/python-370/)

  

Don't hesitate to go on [Muse Developer website](http://developer.choosemuse.com/) for additionnal information.

  
  

### Installation of dependencies

  

Simply use pip in order to install all of the project's dependencies.

  
  

> pip install -r requirements.txt

  
  

Pip should install all requirements, including:

  

*  [pyserial](https://github.com/pyserial/pyserial)

*  [PyQtGraph](http://www.pyqtgraph.org/)

*  [pyMuse](https://github.com/PolyCortex/pyMuse/) and its own dependencies

*  [PyQt5](https://www.riverbankcomputing.com/software/pyqt/intro)

  

## Getting started

  

### To run mindpong.py on Windows

  

1. Connect your two Muse headsets with your computer by bluetooth

  

2. Start Muse Direct and set an OSC UDP output for player one and player two:

  

![One headband needs to output his eeg relative data by OSC UDP on port 5001 (Player One)](https://lh3.googleusercontent.com/ScMKcED4j-zZorx4d1T5wt1C1Bj77RoG66tWXi9HJK2lW6FCJ8ExcOokcgxV4x3xf13MWFBWTVI  "PlayerOne")

*Figure 2 : output setup for player one*

  

![The other headband needs to output his eeg relative data by OSC UDP on port 5002 (Player Two)](https://lh3.googleusercontent.com/MM86nkKx5G34gXIX4TYHwlmRQV4f8bnHP-k2PH3dKrEQqoPWGavZH2RPWB_6ZrzbBIz-VCZe9q4  "Player Two")

*Figure 3 : output setup for player two*

  

3. Start ./mindpong.py in a terminal:

  

> python ./mindpong.py

  

4. Press play.
