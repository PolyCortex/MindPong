
# MindPong

MindPong is a fantastic EEG multiplayer game requiring two Muse headbands and an arduino. The goal is to push a ball by controlling a fan with your brain. The more you're focused, the more the fan rotates. We're interested in beta waves in order to establish how much you're focused. It relies entirely on the [pyMuse](https://github.com/PolyCortex/pyMuse) library.

## Hardware setup
![](https://lh3.googleusercontent.com/0qZbfWiSNkhvY9a1p-VeWJkkqcerjlyOVvZsjT5voVrMULuboeTstvmIPuugCrhioYp3C4fIoH8 "MindPong")

*Figure 1 : rough idea of our hardware setup.*

The necessary setup is a ping pong ball in a translucent plastic  tube with two fans at the edges of the tube. They are connected to an Arduino Uno wich is linked to a computer that is receiving the signal of two Muse headbands via bluetooth. We use Muse Direct/MuseIO to get beta waves from the headbands.

## Installation

You will need some tools to get started with Muse headset and pyMuse:
* [MuseDirect](http://developer.choosemuse.com/tools/windows-tools) (Windows) or [MuseIO](http://developer.choosemuse.com/tools/mac-tools) (MacOS) or [MuseIO](http://developer.choosemuse.com/tools/linux-tools)(Linux)
* [Python 2.7](https://www.python.org/downloads/release/python-2714/)

Don't hesitate to go on [Muse Developer website](http://developer.choosemuse.com/) to get information.

### Prerequisites

You must have Python 2.7 installed and you must have installed the toolkit from the [Muse Developper website](http://developer.choosemuse.com/tools/windows-tools).

### Installation of dependencies

In order to install all the dependencies of this project just use pip.

> pip install -r requirements.txt

Pip should install all requirements, including:
* pexpect
* [pyMuse](https://github.com/PolyCortex/pyMuse/) and its own dependencies
* [PyQt4](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyqt4)

## Getting started
### To run mindpong.py on Windows

 1. Connect your two Muse headsets with your computer by bluetooth
 2. Start Muse Direct and set OSC UDP output for player one and player two:
  ![One headband needs to output his eeg relative data by OSC UDP on port 5001 (Player One)](https://lh3.googleusercontent.com/ScMKcED4j-zZorx4d1T5wt1C1Bj77RoG66tWXi9HJK2lW6FCJ8ExcOokcgxV4x3xf13MWFBWTVI "PlayerOne")

  *Figure 2 : output setup for player one*
 
 ![The other headband needs to output his eeg relative data by OSC UDP on port 5002 (Player Two)](https://lh3.googleusercontent.com/MM86nkKx5G34gXIX4TYHwlmRQV4f8bnHP-k2PH3dKrEQqoPWGavZH2RPWB_6ZrzbBIz-VCZe9q4 "Player Two")
   
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
