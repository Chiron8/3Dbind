# import packages
import time # controls pauses
import board # required for microcontroller to talk to computer
import adafruit_mmc56x3 # magnetometer package
import neopixel # for in-built LED
import usb_hid # The next 4 packages control keyboard and mouse
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse

pixel = neopixel.NeoPixel(board.NEOPIXEL, 1) # initializes built in LED
pixel.fill((255, 0, 0)) # sets LED colour to red

kbd = Keyboard(usb_hid.devices) # sets mouse
m = Mouse(usb_hid.devices) # sets keyboard
i2c = board.STEMMA_I2C()  # For using the built-in STEMMA connector
sensor = adafruit_mmc56x3.MMC5603(i2c) # tells program what magnetometer is connected

# initalise average variables
X = 0
Y = 0
Z = 0

threshold = 100 # how far you need to push device to control CAD

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


while True:
    pixel.fill((255, 40, 80)) # sets LED colour to green
    mag_x, mag_y, mag_z = sensor.magnetic # get magnetometer readings
    
    # HOW THE CONTROLS WORK:
    # if mag_s - S < -threshold...:            CHECKS IF CONTROL CAN BE ACTIVATED
    #   time.sleep(1)                          WAITS 1 SECOND
    #   if mag_s - S < -threshold:             CHECKS IF CONTROL CAN STILL BE ACTIVATED THE ACTION STARTS 
    #                                          (THIS IS TO CHECK THE DEVICE HASN'T BEEN PRESSED BY ACCIDENT)
    #        m.press(Mouse.MIDDLE_BUTTON)      HOLDS MIDDLE BUTTON
    #        for i in range(41):               MOVES MOUSE SMOOTHLY
    #            m.move(-4, 0, 0)
    #        m.release(Mouse.MIDDLE_BUTTON)    RELEASES MIDDLE BUTTON THE SHIFT KEY
    #        kbd.release(Keycode.LEFT_SHIFT)
    #        time.sleep(1)                     PAUSES FOR 1 SECOND TO NOT ACTIVATE AGAIN
    
    if mag_y - Y < -threshold * 2 and mag_z - Z < -threshold * 2: # press down
        time.sleep(1)
        mag_x, mag_y, mag_z = sensor.magnetic
        if mag_y - Y < -threshold * 2 and mag_z - Z < -threshold * 2:
            m.click(Mouse.MIDDLE_BUTTON)
            time.sleep(0.1)
            m.click(Mouse.MIDDLE_BUTTON)
        else:
            for i in range(7):
                m.move(0, 0, -1)
                time.sleep(0.05)
    
    elif mag_x - X > threshold/2 and mag_z - Z < -(threshold/2) and mag_y - Y < 0: #shift left
        time.sleep(0.5)
        mag_x, mag_y, mag_z = sensor.magnetic
        if mag_x - X > threshold/2 and mag_z - Z < -(threshold/2) and mag_y - Y < 0:
            #kbd.press(Keycode.LEFT_SHIFT)
            m.press(Mouse.MIDDLE_BUTTON)
            for i in range(41):
                m.move(-4, 0, 0)
            m.release(Mouse.MIDDLE_BUTTON)
            kbd.release(Keycode.LEFT_SHIFT)
            time.sleep(1)
            
    elif mag_z - Z < -(threshold/2) and mag_y - Y < -(threshold/2) and mag_x - X > -(threshold/2): #shift right
        time.sleep(0.5)
        mag_x, mag_y, mag_z = sensor.magnetic
        if mag_z - Z < -(threshold/2) and mag_y - Y< -(threshold/2) and mag_x - X > -(threshold/2):
            #kbd.press(Keycode.LEFT_SHIFT)
            m.press(Mouse.MIDDLE_BUTTON)
            for i in range(41):
                m.move(4, 0, 0)
            m.release(Mouse.MIDDLE_BUTTON)
            kbd.release(Keycode.LEFT_SHIFT)#
            time.sleep(1)
        
    elif mag_y - Y < -(threshold/2) and mag_x - X < -(threshold/2): #shift down
        time.sleep(0.5)
        mag_x, mag_y, mag_z = sensor.magnetic
        if mag_y - Y < -(threshold/2) and mag_x - X < -(threshold/2):
            #kbd.press(Keycode.LEFT_SHIFT)
            m.press(Mouse.MIDDLE_BUTTON)
            for i in range(41):
                m.move(0, 4, 0)
            m.release(Mouse.MIDDLE_BUTTON)
            kbd.release(Keycode.LEFT_SHIFT)
            time.sleep(1)
    

        
    elif mag_y - Y > threshold and mag_z - Z < -threshold: #shift up
        time.sleep(0.5)
        mag_x, mag_y, mag_z = sensor.magnetic
        if mag_y - Y > threshold and mag_z - Z < -threshold:
            #kbd.press(Keycode.LEFT_SHIFT)
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
