import spidev
import RPi.GPIO as GPIO
from time import sleep
from time import time

import sys

# opcodes
RREG = 0x20  # Read registers
WREG = 0x40  # Write registers


class Register:
    """ A class used to represent a register on a TI ADC
    ...
    Attributes
    ----------
    address : byte
        The address of the register
    setvalue : byte
        The value that you want to write to the register. This
        should be set either by using the default value or the
        setregister function

    Methods
    -------
    setregister(data)
        Takes a list of bytes representing different register settings
        and combines them into a single byte to send to the register
     """

    def __init__(self, address, setvalue):
        """
        Parameters
        ----------
        address : byte
            The address of the register
        setvalue : byte
            The value that you want to write to the register. This
            should be set either by using the default value or the
            setregister function

        """
        self.address = address
        self.setvalue = setvalue

    def setregister(self, settingsList):
        """
        Takes a list of bytes representing different register settings
        and combines them into a single byte to send to the register.
        Since this function uses the OR operator it is critical to
        include ALL settings for the given register even if some are left
        to the default. If a setting is not included it will be set to to 0.

        Parameters
        ----------
        data : list
            A list of bytes where each byte represents one setting of a given
            register. The list should not be longer or shorter than the number
            of settings that exist for the register you want to send them to.

        """
        for setting in settingsList:
            self.setvalue = setting | self.setvalue


def writeToConsecutiveRegisters(connection, startingreg, data):
    """writes a list of values to consecutive registers on an ADC.

    Parameters
    ----------
    connection : SpiDev object
        See documentation for python Spidev (https://pypi.org/project/spidev/)
    startingreg : byte
        The address of the first register you want to write to
    data : list
        The values you would like to write to the register
        see section 9.6 of the ADS126x datasheet for an explanations
        of what values have what functions at a given register
    """
    data.insert(0, len(data) - 1)
    data.insert(0, WREG | startingreg)
    connection.xfer3(data)


def readFromConsecutiveRegisters(connection, startingreg, numbertoread):
    """writes a list of values to consecutive registers on an ADC.

    Parameters
    ----------
    connection : SpiDev object
        See documentation for python Spidev (https://pypi.org/project/spidev/)
    startingreg : byte
        The address of the first register you want to read from
    numbertoread : byte
        The number of registers you would like to read from

    Returns
    -------
    list
        Returns list of register values from consecutive registers starting
        with the specified register
    """

    connection.xfer2([RREG | startingreg, numbertoread - 1])
    regvalues = connection.readbytes(numbertoread)
    return regvalues


def writeToSingleRegister(connection, reg_address, data):
    """writes a value to a register on the ADS1262.

    Parameters
    ----------
    connection : SpiDev object
        See documentation for python Spidev (https://pypi.org/project/spidev/)
    reg_address : byte
        The address of the register you would like to write to
    data : byte
        The value you would like to write to the register
        see section 9.6 of the ADS1262 datasheet for an explanations
        of what values have what functions at a given register
    """
    wreg_address = WREG | reg_address
    connection.writebytes([wreg_address, 0x00, data])
