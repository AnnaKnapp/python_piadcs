import spidev
import RPi.GPIO as GPIO
from time import sleep
from time import time
import sys
from constants import *

spi = spidev.SpiDev()
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(STRT, GPIO.OUT) #start pin at gpio pin 4 - output
# GPIO.setup(DRDY, GPIO.IN, pull_up_down = GPIO.PUD_UP) #DRDY pin
# GPIO.setup(PWDN, GPIO.OUT) #PWDN pin
# spi.open(spiBus,0) # (bus, device)??
# spi.mode = 0b01
# spi.max_speed_hz = 1400000000/clockDiv

# class Interface:
#     startpin = 41
#     def __init__(self, strtpin):
#         self.strtpin = strtpin

#     def read():
#         #bla


def ads1262_Reg_Read(reg_address):
    rreg_address = RREG | reg_address
    spi.xfer([rreg_address, 0x00])
    register_byte = spi.readbytes(1)
    return register_byte



def ads1262_Reg_Write(reg_address, data):
    #I beleive this library automatically brings CS low
    #if this doesnt work try spi.xfer2() to keep CS low
    wreg_address = WREG | reg_address
    spi.xfer([wreg_address, 0x00, data])


def ads1262_Read_Data_By_Command():
    spi.xfer2([RDATA])
    adc_data_out = spi.readbytes(6)
    print(adc_data_out)


def init_GPIO_SPI(STRT=26, DRDY=12, PWDN=27, spiBus=0, clockDiv=1024):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(STRT, GPIO.OUT) #start pin at gpio pin 4 - output
    GPIO.setup(DRDY, GPIO.IN, pull_up_down = GPIO.PUD_UP) #DRDY pin
    GPIO.setup(PWDN, GPIO.OUT) #PWDN pin
    spi.open(spiBus,0) # (bus, device)??
    spi.mode = 0b01
    spi.max_speed_hz = int(1400000000/clockDiv)  #change to 1500000000 for RPi4


def restart(STRT=26, PWDN=27):
    GPIO.output(PWDN, 0) #turn it off
    sleep(.5) #let it have a nap
    GPIO.output(PWDN, 1) #turn it on
    GPIO.output(STRT, 0) #Set start low so conversions do not run and DRDY does not pulse
    sleep(2)

def read_Continuous_mode(DRDY = 12):
    incoming = GPIO.wait_for_edge(DRDY, GPIO.FALLING, timeout=100)
    datain = spi.readbytes(6)
    if datain[5] != sum(datain[1:5])+0x9B & 255:
        print("ERR - checksum failed")
        return float('nan')
    else:
        combined_data = datain[1] << 24 | datain[2] << 16 | datain[3] << 8 | datain[4]
        if(combined_data & (1<<31)) !=0:
            combined_data = combined_data - (1<<32)
        converteddata = combined_data*(2.5/2**31)
        return converteddata


def write_all_regs():
    ads1262_Reg_Write(POWER, 0x01)      #Aincom level shift for isolated sensors disabled - 0x01
    sleep(.01)
    ads1262_Reg_Write(INTERFACE, 0x05)  #checksum enabled
    sleep(.01)
    ads1262_Reg_Write(MODE0, 0x00)      
    sleep(.01)
    ads1262_Reg_Write(MODE1, 0x00)  
    sleep(.01)
    ads1262_Reg_Write(MODE2,  0x28) #sets PGA and datarate
    sleep(.01)
    ads1262_Reg_Write(INPMUX, 0x01) #Ain0 is + input and Ain0 is - input. to change please see datasheet
    sleep(.01)  
    ads1262_Reg_Write(OFCAL0, 0x00) 
    sleep(.01)  
    ads1262_Reg_Write(OFCAL1, 0x00) 
    sleep(.01)  
    ads1262_Reg_Write(OFCAL2, 0x00) 
    sleep(.01)  
    ads1262_Reg_Write(FSCAL0, 0x00) 
    sleep(.01)  
    ads1262_Reg_Write(FSCAL1, 0x00) 
    sleep(.01)  
    ads1262_Reg_Write(FSCAL2, 0x40) 
    sleep(.01)  
    ads1262_Reg_Write(IDACMUX, 0xBB)    
    sleep(.01)  
    ads1262_Reg_Write(IDACMAG, 0x00)    
    sleep(.01)  
    ads1262_Reg_Write(REFMUX, 0x00) 
    sleep(.01)    
    ads1262_Reg_Write(TDACP, 0x00)  
    sleep(.01)    
    ads1262_Reg_Write(TDACN, 0x00)  
    sleep(.01)    
    ads1262_Reg_Write(GPIOCON, 0x00)    
    sleep(.01)    
    ads1262_Reg_Write(GPIODIR, 0x00)    
    sleep(.01)    
    ads1262_Reg_Write(GPIODAT, 0x00)    
    sleep(.01)    
    ads1262_Reg_Write(ADC2CFG, 0x00)    
    sleep(.01)    
    ads1262_Reg_Write(ADC2MUX, 0x01)    
    sleep(.01)    
    ads1262_Reg_Write(ADC2OFC0, 0x00)   
    sleep(.01)    
    ads1262_Reg_Write(ADC2OFC1, 0x00)   
    sleep(.01)    
    ads1262_Reg_Write(ADC2FSC0, 0x00)   
    sleep(.01)    
    ads1262_Reg_Write(ADC2FSC1, 0x40)   
    sleep(.01)

def read_all_regs():
    reglist = []
    reglist.append(ads1262_Reg_Read(POWER))         
    sleep(.01)
    reglist.append(ads1262_Reg_Read(INTERFACE))
    sleep(.01)
    reglist.append(ads1262_Reg_Read(MODE0))
    sleep(.01)
    reglist.append(ads1262_Reg_Read(MODE1))
    sleep(.01)
    reglist.append(ads1262_Reg_Read(MODE2))
    sleep(.01)
    reglist.append(ads1262_Reg_Read(INPMUX))
    sleep(.01)  
    reglist.append(ads1262_Reg_Read(OFCAL0)) 
    sleep(.01)  
    reglist.append(ads1262_Reg_Read(OFCAL1)) 
    sleep(.01)  
    reglist.append(ads1262_Reg_Read(OFCAL2))  
    sleep(.01)  
    reglist.append(ads1262_Reg_Read(FSCAL0)) 
    sleep(.01)  
    reglist.append(ads1262_Reg_Read(FSCAL1))
    sleep(.01)  
    reglist.append(ads1262_Reg_Read(FSCAL2))
    sleep(.01)  
    reglist.append(ads1262_Reg_Read(IDACMUX)) 
    sleep(.01)  
    reglist.append(ads1262_Reg_Read(IDACMAG))
    sleep(.01)  
    reglist.append(ads1262_Reg_Read(REFMUX))
    sleep(.01)    
    reglist.append(ads1262_Reg_Read(TDACP))
    sleep(.01)    
    reglist.append(ads1262_Reg_Read(TDACN))
    sleep(.01)    
    reglist.append(ads1262_Reg_Read(GPIOCON))
    sleep(.01)    
    reglist.append(ads1262_Reg_Read(GPIODIR))
    sleep(.01)    
    reglist.append(ads1262_Reg_Read(GPIODAT))
    sleep(.01)    
    reglist.append(ads1262_Reg_Read(ADC2CFG))
    sleep(.01)    
    reglist.append(ads1262_Reg_Read(ADC2MUX)) 
    sleep(.01)    
    reglist.append(ads1262_Reg_Read(ADC2OFC0))
    sleep(.01)    
    reglist.append(ads1262_Reg_Read(ADC2OFC1))
    sleep(.01)    
    reglist.append(ads1262_Reg_Read(ADC2FSC0))
    sleep(.01)    
    reglist.append(ads1262_Reg_Read(ADC2FSC1))
    sleep(.01)
    return reglist
