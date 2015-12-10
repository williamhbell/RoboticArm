# Robotic Arm

Written by W. H. Bell [ http://www.whbell.net/ ]

This package contains some basic examples of how to drive the Maplin (OWI) robotic arm.

## Overview

The Maplin (OWI) robotic arm comes as a kit that includes a USB 
controller.  The robotic arm can be directly connected to a Raspberry 
Pi, where the electrical power for the five motors and the LED is 
provided by batteries in the base.  To connect to the robotic arm, the 
robotic arm should be turned on using the power switch on top of the 
unit and the USB should be connected.  If the motors are driven for too 
long, the gears will start to crunch.  If this happens, turn the 
robotic arm power off immediately and then correct the program.

## Programs

### simpleArm

To run the program type

sudo ./python/simpleArm.py

By default this will just turn on the LED for one second.  There are a 
set of commands that are commented out.  Try uncommenting the commands, 
but becareful not to run the motors for too long!  If they run for too 
long, the arm will overstretch and the gears will start to crunch.  If 
this happens, turn the robotic arm power supply off immediately.

### keyboardControl

To run the program type

sudo ./python/keyboardControl.py

This will open a ncurses based text menu.  It is possible to run two
or more motors at once by pressing the keys associated with the
commands.  If the motors are driven too far the gears will start to
crunch.  Therefore, be prepared to stop the arm quickly.

## Software dependencies

To install the software dependencies for the robotic arm type:

sudo -s
apt-get install -y python-setuptools python-dev
easy_install pip
pip install pyusb
exit
