# Arduino Nano RP2040 Connect w/ OV2640 & Temperature/Motion sensors

Nano RP2040 tracks temperature/motion and upon conditional sends an image to RPi 4. This folder describes everything relevant you need to know. 

## Table of Contents

   * [Human Binary Classification Suite](#human-binary-classification-suite)
      * [Dependencies](#dependencies)
      * [Hardware Wiring](#harware-wiring)

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

## File Descriptions

[1]: https://circuitpython.org/libraries
[2]: https://www.arducam.com/docs/pico/arducam-camera-module-for-raspberry-pi-pico/spi-camera-for-raspberry-pi-pico/
[3]: https://github.com/ArduCAM/PICO_SPI_CAM/tree/master/Python
[4]: https://circuitpython.org/board/arduino_nano_rp2040_connect/
