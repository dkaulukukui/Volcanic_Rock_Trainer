#This project is to build climbing trainer board for Volcanic Rock Gym

This project will be completed using the following:

Hardware: 
- Raspi Zero-W
- WS2811 RGB led lighting string
- Custom interface board
- 6 x Arcade buttons (N.O.)

Software libraries:
- Adafruit NeoPixel libraries

The end product will be a climbing training board with various routines
tied to buttons.  
Press button 1, initiate routine 1, button 2 = routine 2 etc.

There will be one button which acts as a start/stop/reset button.  

This button will be running as a daemon upon start up and then call
the main python script when pressed. 

There are configuration files associated with this script:

Each climbing pattern has its own configuration file with the following format:

ROW(0-8) LED#(0-2) RED(0-255) GREEN(0-255) BLUE(0-255)

The main file reads in this file into a list of lists 
which is then iterated through turning on each LED specified to the specified color.

Multiple LEDS in each row can be lit
