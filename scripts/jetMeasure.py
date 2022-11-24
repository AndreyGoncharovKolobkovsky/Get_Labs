import spidev
import jetFunctions as f
import time
import RPi.GPIO as GPIO
import numpy as np

directionPin = 27
enablePin = 22
stepPin = 17

spi = spidev.SpiDev()
try:
    f.initSpiAdc()
    f.initStepMotorGpio()
    f.stepBackward(0)
    s = []
    samp = 15
    count = 500
    step = 2
    for i in range(count):
        s.append(f.getMeanAdc(samp))
        f.stepForward(step)
    f.saveMeasures(s, samp, step, count)
    f.stepBackward(0)
finally:
    f.deinitSpiAdc()
    f.deinitStepMotorGpio()
