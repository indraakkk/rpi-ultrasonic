#!/usr/bin/env python

# libraries
import RPi.GPIO as GPIO
import time

import pyaudio
import wave

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
setengahMeter = wave.open(r"./voice/setengahmeter.wav", "rb")
satuMeter = wave.open(r"./voice/satumeter.wav", "rb")
duaMeter = wave.open(r"./voice/duameter.wav", "rb")
p = pyaudio.PyAudio()


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
    stream = p.open(format=p.get_format_from_width(setengahMeter.getsampwidth()),
                channels=setengahMeter.getnchannels(),
                rate=setengahMeter.getframerate(),
                output=True)

    data = setengahMeter.readframes(chunk)

    # while data:

    while True:
      stream.write(data)
      data = setengahMeter.readframes(chunk)

      dist = distance()
      print("Jarak Terukur = %.1f cm" % dist)
      time.sleep(1)

      # control to voice

  
  except KeyboardInterrupt:
    # print("Pengukuran dihentikan")
    # GPIO.cleanup()
      stream.stop_stream()
      stream.close()

      p.terminate()
      print("voice stopped")