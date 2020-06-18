import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.OUT)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def ring():
    GPIO.output(14, GPIO.HIGH)
    time.sleep(0.02)
    GPIO.output(14, GPIO.LOW)

ring()
time.sleep(0.2)
ring()

down = False
while True:
    input_state = GPIO.input(27)
    if input_state == False and not down:
        down = True
        ring()
    if input_state == True and down:
        down = False
