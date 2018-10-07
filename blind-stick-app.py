#!/usr/bin/env python

# libraries
import os
import RPi.GPIO as GPIO
import time

# import pyaudio
# import wave

# GPIO Mode (Board / BCM)
GPIO.setmode(GPIO.BCM)

# GPIO pin declaration
GPIO_TRIGGER = 20
GPIO_ECHO = 21

# GPIO setup
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

# Define stream chunk
chunk = 1024

# setup for pyaudio file
# halfMeter = wave.open(r"./voice/setengahmeter.wav", "rb")
# oneMeter = wave.open(r"./voice/satumeter.wav", "rb")
# twoMeter = wave.open(r"./voice/duameter.wav", "rb")
# p = pyaudio.PyAudio()

# streamHalf = p.open(format=p.get_format_from_width(halfMeter.getsampwidth()),
#             channels=halfMeter.getnchannels(),
#             rate=halfMeter.getframerate(),
#             output=True)

# streamOne = p.open(format=p.get_format_from_width(oneMeter.getsampwidth()),
#             channels=oneMeter.getnchannels(),
#             rate=oneMeter.getframerate(),
#             output=True)

# streamTwo = p.open(format=p.get_format_from_width(twoMeter.getsampwidth()),
#         channels=twoMeter.getnchannels(),
#         rate=twoMeter.getframerate(),
#         output=True)


# dataHalf = halfMeter.readframes(chunk)
# dataOne = oneMeter.readframes(chunk)
# dataTwo = twoMeter.readframes(chunk)


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
      # time.sleep(1)
      if dist > 3 and dist <= 5:
        print("setengah meter didepan")
        # os.system("aplay ./voice/setengahmeter.wav &")

      if dist > 6 and dist <= 10:
        print("satu meter didepan")
        # os.system("aplay ./voice/satumeter.wav &")

      if dist > 11 and dist <= 20:
        print("dua meter didepan")
        # os.system("aplay ./voice/duameter.wav &")
      sleep(0.1)
      else:
        print("oke")

  except KeyboardInterrupt:
    print("Monitoring stopped by user")
    GPIO.cleanup()
