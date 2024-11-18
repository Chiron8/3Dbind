# MAIN PROGRAM FOR 3Dbind
# Import packages for the MC
import time # Allows MC to introduce pauses
import board # Allows the MC to communicate with the computer
import adafruit_mmc56x3 # Allows MC to communicate with magetometer
import neopixel # Allows MC to use onboard LED
import usb_hid # These 4 packages allows MC to simulate keyboard and mouse
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse

pixel = neopixel.NeoPixel(board.NEOPIXEL, 1) # Shortcut code to refer to LED
pixel.fill((255, 0, 0)) # Sets LED colour to red

kbd = Keyboard(usb_hid.devices) # Shortcut code to refer to keyboard
m = Mouse(usb_hid.devices) # Shortcut code to refer to mouse
i2c = board.STEMMA_I2C()  # Shortcut code to refer to how magnetometer is connected to MC
sensor = adafruit_mmc56x3.MMC5603(i2c) # Shortcut code to refer to magnetometer

threshold = 100 # How far the handle needs to move before MC starts keybind action

# Creates 3 average axis variables
X = 0
Y = 0
Z = 0

avrgList = [] # Creates 'list of average readings'

# Adds magnetometer readings to 'list of average readings'
for i in range(1, 4):
    pixel.fill((0, 0, 255))
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

pixel.fill((255, 40, 80)) # Sets LED colour to pink

while True:
    # PROGRAM MAIN SECTION
    # This controls all features of 3Dbind
    mag_x, mag_y, mag_z = sensor.magnetic # Takes magnetometer readings
    
    if mag_y - Y < -threshold * 2 and mag_z - Z < -threshold * 2: # Has user pushed down on handle? (zoom feature)
        time.sleep(1) 
        mag_x, mag_y, mag_z = sensor.magnetic
        if mag_y - Y < -threshold * 2 and mag_z - Z < -threshold * 2: # Is user still pushing down after one second? (zoom out)
            m.click(Mouse.MIDDLE_BUTTON) # Keybind 'double click middle button' on mouse to zoom out
            time.sleep(0.1)
            m.click(Mouse.MIDDLE_BUTTON)
        else: # User wasn't pushing down handle after one second
            for i in range(7): # Keybind 'scroll down' mouse wheel to zoom in
                m.move(0, 0, -1)
                time.sleep(0.05)

    # BELOW IS A GENERAL EXPLAINATION ON HOW THE PROGRAM MANAGES KEYBINDS IN RELATION TO THE HANDLE MOVEMENT:
    # if mag_s - S < -threshold...:            CHECKS IF HANDLE HAS BEEN MOVED
    #   time.sleep(0.5)                            WAITS 0.5 SECONDS
    #   if mag_s - S < -threshold:             CHECKS IF HANDLE IS STILL IN THE POSITION IT WAS MOVED TO 
    #                                          (THIS IS TO CHECK THE DEVICE HASN'T BEEN PRESSED or KNOCKED BY ACCIDENT)
    #        m.press(Mouse.MIDDLE_BUTTON)      KEYBIND 'HOLD MIDDLE BUTTON' OF MOUSE
    #        for i in range(41):               KEYMIND MOVES ON-SCREEN CURSOR
    #            m.move(-4, 0, 0)
    #        m.release(Mouse.MIDDLE_BUTTON)    KEYBIND RELEASES 'MIDDLE BUTTON' OF MOUSE
    #        time.sleep(1)                     PAUSES FOR 1 SECOND TO STOP CONTINOUS KEYBIND ACTION
    
    elif mag_x - X > threshold/2 and mag_z - Z < -(threshold/2) and mag_y - Y < 0: # Push handle left
        time.sleep(0.5)
        mag_x, mag_y, mag_z = sensor.magnetic
        if mag_x - X > threshold/2 and mag_z - Z < -(threshold/2) and mag_y - Y < 0:
            m.press(Mouse.MIDDLE_BUTTON)
            for i in range(41):
                m.move(-4, 0, 0)
            m.release(Mouse.MIDDLE_BUTTON)
            kbd.release(Keycode.LEFT_SHIFT)
            time.sleep(1)
            
    elif mag_z - Z < -(threshold/2) and mag_y - Y < -(threshold/2) and mag_x - X > -(threshold/2): # Push handle right
        time.sleep(0.5)
        mag_x, mag_y, mag_z = sensor.magnetic
        if mag_z - Z < -(threshold/2) and mag_y - Y< -(threshold/2) and mag_x - X > -(threshold/2):
            m.press(Mouse.MIDDLE_BUTTON)
            for i in range(41):
                m.move(4, 0, 0)
            m.release(Mouse.MIDDLE_BUTTON)
            kbd.release(Keycode.LEFT_SHIFT)#
            time.sleep(1)
        
    elif mag_y - Y < -(threshold/2) and mag_x - X < -(threshold/2): # Pull handle backwards
        time.sleep(0.5)
        mag_x, mag_y, mag_z = sensor.magnetic
        if mag_y - Y < -(threshold/2) and mag_x - X < -(threshold/2):
            m.press(Mouse.MIDDLE_BUTTON)
            for i in range(41):
                m.move(0, 4, 0)
            m.release(Mouse.MIDDLE_BUTTON)
            kbd.release(Keycode.LEFT_SHIFT)
            time.sleep(1)
    

        
    elif mag_y - Y > threshold and mag_z - Z < -threshold: # Push handle forwards
        time.sleep(0.5)
        mag_x, mag_y, mag_z = sensor.magnetic
        if mag_y - Y > threshold and mag_z - Z < -threshold:
            m.press(Mouse.MIDDLE_BUTTON)
            for i in range(41):
                m.move(0, -4, 0)
            m.release(Mouse.MIDDLE_BUTTON)
            kbd.release(Keycode.LEFT_SHIFT)
            time.sleep(1)
        
        
    
    if mag_x > 1000 or mag_x < -1000:
        pixel.fill((255, 0, 0)) # sets LED colour to red
        time.sleep(3)
        avrgList = [] #sets list to record averages


        # creates a list of current magnetic strengths
        for i in range(1, 4):
            pixel.fill((0, 0, 255))
            mag_x, mag_y, mag_z = sensor.magnetic
            avrgList.append(mag_x)
            avrgList.append(mag_y)
            avrgList.append(mag_z)
            time.sleep(0.5)

        # makes an average of each axis strength so we can cancel it out later in the program
        X = (avrgList[0] + avrgList[3] + avrgList[6]) / 3
        Y = (avrgList[1] + avrgList[4] + avrgList[7]) / 3
        Z = (avrgList[2] + avrgList[5] + avrgList[8]) / 3
    time.sleep(0.5)
    i=0
        
    print("(1,", mag_x - X, ",", mag_y - Y, ",", mag_z - Z, ")")
