#!/usr/bin/env python

# libraries
import os
import RPi.GPIO as GPIO
import time

# GPIO Mode (Board / BCM)
GPIO.setmode(GPIO.BCM)

# GPIO pin declaration
GPIO_TRIGGER = 20
GPIO_ECHO = 21

# GPIO setup
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def distance():
  # set Trigger to HIGH
  GPIO.output(GPIO_TRIGGER, True)

  # set Trigger LOW for 0.01ms
  time.sleep(0.00001)
  GPIO.output(GPIO_TRIGGER, False)

  StartTime = time.time()
  StopTime = time.time()

  # save StartTime
  while GPIO.input(GPIO_ECHO) == 0:
      StartTime = time.time()

  # save arrival time
  while GPIO.input(GPIO_ECHO) == 1:
      StopTime = time.time()

  TimeEllapsed = StopTime - StartTime
  distance = (TimeEllapsed * 34300) / 2

  return distance

if __name__=='__main__':
  try:
    while True:

      dist = distance()
      print("Jarak Terukur = %.1f cm" % dist)

      # voice control
      if dist <= 50:
        print("setengah meter didepan")
        os.system("aplay ./voice/setengahmeter.wav &")
        time.sleep(3)
      if dist > 90  and dist <= 100:
        print("satu meter didepan")
        os.system("aplay ./voice/satumeter.wav &")
        time.sleep(3)
      if dist > 190 and dist <= 200:
        print("dua meter didepan")
        os.system("aplay ./voice/duameter.wav &")
        time.sleep(3)

  except KeyboardInterrupt:
    print("Monitoring stopped by user")
    GPIO.cleanup()
