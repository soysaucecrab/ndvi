import serial
import time

# Set up the serial port
ser = serial.Serial('/dev/ttyACM0', 115200)  # Change '/dev/ttyACM0' to the appropriate serial port

status_value = [1, 2, 3, 4, 5, 6, 7, 8]
status_len = 0

def calculate_status_len(status_values):
    result = 0
    for value in status_values:
        if value < 10:
            result += 1
        elif value < 100:
            result += 2
        elif value < 1000:
            result += 3
        elif value < 10000:
            result += 4
        result += 1  # for ','
    return result

while True:
    # Calculate sensor value string length
    status_len = calculate_status_len(status_value)

    # Send Message to main cansat
    ser.write(bytes([0x76, 0x00, 0xA1, status_len]))
    for value in status_value:
        ser.write(str(value).encode())
        ser.write(b',')

    ser.write(b'\n')
    time.sleep(1)

# Note: This is a basic conversion of the Arduino code to Python for Raspberry Pi.
#       You may need to adjust the serial port and other configurations to match your specific setup.
