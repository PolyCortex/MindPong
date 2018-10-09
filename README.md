# MindPong

MindPong is a fantastic EEG multiplayer game requiring two Muse headbands and an arduino. The goal is to push a ball by controlling a fan with your brain. The more you're focused, the more the fan rotates. We're interested in beta waves in order to establish how much you're focused. It relies entirely on the [pyMuse](https://github.com/PolyCortex/pyMuse) library.

## Hardware setup
![](https://lh3.googleusercontent.com/0qZbfWiSNkhvY9a1p-VeWJkkqcerjlyOVvZsjT5voVrMULuboeTstvmIPuugCrhioYp3C4fIoH8 "MindPong")

*Figure 1 : rough idea of our hardware setup.*

The necessary setup is a ping pong ball in a translucent plastic  tube with two fans at the edges of the tube. They are connected to an Arduino Uno wich is linked to a computer that is receiving the signal of two Muse headbands via bluetooth. We use [Muse Direct](http://www.choosemuse.com/direct/) to get beta waves from the headbands.

## Installation of dependencies

You will need some tools to get started with Muse headset and pyMuse:
* [MuseDirect](http://www.choosemuse.com/direct/)
* [Python 2.7](https://www.python.org/downloads/release/python-2714/)

Don't hesitate to go on [Muse Developer website](http://www.choosemuse.com/developer/) to get information.

### Prerequisites

You must have Python 2.7 installed, [Muse Direct](https://www.microsoft.com/en-us/p/muse-direct/9p0mbp6nv07x) and your operating system must be Windows.

### Installation

In order to install all the dependencies of this project just use pip.

> pip install -r requirements.txt

Pip should install all requirements, including:
* pexpect
* [pyMuse](https://github.com/PolyCortex/pyMuse/) and its own dependencies
* [PyQt4](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyqt4)

## Getting started
### Setup Muse Direct

 1. Connect your two Muse headsets with your computer by bluetooth
 2. Start Muse Direct and set OSC UDP output for player one and player two:
	
  ![One headband needs to output his eeg relative data by OSC UDP on port 5001 (Player One)](https://lh3.googleusercontent.com/ScMKcED4j-zZorx4d1T5wt1C1Bj77RoG66tWXi9HJK2lW6FCJ8ExcOokcgxV4x3xf13MWFBWTVI "PlayerOne")
	
  *Figure 2 : output setup for player one*
 
 ![The other headband needs to output his eeg relative data by OSC UDP on port 5002 (Player Two)](https://lh3.googleusercontent.com/MM86nkKx5G34gXIX4TYHwlmRQV4f8bnHP-k2PH3dKrEQqoPWGavZH2RPWB_6ZrzbBIz-VCZe9q4 "Player Two")
   
  *Figure 3 : output setup for player two*
  
 4. Start ./mindpong.py in a terminal:

> python ./mindpong.py

4. Press play.

