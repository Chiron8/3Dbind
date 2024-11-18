# CALIBRATION PROGRAM FOR 3Dbind
# Import packages for the MC
import time # Allows MC to introduce pauses
import board # Allows the MC to communicate with the computer
import adafruit_mmc56x3 # Allows MC to communicate with magetometer
import neopixel # Allows MC to use onboard LED

pixel = neopixel.NeoPixel(board.NEOPIXEL, 1) # Shortcut code to refer to LED
pixel.fill((255, 0, 0)) # Sets LED colour to red

i2c = board.STEMMA_I2C()  # Shortcut code to refer to how magnetometer is connected to MC
sensor = adafruit_mmc56x3.MMC5603(i2c) # shortcut code to refer to magnetometer

# Creates 3 average axis variables
X = 0
Y = 0
Z = 0

avrgList = [] # Creates 'list of average readings'

# Adds magnetometer readings to 'list of average readings'
for i in range(1, 4):
    pixel.fill((0, 255, 0))
    mag_x, mag_y, mag_z = sensor.magnetic
    avrgList.append(mag_x)
    avrgList.append(mag_y)
    avrgList.append(mag_z)
    time.sleep(0.5)

# Takes data from 'list of average readings' and creates an average for each axis
# This is how the program reads zero when the magnet/handle is stationary
X = (avrgList[0] + avrgList[3] + avrgList[6]) / 3
Y = (avrgList[1] + avrgList[4] + avrgList[7]) / 3
Z = (avrgList[2] + avrgList[5] + avrgList[8]) / 3

while True:
    # Computer console displays each axis strength minus it's respective average value
    # This is so Mu Editor plotter can display output from magnetometer
    mag_x, mag_y, mag_z = sensor.magnetic
    print("(1, " + str(mag_x - X) + ", " + str(mag_y - Y) + ", " + str(mag_z - Z) + ")")
    time.sleep(0.01) # Short pause of 0.01s set between each set of 3 axis readings to avoid Mu Editor data overload
