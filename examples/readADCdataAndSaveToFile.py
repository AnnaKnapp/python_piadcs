# A quick example demonstrating how to set registers, read ADC conversion data,
# and save that to a .csv file. It also keeps track of the rate of
# communication error as a way of checking that SPI speed is set appropriately.
import spidev
import RPi.GPIO as GPIO
from time import sleep
from time import time
import sys
from piadcs import ads126x as adc
import piadcs
import os
import signal
import gc


# First thing you must do is define your Pins and SPI bus for
#  communication with the ADC
startpin = 22
drdypin = 4
pwdnpin = 27

# This is here to help the program exit gracefully upon ctrl-c. Since it
# runs infinetly otherwise.


def signal_handler(signal, frame):
    global interrupted
    interrupted = True


signal.signal(signal.SIGINT, signal_handler)

# os.nice(-20)  # this prioritizes this over other programs currently running on your pi - if you want to enable this you need to use sudo
gc.disable()  # improves timing

# This opens a file to write the ADC data to. If the file doesn't exist already
# it will make it. If you don't change this it will make the file right in the
# directory you are running this program from so please change it if you don't
# want this to happen.
datafile = open("test.txt", 'w')

# Make a SpiDev object for our SPI connection with the ADC
spi = spidev.SpiDev()

# This handy function sets up the GPIO pins and SPI to the correct mode
adc.init_GPIO_SPI(startpin, drdypin, pwdnpin, spi, 0, 600000)

# This function restarts the ADC ensuring it is ready to receive commands
adc.restart(startpin, pwdnpin)

# Initialize a register using the built in register object. Register addressed
# for all registers on the ADS126x are stored in the constants file for easy use
power = piadcs.Register(adc.POWER_ADDRESS, 0)

# use the setregister function to change the setvalue to the desired byte.
# The settings for each register are defined in the constants file. In order
# for this to work properly either set it with the default value or ensure that
# you specify ALL possible settings. In this case even though the internal ref
# is enabled in the default we still need to specify it if we want to enable
# the vbias otherwise it will be disabled.
power.setregister([adc.POWER_VBIAS_ENABLED, adc.POWER_INTREF_ENABLED])

# This initializes and sets the Interface register - Note how all options are
# specified regardless of if they are defaults or not
interface = piadcs.Register(adc.INTERFACE_ADDRESS, 0)
interface.setregister([adc.INTERFACE_TIMEOUT_DISABLED,
                      adc.INTERFACE_STATUS_ENABLED, adc.INTERFACE_CRC_CHECKSUM])

# This sets Mode0 to the default values for all settings. The default
# values for programming registers are defined in the ADS126x datasheet
# and can be found in the constants file for quick access
mode0 = piadcs.Register(adc.MODE0_ADDRESS, adc.MODE0_DEFAULT)

mode1 = piadcs.Register(adc.MODE1_ADDRESS, 0)
mode1.setregister([adc.MODE1_FILTER_SINC4,
                  adc.MODE1_SBADC_ADC1, adc.MODE1_SBMAG_NONE])

mode2 = piadcs.Register(adc.MODE2_ADDRESS, 0)
mode2.setregister([adc.MODE2_BYPASS_PGAENABLED,
                  adc.MODE2_GAIN_1, adc.MODE2_DR_20])

inpmux = piadcs.Register(adc.INPMUX_ADDRESS, 0)
inpmux.setregister([adc.INPMUX_MUXP_AIN9, adc.INPMUX_MUXN_AINCOM])

# Write the set values to the registers. This function will write the default values
# to the registers unless the values are specified. It writes to all 26 registers.
adc.write_all_regs(spi, power=power.setvalue, interface=interface.setvalue, mode0=mode0.setvalue,
                   mode1=mode1.setvalue, mode2=mode2.setvalue, inpmux=inpmux.setvalue)

# Print out all register values to confirm that they were written correctly
print(adc.read_all_regs(spi))

startime = time()
errorcount = 0
successcount = 0
interrupted = False

# if you forget this, the ADC will not start conversions
adc.startConversions(startpin)

while 1:
    rawdata, err = adc.read_Continuous_CHK(spi, drdypin)
    if err == None:
        converteddata = adc.convert_data(rawdata)
        timeSoFar = str(time() - startime)
        stringToWrite = timeSoFar + ',' + str(converteddata) + '\n'
        # print(stringToWrite)
        datafile.write(stringToWrite)
        successcount += 1
    else:
        errorcount += 1
        # print(err) # you can print the error to see what is going wrong - if the communcation is failing or if DRDY is not dropping

    if interrupted:  # this allows the program to exit gracefully when ctrl-c is used to stop it
        datafile.close()
        errorrate = float(errorcount)/float(successcount)
        print("Error rate:" + str(errorrate) + '\n')
        gc.collect()
        print('Exited Gracefully')
        exit()
