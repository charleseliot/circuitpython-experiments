# circuitpython-experiments
Code to play with devices using CircuitPython.

## Working with CircuitPython

Devices like the NeoTrellis M4 with the SAMD51 chip support easy modification to the bootloader by dragging new boot executables into a shared boot drive. The boot executables are packaged according to the UF2 format. To program these devices you write code, compile it, format the output into a UF2 package, copy the package to the shared boot drive, then reboot the device. Microsoft MakeCode does a great job linking these steps into a simple workflow.

Getting into the boot drive can be a bit tricky, because it involves double-clicking the board's reset button with just the right interval (about half a second) between clicks. If the board is connected to your computer with a USB data cable, a new disk volume will show up with a name like CPLAYBOOT or TRELM4BOOT. This is where you drop your new UF2 package to change the bootloader behavior. On the NeoTrellis M4 device this is an 8MB SPI Flash drive, and the drive is fully accessible to running code for media files, graphics files, logs, etc.

_Pro tip: you must use a full data USB cable, not a charging-only cable. Since the two cable types are annoyingly indistinguishable - except that one works and the other mysteriously does not - once you know you have a data cable, mark it somehow. I have blue painter's tape on mine._

Go here for more details: https://learn.adafruit.com/adafruit-neotrellis-m4/uf2-bootloader-details. 

CircuitPython makes this already straightforward coding process even easier. First you need to load the CircuitPython on to your device. You do this by loading a new UF2 bootloader for the version of CircuitPython appropriate to your device. (For example, here is the link to the CircuitPython bootloaders for the NeoTrellis M4: https://circuitpython.org/board/trellis_m4_express/. You'll find scores of others on GitHub. Here are the v5 beta 2 versions: https://github.com/adafruit/circuitpython/releases/tag/5.0.0-beta.2) When the device reboots it will mount the CircuitPython environment, and publish a new shared disk volume called CIRCUITPY.

To run Python code on your device, you just drop a Python source file into the CIRCUITPY volume (with an appropriate filename: either _code.py_, _code.txt_, _main.py_, or _main.txt_, but _code.py_ is usual). CircuitPython devices are usually configured to auto-reboot when code changes, so your new Python code should run immediately. If not, just press the reset button once.

CircuitPython does most of the things you expect from a Python environment (see https://learn.adafruit.com/circuitpython-essentials/circuitpython-built-ins for details), but you'll need to add library code to support the devices you're using. For this you need to know about the CircuitPython Library Bundles at https://circuitpython.org/libraries.

The library bundles contain masses of code (in compressed .MPY format) with support for specific bits of hardware. You just move the pieces you need into the ./lib folder of the CIRCUITPY volume.

For example, the NeoTrellis M4 Express example includes the following lines:

import adafruit_trellism4
import adafruit_ds3231

These imports refer to the _adafruit_trellisM4.mpy_
and _adafruit_ds3231.mpy_ files from the CircuitPython Library Bundle.

Note 1: Watch out for version mismatches! Use library files from the CircuitPython Library Bundle for your CircuitPython environment - v4 for v4, v5 for v5.

Note 2: If you're using devices from AdaFruit, the documentation on how to use CircuitPython with the device should tell you exactly which library files you'll need to copy to the CIRCUITPY/lib directory. For example, the documentation page for the DS3231 RTC chip (https://learn.adafruit.com/adafruit-ds3231-precision-rtc-breakout/circuitpython) lists the three libraries you'll need: _adafruit_ds3231.mpy_, _adafruit_bus_device_, and _adafruit_register_. (The latter two are actually directories, not individual files.)

### CircuitPython References

Go here if you just want to get started with CircuitPython on a compatible device: https://learn.adafruit.com/welcome-to-circuitpython

Then here to master the basics of CircuitPython: 
https://learn.adafruit.com/circuitpython-essentials

And finally here to dig into the details: https://circuitpython.readthedocs.io/en/latest/docs/


## Adafruit NeoTrellis M4 Express

Source directory: ./trellis-m4

The NeoTrellis M4 Express is a device from Adafruit that provides an 8 x 4 lights + buttons surface, with audio and other goodies. The lights are set up as a grid of 32 NeoPixels, each associated with an Elastomer button.

The on-board SAMD51 chip can be programmed like an Arduino, but support for CircuitPython makes programming even easier. (https://learn.adafruit.com/adafruit-neotrellis-m4/what-is-circuitpython)

For information about the NeoTrellis M4 Express board, go here: https://learn.adafruit.com/adafruit-neotrellis-m4/board-tour

In this example I've also attached a DS3231 real-time clock to the Trellis unit, connected over an I2C interface. The RTC comes on a small board available from Adafruit (https://learn.adafruit.com/adafruit-ds3231-precision-rtc-breakout/overview), which not only carries the chip, but also (1) appropriate pull-up resistors on the I2C lines, and (2) a battery so the chip will remember the time you set even when it's not powered from the Trellis board.

The board is connected to the Trellis through the 4-pin JST "hacking port" on the Trellis. The pins carry ground and 3.3V lines, plus the SDA and SCL (data and clock) lines needed for I2C.

The example code presents a BCD (binary coded decimal) clock based on the time read from the DS3231 chip. The time is displayed as HH:MM:SS, with each digit displayed in binary format by a column of NeoPixel lights.
