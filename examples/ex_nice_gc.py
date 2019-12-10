import spidev
import RPi.GPIO as GPIO
from time import sleep
from time import time
import sys
import pyADS1262 as adc
import os
import signal
import gc


#define the gpio pins you are using for communication outside of spi
#pinmode is BCM
#change these values only if you are wiring the ADC to the pi differently than what is indicated in the wiring diagram
mySTRT = 26 #start pin - output from pi to ADC
myPWDN  = 27 #power down - output from pi to ADC
myDRDY  = 12 #data ready - input from ADC to pi
myspiBus = 0 #this selects which pins will be used for the SPI communication. For more information refer to raspberry pi documentation
myclockDiv = 1024 #SPI clock divider - sets speed of spi communication. must be power of 2. Larger vales will mean slower SPI, but extremelylow values may result in errors

os.nice(-20) #this prioritizes this over other programs currently running on your pi 
gc.disable() #improves timing


#This is here to help the program exit gracefully upon ctrl-c
def signal_handler(signal, frame):
    global interrupted
    interrupted = True
signal.signal(signal.SIGINT, signal_handler)


#spi = spidev.SpiDev()
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(adc.STRT, GPIO.OUT) #start pin at gpio pin 4 - output
# GPIO.setup(adc.DRDY, GPIO.IN, pull_up_down = GPIO.PUD_UP) #DRDY pin
# GPIO.setup(adc.PWDN, GPIO.OUT) #PWDN pin
# GPIO.setup(13, GPIO.OUT)
# spi.open(adc.spiBus,0) # (bus, device)??
# spi.mode = 0b01
# spi.max_speed_hz = 1400000000/adc.clockDiv

fileName = sys.argv[1] + '.txt'


adc.init_GPIO_SPI(mySTRT, myDRDY, myPWDN, myspiBus, myclockDiv) #sets up spi and gpio communication on Raspberry Pi
                #The arguments here are optional. If none are provided it defaults to those in the wiring diagram
adc.restart(mySTRT, myPWDN) #restarts the ADC - arguments option defaults are in wiring diagram
adc.write_all_regs() #Writes registers with the values defined in the module - currently hard-coded. Will be more modular in future releases
print(adc.read_all_regs()) #reads back the values written in order. Returns a list of the values

print("Time to start reading")

GPIO.output(mySTRT, 1)
datafile = open(fileName, 'w')
startime = time()
errorcount=0

interrupted = False
while 1:
        timeSoFar = str(time() - startime)
        stringToWrite = timeSoFar +','+ str(read_Continuous_mode(myDRDY)) + '\n'
        datafile.write(stringToWrite)

    if interrupted:
        gc.collect()
        print('interrupted')
        exit()


