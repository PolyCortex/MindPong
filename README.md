# MindPong

MindPong is a fantastic EEG multiplayer game requiring two Muse headbands and an arduino board. The goal is to move a ball by controlling a fan with your brain. The more you are focused, the more the fan rotates. We are interested in beta waves in order to establish how much you are focused. It relies entirely on the [pyMuse](https://github.com/PolyCortex/pyMuse) library.

## Hardware setup

![](https://lh3.googleusercontent.com/hYLyprlF2NU10iol23kcK9le9mxZFwJHhowW4WIG_MiD-Xwt7dxBypljR12KK2bUvDECs3nIVfNz  "Mindpong")

*Figure 1 : rough idea of our hardware setup.*

The necessary setup is a ping pong ball in a transparent plastic tube with two fans at the edges of the tube. They are connected to an Arduino Uno wich is linked to a computer which receives the signal from two Muse headbands via bluetooth. We use Muse Direct/MuseIO to obtain beta waves from the headbands.

### Electrical circuits

We use two independent circuits to make the game work. The first one allows the arduino to control the fans and the second one allows the microcontroller to raise a cute little flag for the winner.

#### Fan control circuit

The circuit makes it possible to use a [PWM](https://en.wikipedia.org/wiki/Pulse-width_modulation) to control the fans' speed. To do so, a transistor (N-MOSFET) blocks and enables the 12V current to flow to the fans. We are using a [flyback diode](https://en.wikipedia.org/wiki/Flyback_diode) to provide a path to dissipate energy stored by the motor inductance.

![Fan Circuit](https://lh3.googleusercontent.com/FvU2NcXTf2U4deSbWsVEagh_gK9IJBwsLBZUwifjeJtzx3YXEerjKFWneWsKj4rK-UNyDokOJA0V "Fan Circuit")
We need two of this circuit to power the two fans.

#### Laser and laser receiver circuit

The flags circuit is really simple. It is composed of three components for each of the two flags: a laser emitter, a laser receiver and a servomotor with the flag affixed to it. They are all linked to the arduino's GPIOs (digital pins) and powered by the 5V output of the arduino. The software reproduces the following behavior: when the laser emitter loses the light signal (the ball passes over it), the flag is raised.

## Installation
You will need a few tools to get started with Muse headset and pyMuse:

*  [MuseDirect](http://developer.choosemuse.com/tools/windows-tools) (Windows) or [MuseIO](http://developer.choosemuse.com/tools/mac-tools) (MacOS) or [MuseIO](http://developer.choosemuse.com/tools/linux-tools)(Linux)

*  [Python 3.7](https://www.python.org/downloads/release/python-370/)

Don't hesitate to go on [Muse Developer website](http://developer.choosemuse.com/) for additionnal information.

### Prerequisites

You must have Python 3.7 installed and you must have installed the toolkit from the [Muse Developper website](http://developer.choosemuse.com/tools/windows-tools).


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


### To run mindpong.py on MacOS/Linux


1. Connect your two Muse headsets with your computer by bluetooth

2. Start two terminal and run Muse IO in each. Set an OSC UDP output for player one (localhost:5001) and player two (localhost:5002):

> muse-io --device Muse-XXXX --osc osc.udp://localhost:5001

  
> muse-io --device Muse-XXXX --osc osc.udp://localhost:5002

3. Start ./mindpong.py in a terminal:
  
> python ./mindpong.py

4. Press play.
