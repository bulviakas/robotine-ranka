import serial
import time

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
    time.sleep(2)
    ser.reset_input_buffer()
    
    while True:
        ser.write(("FRIDGE").encode('utf-8'))
        time.sleep(3)
        ser.write(("WEAK SHAKE").encode('utf-8'))
        time.sleep(3)
        ser.write(("STRONG SHAKE").encode('utf-8'))
        time.sleep(3)
        ser.write(("FINAL").encode('utf-8'))
        time.sleep(3)
        ser.write(("IDLE").encode('utf-8'))
        time.sleep(3)
        
