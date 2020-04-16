import spidev
import RPi.GPIO as GPIO
from time import sleep
from time import time
import sys
from constants import *

#initializes an spi object using spidev
spi = spidev.SpiDev()


def ads1262_Reg_Read(reg_address):
    """returns the value of a register on the ADS1262.
    
    Arguments
    ----------
    reg_address : byte
        The address of the register you would like to read from
        see section 9.6 of the ADS1262 datasheet for register maps

    Returns
    -------
    byte
        The value stored at the register
    """
    rreg_address = RREG | reg_address
    spi.xfer([rreg_address, 0x00])
    register_byte = spi.readbytes(1)
    return register_byte



def ads1262_Reg_Write(reg_address, data):
    """writes a value to a register on the ADS1262.
    
    Arguments
    ----------
    reg_address : byte
        The address of the register you would like to read from
        see section 9.6 of the ADS1262 datasheet for register maps
    data : byte
        The value you would like to write to the register
        see section 9.6 of the ADS1262 datasheet for an explanations
        of what values have what functions at a given register
    """
    #if this doesnt work try spi.xfer2() to keep CS low
    wreg_address = WREG | reg_address
    spi.xfer([wreg_address, 0x00, data])


def ads1262_Read_Data_By_Command():
    """reads a single conversion from the ADS1262. Use for reading in pulse conversion mode See datasheet section 9.4.1.2

    Returns
    -------
    bytes
        6 bytes total. The first is a status byte, the next four
        are the 32-bit the conversion data. The last is a checksum.
        the checksum byte is the lower 8-bit sum of the data 
        conversion bytes plus an offset value 9Bh.
    """
    spi.xfer2([RDATA])
    adc_data_out = spi.readbytes(6)
    return adc_data_out


def init_GPIO_SPI(STRT=26, DRDY=12, PWDN=27, spiBus=0, clockDiv=1024):
    """initializes the GPIO pins and SPI bus on the Raspbery Pi
    
    Arguments
    ----------
    STRT : int, optional
        The BCM number for the GPIO pin connected to the start pin of the ADC
        the default for this is 26 as shown in the wiring diagram
    DRDY : int, optional
        The BCM number for the GPIO pin connected to the data ready pin of the ADC
        the default for this is 12 as shown in the wiring diagram
    PWDN : int, optional
        The BCM number for the GPIO pin connected to the power down pin of the ADC
        the default for this is 27 as shown in the wiring diagram
    spiBus : int, optional
        The spi bus on the Raspberry Pi that you want to use to communicate with the ADS1262
        bus 0 is the default and is the only bus available on the 40 pin RPi header
    clockdiv : int, optional
        The clock divider for spi communication. Larger numbers mean slower spi speeds.
        This number must be a power of 2
    """
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(STRT, GPIO.OUT) #start pin at gpio pin 4 - output
    GPIO.setup(DRDY, GPIO.IN, pull_up_down = GPIO.PUD_UP) #DRDY pin
    GPIO.setup(PWDN, GPIO.OUT) #PWDN pin
    spi.open(spiBus,0) # (bus, device)??
    spi.mode = 0b01
    spi.max_speed_hz = int(1400000000/clockDiv)  #change to 1500000000 for RPi4


def restart(STRT=26, PWDN=27):
     """restarts the ADS1262
    
    Arguments
    ----------
    STRT : int, optional
        The BCM number for the GPIO pin connected to the start pin of the ADC
        the default for this is 26 as shown in the wiring diagram
    PWDN : int, optional
        The BCM number for the GPIO pin connected to the power down pin of the ADC
        the default for this is 27 as shown in the wiring diagram
    """
    
    GPIO.output(PWDN, 0) #turn it off
    sleep(.5) #let it have a nap
    GPIO.output(PWDN, 1) #turn it on
    GPIO.output(STRT, 0) #Set start low so conversions do not run and DRDY does not pulse
    sleep(2)

def read_Continuous_mode(DRDY = 12):
    """reads a single byte of data from the ADC. Use for reading in pulse conversion mode See datasheet section 9.4.1.2

    Arguments
    ----------
    DRDY : int, optional
        The BCM number for the GPIO pin connected to the data ready pin of the ADC
        the default for this is 12 as shown in the wiring diagram

    Returns
    -------
    float
        will either return return a float indicating a voltage between 2.5v and -2.5v or
        a NaN indicating that the checksum failed and there was some communication error.
        This error in communcation is often due to linux prioritizing other tasks and missing
        the output. Can be improved by using os.nice or closing other applications.
    """
    incoming = GPIO.wait_for_edge(DRDY, GPIO.FALLING, timeout=100)
    datain = spi.readbytes(6)
    if datain[5] != sum(datain[1:5])+0x9B & 255:
        print("ERR - checksum failed")
        return float('nan')
    else:
        combined_data = datain[1] << 24 | datain[2] << 16 | datain[3] << 8 | datain[4]
        if(combined_data & (1<<31)) !=0:
            combined_data = combined_data - (1<<32)
        converteddata = float(combined_data*(2.5/2**31))
        return converteddata


def write_all_regs(power = 0x01, interface = 0x05, mode0 = 0x00, mode1 = 0x00, mode2 = 0x04,
inpmux = 0x01, ofcal0 = 0x00, ofcal1 = 0x00, ofcal2 = 0x00, fscal0 = 0x00, fscal1 = 0x00, 
fscal2 = 0x40, idacmux = 0xBB, idacmag = 0x00, refmux = 0x00, tdacp = 0x00, tdacn = 0x00, 
gpiocon =0x00, gpiodir = 0x00, gpiodat = 0x00, adc2cfg = 0x00, adc2mux = 0x01, adc2ofc0 = 0x00,
adc2ofc1 = 0x00, adc2fsc0 = 0x00, adc2fsc1 = 0x40):
    """writes the default (or user specified) values to all the registers on the ADS1262.

    Arguments
    ----------
    This function has 26 optional arguments wich correspond to the 26 8-bit programming registers on the ADS126x.
    The default arguments are the default values for those registers. This is based on the ADS126x datasheet.
    Please refer to section 9.6 (register maps) of that datasheet before using these arguments.

    """
    ads1262_Reg_Write(POWER, power)      #Aincom level shift for isolated sensors disabled - 0x01
    sleep(.01)
    ads1262_Reg_Write(INTERFACE, interface)  #checksum enabled
    sleep(.01)
    ads1262_Reg_Write(MODE0, mode0)      
    sleep(.01)
    ads1262_Reg_Write(MODE1, mode1)  
    sleep(.01)
    ads1262_Reg_Write(MODE2, mode2) #sets PGA and datarate
    sleep(.01)
    ads1262_Reg_Write(INPMUX, inpmux) #Ain0 is + input and Ain0 is - input. to change please see datasheet
    sleep(.01)  
    ads1262_Reg_Write(OFCAL0, ofcal0) 
    sleep(.01)  
    ads1262_Reg_Write(OFCAL1, ofcal1) 
    sleep(.01)  
    ads1262_Reg_Write(OFCAL2, ofcal2) 
    sleep(.01)  
    ads1262_Reg_Write(FSCAL0, fscal0) 
    sleep(.01)  
    ads1262_Reg_Write(FSCAL1, fscal1) 
    sleep(.01)  
    ads1262_Reg_Write(FSCAL2, fscal2) 
    sleep(.01)  
    ads1262_Reg_Write(IDACMUX, idacmux)    
    sleep(.01)  
    ads1262_Reg_Write(IDACMAG, idacmag)    
    sleep(.01)  
    ads1262_Reg_Write(REFMUX, refmux) 
    sleep(.01)    
    ads1262_Reg_Write(TDACP, tdacp)  
    sleep(.01)    
    ads1262_Reg_Write(TDACN, tdacn)  
    sleep(.01)    
    ads1262_Reg_Write(GPIOCON, gpiocon)    
    sleep(.01)    
    ads1262_Reg_Write(GPIODIR, gpiodir)    
    sleep(.01)    
    ads1262_Reg_Write(GPIODAT, gpiodat)    
    sleep(.01)    
    ads1262_Reg_Write(ADC2CFG, adc2cfg)    
    sleep(.01)    
    ads1262_Reg_Write(ADC2MUX, adc2mux)    
    sleep(.01)    
    ads1262_Reg_Write(ADC2OFC0, adc2ofc0)   
    sleep(.01)    
    ads1262_Reg_Write(ADC2OFC1, adc2ofc1)   
    sleep(.01)    
    ads1262_Reg_Write(ADC2FSC0, adc2fsc0)   
    sleep(.01)    
    ads1262_Reg_Write(ADC2FSC1, adc2fsc1)   
    sleep(.01)

def read_all_regs():
    
    """reads the values of all the registers on the ADS1262.
    
    Arguments
    ----------
    reg_address : byte
        The address of the register you would like to read from
        see section 9.6 of the ADS1262 datasheet for register maps
    data : byte
        The value you would like to write to the register
        see section 9.6 of the ADS1262 datasheet for an explanations
        of what values have what functions at a given register
    """
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
