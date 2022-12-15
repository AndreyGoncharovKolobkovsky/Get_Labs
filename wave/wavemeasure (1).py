import waveFunctions as F
import time
import RPi.GPIO as GPIO
n = int(input())
s = []
F.initSpiAdc()
dac = [26, 19, 13, 6, 5, 11, 9, 10]
leds = [21, 20, 16, 12, 7, 8, 25, 24]
troyka = 17
comp = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(troyka, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)
GPIO.setup(dac, GPIO.OUT, initial = GPIO.LOW)
for i in range(len(leds)):
    GPIO.setup(leds[i], GPIO.OUT)
def toBin(Value):
    return [int(elm) for elm in bin(Value)[2:].zfill(8)]
def adc():
    r = 256
    left = 0
    md = (r + left) // 2
    while (r - left) > 1:
        GPIO.output(dac, toBin(md))
        time.sleep(0.001)
        compVal = GPIO.input(comp)
        if compVal == 0:
            r = md
        else:
            left = md
        md = (r + left) // 2
    #volt = 3.3 * left / 256
    return left
try:
    k = int(input())
    t1 = t2 = time.time()
    while (t2-t1 < n):
        s.append(adc())  
        t2 = time.time()
    F.save(s, t1, t2)
finally:    
    F.deinitSpiAdc()