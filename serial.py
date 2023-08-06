import serial
import time

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

ser = serial.Serial('/dev/ttyACM0', 115200)  # Change '/dev/ttyACM0' to the appropriate serial port

StatusValue = [1, 2, 3, 4, 5, 6, 7, 8]
StatusLen = 0

while True:
    # 1. first read the Status value then wait
    for idx in range(8):
        time.sleep(0.001)
    
    # 2. Calculate sensor value string length
    StatusLen = calculate_status_len(StatusValue)
    
    # 3. Send Message to main cansat
    ser.write(bytes([0x76, 0x00, 0xA1, StatusLen]))
    for value in StatusValue:
        ser.write(str(value).encode())
        ser.write(b',')
    
    ser.write(b'\n')
    time.sleep(0.001)

def hyGs_RecvByte(b):
    global sRecvMode
    global cRecvCmd

    # 56 00 .... 
    if sRecvMode == 0x00:
        sRecvMode = 0x01 if b == 0x56 else 0
    elif sRecvMode == 0x01:
        sRecvMode = 0x02 if b == 0x00 else 1 if b == 0x56 else 0
    elif sRecvMode == 0x02:
        sRecvMode = 0x10 if b == 0x48 else 1 if b == 0x56 else 0
    elif sRecvMode == 0x10:
        sRecvMode = sRecvMode + 1 if b == 0x00 else 1 if b == 0x56 else 0
    elif sRecvMode == 0x11:
        sRecvMode = sRecvMode + 1
        cRecvCmd[0] = b
    elif sRecvMode == 0x12:
        sRecvMode = sRecvMode + 1
        cRecvCmd[1] = b
    elif sRecvMode == 0x13:
        sRecvMode = 0
        cRecvCmd[2] = b
        if 64 <= cRecvCmd[0] < 64 + 8:  # when 8 bit data value
            if (cRecvCmd[0] ^ cRecvCmd[1]) == cRecvCmd[2]:  # XOR
                StatusValue[cRecvCmd[0] - 64] = cRecvCmd[1]
    else:
        sRecvMode = 1 if b == 0x56 else 0
