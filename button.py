#########################################################################################
                                              #
import gpiozero                               # import gpiozero for button     
import os                                     # import os so we can use terminal commands
import wget                                   # import wget so we can download files 
from time import sleep                        # import sleep for LED functionality
from gpiozero import Button                   # import Button for Button functionality
from gpiozero import LED                      # import LED class for LED functionality
from gpiozero import RGBLED                   # import RGBLED for multicolor LED 
                                              # functionality
#########################################################################################
'''                                           #
url = 'where file is'                         # first, download most recent version of  
wget.download(url, '/home/pi/rpipdi/WriteFile.hex)      
'''                                           # hex file and place in rpipdi folder
                                              #
button = Button(2)                            # button is set to GPIO #2
led = RGBLED(17, 18, 23)                      # multicolor LED is set to use GPIOs
                                              # 17, 18, 23 on pi
print ('Push the button to program')          # print instruction(not necessary for final
                                              # draft
button.wait_for_press()                       # wait for button to be pressed
print('Beginning...')                         # print that programming is starting
os.chdir('rpipdi')                            # move to the rpipdi directory
led.pulse(fade_in_time=0.3,fade_out_time=0.5,on_color=(1,0,0),off_color=(0,1,0))
                                              # Led pulses red/green while programming
def write():                                  # define write function
    return os.system('sudo ./rpipdi -c 26 -d 21 -E -w winghead-psu-testblink.hex -x')
while write() != 0:                           # while the return value from the os.system
    pass                                      # is not 0 (CRC values do not match),
                                              # continue attemptinf to write the hex file
led.blink(on_time=1,off_time=0,on_color=(1,0,0))
sleep(10)                                     # once CRC value is correct, shine green on
                                              # LED for 10 seconds
                                              #
#########################################################################################