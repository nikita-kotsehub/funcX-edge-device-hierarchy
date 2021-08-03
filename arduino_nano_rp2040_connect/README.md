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
| ------------- |:-------------:|
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
| ------------- |:-------------:|
| VCC           | 5V |
| DOUT            | D9 (or any other GPIO port, except A6, A7)   |
| GND            | GND |

<img src="https://diyusthad.com/wp-content/uploads/2020/10/PIR-Motion-Sensor-Pinout-LQ.jpg" alt="HC-SR501 Pinout" width=300/>

*Notes:*

1. By default, Nano RP2040 will not output the 5V to power the motion sensor [[5]]. To get it to work, you need to solder the solder pads [[6]].
2. The motion sensor might take up to 60 seconds to start, during which it will switch from True to False multiple times. If it still does not work, try turning the left knob all the way counterclockwise, and the right one clockwise.

## Functions

### Main Driver

### Camera Functions

[1]: https://circuitpython.org/libraries
[2]: https://www.arducam.com/docs/pico/arducam-camera-module-for-raspberry-pi-pico/spi-camera-for-raspberry-pi-pico/
[3]: https://github.com/ArduCAM/PICO_SPI_CAM/tree/master/Python
[4]: https://circuitpython.org/board/arduino_nano_rp2040_connect/
[5]: https://forum.arduino.cc/t/5v-pin-on-nano-rp2040-connect-not-working/866247
[6]: https://support.arduino.cc/hc/en-us/articles/360014779679-Why-doesn-t-the-5V-pin-work-in-the-Arduino-Nano-33-BLE-boards-
