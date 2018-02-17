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
the main python script when pressed.  when pressed again it will call 
a third script to clear the LEDs then return to the wait state.


