# A quick example demonstrating how to set, read from, and reset registers on the ADS126x

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

# Make a SpiDev object for our SPI connection with the ADC
spi = spidev.SpiDev()

# This handy function sets up the GPIO pins and SPI to the correct mode
adc.init_GPIO_SPI(startpin, drdypin, pwdnpin, spi, 0, 600000)

print(adc.read_all_regs(spi))

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
mode1.setregister([adc.MODE1_FILTER_FIR,
                  adc.MODE1_SBADC_ADC1, adc.MODE1_SBMAG_NONE])

mode2 = piadcs.Register(adc.MODE2_ADDRESS, 0)
mode2.setregister([adc.MODE2_BYPASS_PGAENABLED,
                  adc.MODE2_GAIN_32, adc.MODE2_DR_20])

inpmux = piadcs.Register(adc.INPMUX_ADDRESS, 0)
inpmux.setregister([adc.INPMUX_MUXP_AIN9, adc.INPMUX_MUXN_AINCOM])

# Write the set values to the registers. This function will write the default values
# to the registers unless the values are specified. It writes to all 26 registers.
adc.write_all_regs(spi, power=power.setvalue, interface=interface.setvalue, mode0=mode0.setvalue,
                   mode1=mode1.setvalue, mode2=mode2.setvalue, inpmux=inpmux.setvalue)

# Print out all register values to confirm that they were written correctly
print(adc.read_all_regs(spi))


# If you want to change the register values after they are set
# make sure to send the stop signal or tie the start pin low
# to stop conversions before sending any register commands.

# If you want to write a new value to a register make sure to clear the
# setregister attribute first. In this example we change 2 registers so
# that we can read the temperature sensor that is built into the ads126x
mode2.setvalue = 0
mode2.setregister([adc.MODE2_BYPASS_PGAENABLED,
                  adc.MODE2_GAIN_1, adc.MODE2_DR_20])

inpmux.setvalue = 0
inpmux.setregister([adc.INPMUX_MUXP_TEMPSENSORP, adc.INPMUX_MUXN_TEMPSENSORN])

# Since we are only writing to two registers and don't want to overwrite
# the data we previously sent to other registers it is better to use the
# writeToConsecutiveRegisters function than the writeToAllRegisters one since
# ONLY the two registers we want to change get changed
piadcs.writeToConsecutiveRegisters(
    spi, mode2.address, [mode2.setvalue, inpmux.setvalue])

# likewise we can use the readFromConsecutiveRegisters function to read only the
# two registers we are interested in rather than all 26
print(piadcs.readFromConsecutiveRegisters(spi, mode2.address, 2))
