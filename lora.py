import serial
import RPi.GPIO as GPIO
import struct
import time

ResetPin = 12

class LoRa():
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False) 
        GPIO.setup(ResetPin, GPIO.OUT)
        GPIO.output(ResetPin, 1)

        self.s = serial.Serial('/dev/ttyS0', 115200, timeout = 1)

    def open(self):
        self.s.open()

    def close(self):
        self.s.close()

    def readline(self, timeout = None):
        if timeout != None:
            self.s.close()
            self.s.timeout = timeout
            self.s.open()
        line = self.s.readline()
        if timeout != None:
            self.s.close()
            self.s.timeout = None
            self.s.open()
        return line

    def write(self, msg):
        self.s.write(msg.encode('ascii'))

    def reset(self):
        GPIO.output(ResetPin, 0)
        time.sleep(0.1)
        GPIO.output(ResetPin, 1)
        print("Reset LoRa module")
        time.sleep(5)
        

def main():
    lr = LoRa()