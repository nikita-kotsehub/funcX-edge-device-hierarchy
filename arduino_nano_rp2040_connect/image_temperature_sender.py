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

# Import weights
with open('w1_temp.txt', 'r') as f:
    # the weights import is specific to the (2, 1) dimension from the DNN model
    # if you change the model, you would need to modify this section to your
    # weights dimensions
    a1 = [float(f.readline())]
    a2 = [float(f.readline())]
    w1 = np.array([a1, a2])
    
# Import the bias 
with open('b1_temp.txt', 'r') as f:
    a1 = [float(f.readline())]
    b1 = np.array(a1)

# Temperature prediction function
def predict_next_temp(previous_temps, w1=w1, b1=b1):
    '''
    Predicts the next temperature using the previous two.
    The function is specific to our simplistic neural network with just
    a single neuron in a Dense layer.
    
    Input
    -----
    previous_temps: ulab.numpy ndarray
        shape: (2,)
    
    w1: ndarray
    b1: ndarray

    Output
    ------
    prediction[0]: float
        prediction is an array with a single element, the predicted next temperature
    '''
    prediction=np.dot(previous_temps, w1) + b1
    return prediction[0]

# define the critical temperature threshold
temperature_threshold = 25

# 2nd previous temperature
previous_2 = microcontroller.cpu.temperature

while True:
    # get the current temperature
    previous_1 = microcontroller.cpu.temperature
    
    # put the two previous temps in a ndarray & predict the next temperature
    time_series = np.array([previous_2, previous_1])
    next_predicted = predict_next_temp(time_series)
    print(f"{[previous_2, previous_1]} --> {next_predicted}")
    
    # if the next temperature is above the defined threshold,
    # take a picture and send it to the server
    if next_predicted > temperature_threshold:
        print("Predicted Extreme Heat! Sending an Image!")
        # the very fist image might be too dark, but the next ones should be okay
        time.sleep(1)
        image = capture(mycam)
        answer = requests.post(ip_image_receiver, data=image)
        print(answer.text)
        
    previous_2 = previous_1
    
    # An optional pause before taking the next temperature
    time.sleep(5)