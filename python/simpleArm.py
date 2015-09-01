#!/usr/bin/env python
# A simple program to manipulate the Maplin robotic arm
# W. H. Bell
#
import usb.core, usb.util, time

# A simple function to act on one motor or the LED at a time
def moveArm(roboArm,duration, cmd):
  roboArm.ctrl_transfer(0x40,6,0x100,0,cmd,1000)
  time.sleep(duration)
  roboArm.ctrl_transfer(0x40,6,0x100,0,[0,0,0],1000)

# Use a dict to store the bits for each motor direction and the LED.
movement = {}
movement["base_left"] = [0,1,0]
movement["base_right"] = [0,2,0]
movement["shoulder_up"] = [64,0,0]
movement["shoulder_down"] = [128,0,0]
movement["elbow_up"] = [16,0,0]
movement["elbow_down"] = [32,0,0]
movement["wrist_up"] = [4,0,0]
movement["wrist_down"] = [8,0,0]
movement["grip_open"] = [2,0,0]
movement["grip_close"] = [1,0,0]
movement["light_on"] = [0,0,1]
movement["light_off"] = [0,0,0]

# The main function
def main():

  # Try to connect to the robotic arm
  roboArm = usb.core.find(idVendor=0x1267, idProduct=0x0000)

  # If the connection fails, then raise an exception
  if roboArm is None:
    raise ValueError("Arm not found")
  
  # Turn the gip light on for 1 second
  moveArm(roboArm,1,movement["light_on"])

  # Uncomment the loop below to test all of the functions
  #for i in xrange(2):
  #  moveArm(roboArm,1,movement["light_on"])
  #  moveArm(roboArm,1,movement["shoulder_up"])
  #  moveArm(1,movement["shoulder_down"])
  #  moveArm(1,movement["elbow_down"])
  #  moveArm(1,movement["elbow_up"])
  #  moveArm(2,movement["wrist_up"])
  #  moveArm(2,movement["wrist_down"])
  #  moveArm(1,movement["grip_close"])
  #  moveArm(0.8,movement["grip_open"])
  #  moveArm(1,movement["light_off"])

# Call the main function if this file is executed
if __name__ == '__main__':
  main()
