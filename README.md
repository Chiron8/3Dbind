# 3Dbind
## 3Dbind is a device that can easily control views in 3D CAD (origninally for Autodesk Fusion)
Written in CircuitPython
The code is written for an Adafruit QtPy RP2040 with an MMC56x3 magnetometer

Keybindings in code are for Autodesk Fusion, make sure to change them for your preferred CAD!

3D models are availiable here: https://www.thingiverse.com/thing:6834057

## Instructions
### Getting started
Choose which file you want to use. `calibration.py` just calibrates the magnetometer and if using `Mu editor` will plot a graph. `main.py` can control 3D CAD software.
You will need to add the file to the MC's drive and rename it to `code.py`

drag the `lib` folder into the MC's drive. This contains all the necessary packages. *MAKE SURE THERE IS ONLY ONE `lib` FOLDER*

### Using the device
Panning: Push forwards to pan forwards, push left to pan left, etc...

Orbiting: Same as panning but hold the `SHIFT` key

Zooming in/out: To zoom in, press the handle down. To zoom out, hold the handle down

I hope you enjoy it!

## The device is pretty much plug and play!

## Pictures
[![alt text](https://github.com/Chiron8/3Dbind/blob/main/IMG_7437.jpg)
