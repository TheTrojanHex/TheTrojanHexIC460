


import os
import spidev
import serial
import RPi.GPIO as GPIO
#import IoTSend
import numpy

tempFlag = 0

IN1 = 27
IN2 = 17
IN3 = 2
IN4 = 3


spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=5000

GPIO.setmode(GPIO.BCM)
GPIO.setup(IN1,GPIO.OUT)
GPIO.setup(IN2,GPIO.OUT)

GPIO.setup(IN3,GPIO.OUT)
GPIO.setup(IN4,GPIO.OUT)




###########################

def ReadChannel(channel):
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data
 
# Function to convert data to voltage level,
# rounded to specified number of decimal places.
def ConvertVolts(data,places):
  volts = (data * 3.3) / float(1023)
  volts = round(volts,places)
  return volts
 
# Function to calculate temperature from
# TMP36 data, rounded to specified
# number of decimal places.
def ConvertTemp(data,places):
 
  # ADC Value
  # (approx)  Temp  Volts
  #    0      -50    0.00
  #   78      -25    0.25
  #  155        0    0.50
  #  233       25    0.75
  #  310       50    1.00
  #  465      100    1.50
  #  775      200    2.50
  # 1023      280    3.30
 
  temp = ((data * 330)/float(1023))#-50 40
  temp = round(temp,places)
  return temp




def readChannel(channel):
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data


def readTempSensor():
    temp = readChannel(0)
    return temp


def WINDOWS_OPEN():
    print("window open")
    GPIO.output(IN1, True)
    GPIO.output(IN2, False)
    time.sleep(1)
    GPIO.output(IN1, False)
    GPIO.output(IN2, False)
    time.sleep(1)

def WINDOWS_CLOSE():
    print("window close")
    GPIO.output(IN1, False)
    GPIO.output(IN2, True)
    time.sleep(1)
    GPIO.output(IN1, False)
    GPIO.output(IN2, False)
    time.sleep(1)

def CURTAIN_CLOSE():
      print("curtain close")
      GPIO.output(IN3, False)
      GPIO.output(IN4, True)
      time.sleep(2.0)
      GPIO.output(IN3, False)
      GPIO.output(IN4, False)
      time.sleep(1)

def CURTAIN_OPEN():
      print("curtain open")
      GPIO.output(IN3, True)
      GPIO.output(IN4, False)
      time.sleep(2.0)
      GPIO.output(IN3, False)
      GPIO.output(IN4, False)
      time.sleep(1)



WINDOWS_OPEN()
CURTAIN_OPEN()


while True:


    temp_level = ReadChannel(7)
    temp_volts = ConvertVolts(temp_level,2)
    temp       = ConvertTemp(temp_level,2)

    print ("--------------------------------------------")
    print("Temp : {} ({}V) {} deg C".format(temp_level,temp_volts,temp))
    time.sleep(1.0)
    if((temp > 30)):
      WINDOWS_OPEN()

    if((temp > 31)):
      print("curtain close")
      CURTAIN_CLOSE()
      
    if((temp < 29)):
      WINDOWS_CLOSE()
      
 
   



  
      break

    
 
     
          
        
      
    