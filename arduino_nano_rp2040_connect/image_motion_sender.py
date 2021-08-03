# Import libraries
import time
import busio
import microcontroller
from digitalio import DigitalInOut
import ulab.numpy as np

# Internet
import adafruit_requests as requests
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
from adafruit_esp32spi import adafruit_esp32spi

# Camera
from Arducam import *
from board import *
import io
from snapshot import *

# Request address. Make sure to replace with appropriate address
ip_image_receiver = "http://192.168.1.107:8090/image_receiver"
ip_test = "http://192.168.1.107:8090/test"

# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

# Set up Internet (modified pin names for Arduino Nano RP2040 Connect)
# If you are using a board with pre-defined ESP32 Pins:
esp32_cs = DigitalInOut(board.CS1)
esp32_ready = DigitalInOut(board.ESP_BUSY)
esp32_reset = DigitalInOut(board.ESP_RESET)
spi = busio.SPI(board.SCK1, board.MOSI1, board.MISO1)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

requests.set_socket(socket, esp)

while not esp.is_connected:
    try:
        esp.connect_AP(secrets["ssid"], secrets["password"])
    except RuntimeError as e:
        print("could not connect to AP, retrying: ", e)
        continue
    
print("Connected to", str(esp.ssid, "utf-8"), "\tRSSI:", esp.rssi)
print("My IP address is", esp.pretty_ip(esp.ip_address))

answer = requests.get(ip_test)
print(answer.text)

# Set up the camera
try:
    mycam = camera_setup()
except RuntimeError as e:
    print("Could not setup the camera", e)

# Set up HC-SR501 motion detector
PIR_PIN = board.D9   # Pin number connected to PIR sensor output wire.
# Setup digital input for PIR sensor:
pir = digitalio.DigitalInOut(PIR_PIN)
pir.direction = digitalio.Direction.INPUT

# wait for the motion sensor to start
#print("Waiting 10 Seconds to get the sensor running")!
tst = pir.value
#time.sleep(10)

while True:
    pir_value = pir.value
    
    # if a motion is detected, send the image 
    if pir_value:
        print("Motion Detected! Sending the image!")
        # Wait 1 second to let the person fully walk into the room
        # otherwise, the image will be taken as soon as the motion sensor
        # detects movement, which might not be desirable
        time.sleep(1)
        image = capture(mycam)
        answer = requests.post(ip_image_receiver, data=image)
        print(answer.text)
        
        # An optional pause before continuing 
        print("Waiting 4 Seconds before continuing...")
        time.sleep(4)
