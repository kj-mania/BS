import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(10, GPIO.OUT)
GPIO.output(10, GPIO.HIGH)

while True:
    print("Buzzer ON for 2 seconds")
    GPIO.output(10, GPIO.HIGH)
    time.sleep(2)