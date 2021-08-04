# Arduino Nano RP2040 Connect w/ OV2640 & Temperature/Motion sensors

Nano RP2040 tracks temperature/motion and upon the conditional sends an image to RPi 4. This folder describes everything relevant you need to know. 

## Table of Contents

   * [Arduino Nano RP2040 Connect w/ OV2640 & Temperature/Motion sensors](#human-binary-classification-suite)
      * [Dependencies](#dependencies)
      * [Hardware Wiring](#hardware-wiring)
      * [Functions](#functions)

## Dependencies

### Language
* CircuitPython 7.0.0 alpha-5 

[download link][4]
### Libraries
* adafruit_bus_device
* adafruit_esp32spi
* adafruit_requests.mpy

The necessary libraries are in the `lib` folder, although you might want to download the latest library bundle from [here][1].

### Hardware
* Arduino Nano RP2040 Connect with soldered pins
* OV2640 SPI camera module
* Jump wires
* Optional: HC-SR501 infrared motion sensor
* Optional: breadboard

## Hardware Wiring

### OV2640 SPI to Nano RP2040

The original guide for connecting OV2640 to Raspberry Pi Pico from Arducam can be found [here][2]. The original codebase is [here][3]. I modified the codebase and adapted the pinout for Arduino Nano RP2040 Connect. 

Use the following wiring: 

| OV2640 SPI    |  Arduino Nano RP2040 Connect|
| ------------- |:-------------|
| CS            | D10 (or any other GPIO port, except A6, A7) |
| MOSI          | D11 (COPI/MOSI)     |
| MISO          | D12 (CIPO/MISO)     |
| SCK           | D13 (SCK) |
| GND           | GND      |
| VCC           | 3.3V     |
| SDA           | A4 (SDA) |
| SCL           | A5 (SCL)     |

### HC-SR501 Motion Sensor

If using the motion sensor, you can use the following wiring:

| HC-SR501    |  Arduino Nano RP2040 Connect|
| ------------- |:-------------|
| VCC           | 5V |
| DOUT            | D9 (or any other GPIO port, except A6, A7)   |
| GND            | GND |

<img src="https://diyusthad.com/wp-content/uploads/2020/10/PIR-Motion-Sensor-Pinout-LQ.jpg" alt="HC-SR501 Pinout" width=300/>

*Notes:*

1. By default, Nano RP2040 will not output the 5V to power the motion sensor [[5]]. To get it to work, you need to solder the solder pads [[6]].
2. The motion sensor might take up to 60 seconds to start, during which it will switch from True to False multiple times. If it still does not work, try turning the left knob all the way counterclockwise, and the right one clockwise.

## Functions

### Main Driver

- `image_temperature_sender.py` is the main function. It connects to a user-provided Wi-Fi access point (see `secrets.py`), loads the weights and biases, sets up the camera, and then continuously predicts the next temperature from the two previous measurements. If it exceeds a threshold, Nano RP2040 takes a picture and sends it as a byte array to a server hosted on a local network with the Raspberry Pi 4. 
- `image_motion_sender.py` is similar to `image_temperature_sender.py`, only it triggers the camera when it detects any motion in the area. You can easily replace the conditional and the data you're sending to the server for your own use cases.
- `secrets.py` should contain a dictionary with your network's `ssid` and `password`. Note that Nano RP2040 might not connect to a network with a network band above 2.4GHz. 
- `w1_temp.txt` & `b1_temp.txt` are the weights and biases for the temperature prediction neural network.

### Camera Functions

- `OV2640_reg.py` enables the OV2640 to take JPEG images of different sizes. 
- `OV5642_reg.py` enables the OV5642 to take JPEG & RAW images of different sizes. Note: the project has not been tested for OV5642.
- `Arducam.py` includes main functions for setting up the camera and taking the pictures. All of the functions here were developed by Arducam. I modified the `__init__` part of the ArducamClass to make it work with Arduino Nano RP2040 Connect. If you have a different microcontroller, you will likely need to change the pinout as well.
- `snapshot.py` calls essential functions from `Arducam.py` to set up the camera and take an image. It abstracts users from the abundance of code in 'Arducam.py'.

[1]: https://circuitpython.org/libraries
[2]: https://www.arducam.com/docs/pico/arducam-camera-module-for-raspberry-pi-pico/spi-camera-for-raspberry-pi-pico/
[3]: https://github.com/ArduCAM/PICO_SPI_CAM/tree/master/Python
[4]: https://circuitpython.org/board/arduino_nano_rp2040_connect/
[5]: https://forum.arduino.cc/t/5v-pin-on-nano-rp2040-connect-not-working/866247
[6]: https://support.arduino.cc/hc/en-us/articles/360014779679-Why-doesn-t-the-5V-pin-work-in-the-Arduino-Nano-33-BLE-boards-
