import time
import busio
from Arducam import *
from board import *
import io

def read_fifo_burst(mycam):
    '''
    Reads data from a temporary buffer into the image_buffer
    
    Input
    -----
    mycam: ArducamClass object
        an object of class ArducamClass, created by camera_setup()
        
    Output
    ------
    image_buffer: bytearray
        returns a bytearray containing a JPEG image

    '''
    once_number=128
    count=0
    length=mycam.read_fifo_length()
    buffer=bytearray(once_number)
    image_buffer = bytearray(0)

    mycam.SPI_CS_LOW()
    mycam.set_fifo_burst()

    while True:
        mycam.spi.readinto(buffer,start=0,end=once_number)
        image_buffer = image_buffer + buffer
        time.sleep(0.00015)
        count+=once_number
        
        if count+once_number>length:
            count=length-count
            mycam.spi.readinto(buffer,start=0,end=count)
            mycam.SPI_CS_HIGH()
            mycam.clear_fifo_flag()
            
            return image_buffer

def camera_setup(camera_version=OV2640, image_size=OV2640_320x240):
    '''
    Initiates the camera with the given model (OV2640/OV5642)
    and image_size. Prints out camera tests. Returns a camera
    object that will be used to take pictures
    
    Input
    -----
    camera_version: int variable
        OV2640 and OV5642 are predefined variables from
        Arducam.py
        
    image_size: int variable
        camera sizes are predefined in Arducam.py & OV2640_reg.py
        
    Output
    ------
    mycam: ArducamClass object
        returns an object of class ArducamClass,
        defined in Arducam.py
        
    Notes
    -----
    Tested only for OV5642. 
    '''
    mycam = ArducamClass(camera_version)
    mycam.Camera_Detection()
    mycam.Spi_Test()
    mycam.Camera_Init()
    mycam.clear_fifo_flag()

    # Current Arducam's code base for OV2640 supports only JPEG
    mycam.set_format(JPEG)
    mycam.OV2640_set_JPEG_size(image_size)
    
    # Uncomment for Black & White images
    # Explore other modes in Arducam.py
    #mycam.OV2640_set_Special_effects(BW)

    mycam.set_bit(ARDUCHIP_TIM,VSYNC_LEVEL_MASK)
    
    return mycam

def capture(mycam):
    '''
    Main driver function.
    
    Input
    -----
    mycam: ArducamClass object
    
    Output
    -----
    image_buffer: bytearray
        returns a bytearray containing a JPEG image
    '''
    mycam.flush_fifo();
    mycam.clear_fifo_flag();
    mycam.start_capture();
    while True:
        if mycam.get_bit(ARDUCHIP_TRIG,CAP_DONE_MASK)!=0:
            image_buffer = read_fifo_burst(mycam)  
            mode=0
            break
    
    return image_buffer