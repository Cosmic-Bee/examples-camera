import time as utime
import busio
import board
from Arducam import *
from board import *

once_number = 128
mode = 0
start_capture = 0
buffer = bytearray(once_number)

mycam = ArducamClass(OV2640)
mycam.OV2640_set_JPEG_size(OV2640_800x600_JPEG)
mycam.Camera_Detection()
mycam.Spi_Test()
mycam.Camera_Init()
utime.sleep(1)
mycam.clear_fifo_flag()

def read_fifo_burst():
    count = 0
    length = mycam.read_fifo_length()
    mycam.SPI_CS_LOW()
    mycam.set_fifo_burst()
    with open("output.jpg", "wb") as f:  # Open file in binary write mode
        while True:
            mycam.spi.readinto(buffer, start=0, end=once_number)
            f.write(buffer)  # Write buffer to file
            utime.sleep(0.00015)
            count += once_number
            if count + once_number > length:
                count = length - count
                mycam.spi.readinto(buffer, start=0, end=count)
                f.write(buffer)  # Write remaining buffer to file
                mycam.SPI_CS_HIGH()
                mycam.clear_fifo_flag()
                break

# Capture a single photo
mycam.flush_fifo()
mycam.clear_fifo_flag()
mycam.start_capture()

while mycam.get_bit(ARDUCHIP_TRIG, CAP_DONE_MASK) == 0:
    utime.sleep(0.001)  # Wait for capture to complete

read_fifo_burst()  # Read the captured image and save it to disk
