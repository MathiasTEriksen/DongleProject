'''
this file contains the python script 'button.py', which listens for physical
button press, and then programs the microcontroller using pdi interface.
It also makes a RGB LED blink during programming, and then turn green for 5
seconds after successfull programming. This program contains an infinite loop
so more than one PSU board can be programmed at a time.
systemd service name = button.service
'''

# gpiozero library is used to conrol gpio pins
import gpiozero                                    
import os                                                                        
import os.path                                
from time import sleep                        
from gpiozero import Button
# uses RGBLED for LED control
from gpiozero import RGBLED                    

# function used to write hex files to memory
def write():
    # run -w command clk is GPIO pin 26, data is GPIO pin 21
    # writes file in Hexfile.hex
    # checks if CRC is correct with -x
    # returns 0 if correct, !=0 if incorrect
    return os.system('sudo ./rpipdi -c 26 -d 21 -E -w Hexfile.hex -x')

# move to working direcory
os.chdir('/home/pi/DongleProject/rpipdi')

# button is set to be controlled by GPIO 2
button = Button(6)
# LED is controlled using GPIO 17, 18 (B not used)
led = RGBLED(4, 17, 23)                                
# wile true used to make infinite loop                                               
while True:
    print ('Push the button to program')
    button.wait_for_press()                       
    print('Beginning...')
    # pulse between green/red while programming
    led.pulse(fade_in_time=0.3,fade_out_time=0.5, 
        on_color=(1,0,0),off_color=(0,1,0)) 
    # while return value from write function is not zero, keep attempting function                                          
    while write() != 0:
        # once return value is 0, the file in memory and write files are identical
        pass                                      
    # shine green for 5 sec                                         
    led.color = (1, 0, 0)    
    sleep(5)                                     
    led.off()
    # ready to program again when LED is off
