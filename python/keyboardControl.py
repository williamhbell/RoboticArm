#!/usr/bin/env python
# Robotic arm manipulation with the keyboard and the ncurses module.
# W. H. Bell
import curses
import usb.core, usb.util

#---------------------------------------------------
# A function to check if the bit corresponding to the search command
# is already set or not.
def commandSet(currentCmd, searchCmd):
  if len(currentCmd) != 3 or len(searchCmd) != 3:
    raise ValueError("currentCmd or searchCmd not 3 elements")

  #  Loop over the current command and check if this bit is set
  for i in xrange(3):
     if (currentCmd[i] & searchCmd[i]) > 0:
        return True
  return False

#---------------------------------------------------
# The main function
def main():

  # Try to connect to the robotic arm
  roboArm = usb.core.find(idVendor=0x1267, idProduct=0x0000)

  # If the connection fails, then raise an exception
  if roboArm is None:
    raise ValueError("Arm not found")

  # Create a ncurses screen
  stdscr = curses.initscr()

  # Turn off the character echo
  curses.noecho()

  # Turn off the requirement for the enter key to be pressed after the 
  # key.
  curses.cbreak()

  # Add the menu strings
  stdscr.addstr(0,0,"=================================================")
  stdscr.addstr(1,16,"Maplin robotic arm",curses.A_BOLD)
  stdscr.addstr(2,0,"=================================================")
  stdscr.addstr(3,0," LED on: 1")
  stdscr.addstr(4,0," Grip open: q              Grip closed: a")
  stdscr.addstr(5,0," Wrist up: w               Wrist down: s")
  stdscr.addstr(6,0," Elbow up: e               Elbow down: d")
  stdscr.addstr(7,0," Shoulder up: r            Shoulder down: f")
  stdscr.addstr(8,0," Base left: z              Base right: x")
  stdscr.addstr(12,0," To stop motion: space     To quit: Esc")
  stdscr.addstr(14,0,"=================================================")  

  # Update the terminal with the menu strings
  stdscr.refresh()

  # Use a dict to store the bits for each motor direction and the LED,
  # where th integer value corresponding to the ASCII character is used 
  # as the key
  cmds = {}
  cmds[ord('z')] = [0,1,0]
  cmds[ord('x')] = [0,2,0]
  cmds[ord('r')] = [64,0,0]
  cmds[ord('f')] = [128,0,0]
  cmds[ord('e')] = [16,0,0]
  cmds[ord('d')] = [32,0,0]
  cmds[ord('w')] = [4,0,0]
  cmds[ord('s')] = [8,0,0]
  cmds[ord('q')] = [2,0,0]
  cmds[ord('a')] = [1,0,0]
  cmds[ord('1')] = [0,0,1]
  cmds[ord(' ')] = [0,0,0]

  # Store the keys for the dict, to prevent many function calls.
  cmdKeys = cmds.keys()

  # A dict to store the opposite command in string form.
  antiCmds = {}
  antiCmds["[0, 1, 0]"] = [0,2,0]
  antiCmds["[0, 2, 0]"] = [0,1,0]
  antiCmds["[64, 0, 0]"] = [128,0,0]
  antiCmds["[128, 0, 0]"] = [64,0,0]
  antiCmds["[16, 0, 0]"] = [32,0,0]
  antiCmds["[32, 0, 0]"] = [16,0,0]
  antiCmds["[4, 0, 0]"] = [8,0,0]
  antiCmds["[8, 0, 0]"] = [4,0,0]
  antiCmds["[2, 0, 0]"] = [1,0,0]
  antiCmds["[1, 0, 0]"] = [2,0,0]

  # Store the kets for the dict, to prevent many function calls.
  antiCmdKeys = antiCmds.keys()

  # A variable to contain the character typed
  key = 0

  # Stop the Robotic arm
  currentCmd = [0,0,0]
  roboArm.ctrl_transfer(0x40,6,0x100,0,currentCmd,1000) 

  # Loop until someone types Esc (escape)
  while key != 27:
    key = stdscr.getch()
    if key not in cmdKeys:
      continue
    
    cmd = cmds[key]
    cmdStr = str(cmd)

    # If the bit is already set, then do nothing
    if commandSet(currentCmd, cmd) and cmdStr != "[0, 0, 0]":
      #stdscr.addstr(22,0,"Set    ")
      continue

    #stdscr.addstr(22,0,"Not set")

    # Get the anti-command to this command
    if cmdStr in antiCmdKeys:
      antiCmd = antiCmds[cmdStr]
      #stdscr.addstr(21,0,str(antiCmd) + " anti command")

      # Check if the anti-command is set
      if commandSet(currentCmd,antiCmd):
        # Turn the bit off
        for i in xrange(3):
          currentCmd[i] = currentCmd[i] ^ antiCmd[i]

    #stdscr.addstr(20,0,cmdStr + " command")
    if cmdStr == "[0, 0, 0]":
      for i in xrange(3):
        currentCmd[i] = 0
    else:
      # Turn the bit on
      for i in xrange(3):
        currentCmd[i] = currentCmd[i] ^ cmd[i]

    #stdscr.addstr(19,0,str(currentCmd) + " currentCmd")
    #stdscr.refresh()
    roboArm.ctrl_transfer(0x40,6,0x100,0,currentCmd,1000)  
    
  # Stop the robotic arm   
  roboArm.ctrl_transfer(0x40,6,0x100,0,[0,0,0],1000)

  # End the curses window and return the terminal to the user
  curses.endwin()

# Call the main function if this file is executed
if __name__ == '__main__':
  main()
