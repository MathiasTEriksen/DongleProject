## PSU Programmer Project

PSU programming stick which can be used to program PSU boards on PCB boardstacks.

### Interface

The PSU boards on the PCB boardstacks rev6 and earlier use a PDI interface to program the microcontroller. This programming stick uses a raspberry pi zero in order to interface with the PDI interface, and write hexfiles into the memory of the microcontroller. The microcontroller on the PSU boards is an ATxMEGA 16e5, and the pinout is as follows:

<img
src="images/Prog_Input(OLD).png"
style="width:400px;"
/>

In order to comminicate with the microcontroller from the pi, we use the GPIO pins. For this purpose, the pin named PDI is going to be used for DATA and the pin named RESET is going to be used as CLOCK. In this case, we use the 3v3 output from the pi and one of the ground pins on the pi in order to power the board. More importantly, GPIO pin 26 is used as for the CLOCK, and GPIO pin 21 is used for DATA. using these commections, we can use the PDI interface to program the microcontroller. In order to interface with the microcontroller, a seperate github project was used as the source code. For reference, the flash page size for this microcontroller is 128 words and the flash base address is 0x008000000.

Source code for PDI interface: https://github.com/buildbotics/rpipdi

Some changes were made to this source code in order to debug and make it work for the application. Notable changes were ignoring some errors and upping retry rate

Updated source code: https://github.com/MSNetrom/rpipdi

Using this source code, all you have to do is enter the rpipdi folder and use the sudo ./rpipdi command to excecute write and erase commands. When using this command, always -c and -d values must be entered. These are the values for which GPIO pins correspond clock and data, in our case -c is 26 and -d 21.

