from piadcs import readFromConsecutiveRegisters, writeToConsecutiveRegisters
import spidev
import RPi.GPIO as GPIO
from time import sleep
from .constants import *


def startConversions(strt):
    """Starts ADC1 conversions by pulling the START pin high

    Arguments
    ----------
    STRT : int
        The BCM number for the GPIO pin connected to the start pin of the ADC
        Pin 26 is used for this in the example wiring diagram
    """
    GPIO.output(strt, 1)


def stopConversions(strt):
    """Stops ADC1 conversions by pulling the START pin low

    Arguments
    ----------
    STRT : int
        The BCM number for the GPIO pin connected to the start pin of the ADC
        Pin 26 is used for this in the example wiring diagram
    """
    GPIO.output(strt, 0)


def startCommand(connection):
    """Starts ADC1 conversions using the start command sent over SPI

    Arguments
    ----------
    Connection : SpiDev object
        The spi connection you use to communicate with the ADC. See spidev
        documentation for more details (https://pypi.org/project/spidev/)
    """
    connection.xfer2([START1])


def stopCommand(connection):
    """Stops ADC1 conversions using the stop command sent over SPI

    Arguments
    ----------
    Connection : SpiDev object
        The spi connection you use to communicate with the ADC. See spidev
        documentation for more details (https://pypi.org/project/spidev/)
    """
    connection.xfer2([STOP1])


def init_GPIO_SPI(STRT, DRDY, PWDN, connection, spiBus, spispeedHz, spidevice=0):
    """initializes the GPIO pins and SPI bus on the Raspbery Pi

    Arguments
    ----------
    STRT : int
        The BCM number for the GPIO pin connected to the start pin of the ADC
        Pin 26 is used for this in the example wiring diagram
    DRDY : int
        The BCM number for the GPIO pin connected to the data ready pin of
        the ADC. Pin 4 is used for this in the example wiring diagram
    PWDN : int
        The BCM number for the GPIO pin connected to the power down pin of the
        ADC. Pin 27 is used for this in the example wiring diagram
    Connection : SpiDev object
        The spi connection you use to communicate with the ADC. See spidev
        documentation for more details (https://pypi.org/project/spidev/)
    spiBus : int
        The spi bus on the Raspberry Pi that you want to use to communicate
        with the ADS126x. bus 0 is is used for this in the example
    spispeedHz : int
        The speed in Hertz of the SPI clock. This should scale depending on
        your ADC datarate. Higher data rates will require faster SPI.
        communication
    spidevice : int, optional
        Sets SPI device if using multiple devices on the same SPI bus. Default
        is zero and can be left as such if you are only using the one device.
    """
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(STRT, GPIO.OUT)  # start pin at gpio pin 4 - output
    GPIO.setup(DRDY, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # DRDY pin
    GPIO.setup(PWDN, GPIO.OUT)  # PWDN pin
    connection.open(spiBus, spidevice)  # (bus, device)
    connection.mode = 0b01
    connection.bits_per_word = 8
    connection.max_speed_hz = spispeedHz


def restart(strt, pwdn):
    """restarts the ADS126x

    Arguments
    ----------
    STRT : int
        The BCM number for the GPIO pin connected to the start pin of the ADC
        In the example wiring diagram this is pin 22
    PWDN : int
        The BCM number for the GPIO pin connected to the power down pin
        of the ADC. In the example wiring diagram this is pin 27
    """
    GPIO.output(pwdn, 0)  # turn it off
    sleep(.5)  # let it have a nap
    GPIO.output(pwdn, 1)  # turn it on
    # Set start low so conversions don't run and DRDY doesn't pulse
    GPIO.output(strt, 0)
    sleep(2)


def read_Data_By_Command_CHK(connection):
    """reads a single conversion from the ADS1262. Use for reading in pulse
    conversion mode See datasheet section 9.4.1.2.

    Arguments
    ----------
    Connection : SpiDev object
        The spi connection you use to communicate with the ADC. See spidev
        documentation for more details (https://pypi.org/project/spidev/)

    Returns
    -------
    tuple
        Returns a tuple containing a list of 4 bytes representing the
        raw output of the ADC, and an error check. If the error check
        is None that means that the checksum passed and the data is useable.
        If the checksum fails the list will be None, and the error check
        will be the string "Checksum Failed". If you are getting a lot of
        this error, you may want to consider increasing SPI speed.
    """
    connection.xfer2([RDATA1])
    datain = connection.readbytes(6)
    if datain[5] != sum(datain[1:5])+0x9B & 255:
        return None, "Checksum Failed"
    else:
        return datain[1:5], None


def read_Continuous_CHK(connection, DRDY):
    """reads a 32 bit conversion from the ADC. Use for reading direct
    (ADS126x datasheet section 9.4.7.1)

    Arguments
    ----------
    Connection : SpiDev object
        The spi connection you use to communicate with the ADC. See spidev
        documentation for more details (https://pypi.org/project/spidev/)
    DRDY : int
        The BCM number for the GPIO pin connected to the data ready pin
        of the ADC. Pin 4 is shown for this in the wiring diagram

    Returns
    -------
    tuple
        Returns a tuple containing a list of 4 bytes representing the
        raw output of the ADC, and an error check. If the error check
        is None that means that the checksum passed and the data is useable.
        If the checksum fails the list will be None, and the error check
        will be the string "Checksum Failed". If you are getting a lot of
        this error, you may want to consider increasing SPI speed.
    """
    dataready = GPIO.wait_for_edge(DRDY, GPIO.FALLING, timeout=5000)
    if dataready is None:
        return None, 'Timeout occurred - check data ready pin, and make sure start pin or start command was used'
    else:
        datain = connection.readbytes(6)
        if datain[5] != sum(datain[1:5])+0x9B & 255:
            return None, "Checksum Failed"
        else:
            return datain[1:5], None


def convert_data(datain):
    """converts the output of the ADC into a voltage

    Arguments
    ----------
    datain : list
        A list of bytes (the raw output of the adc)

    Returns
    -------
    float
        a float indicating a voltage between 2.5v and -2.5v - This will
        not be adjusted for PGA gain. If you use a voltage reference other
        than midsupply (2.5v) which is what is used by the internal
        reference then you will need to adjust this accordingly
    """
    combined_data = datain[0] << 24 | datain[1] << 16 | datain[2] << 8 | datain[3]
    if(combined_data & (1 << 31)) != 0:
        combined_data = combined_data - (1 << 32)
    converteddata = float(combined_data*(2.5/2**31))
    return converteddata


def write_all_regs(connection, power=0x01, interface=0x05, mode0=0x00,
                   mode1=0x00, mode2=0x04, inpmux=0x01, ofcal0=0x00, ofcal1=0x00,
                   ofcal2=0x00, fscal0=0x00, fscal1=0x00, fscal2=0x40, idacmux=0xBB,
                   idacmag=0x00, refmux=0x00, tdacp=0x00, tdacn=0x00, gpiocon=0x00,
                   gpiodir=0x00, gpiodat=0x00, adc2cfg=0x00, adc2mux=0x01,
                   adc2ofc0=0x00, adc2ofc1=0x00, adc2fsc0=0x00, adc2fsc1=0x40):
    """writes the default (or user specified) values to all the registers
    on the ADS126x.

    Arguments
    ----------
    Connection : SpiDev object
        The spi connection you use to communicate with the ADC. See spidev
        documentation for more details (https://pypi.org/project/spidev/)
    Registers : byte, optional
        This function has 26 optional arguments wich correspond to the 26 8-bit
        programming registers on the ADS126x.The default arguments are the default
        values for those registers. This is based on the ADS126x datasheet.
        Options for register settings can be found in the constants file. Use the
        setregister function to change multiple values. Please also refer to 
        section 9.6 (register maps) of that datasheet before using these arguments.

    """
    registervalues = [power, interface, mode0, mode1, mode2, inpmux, ofcal0,
                      ofcal1, ofcal2, fscal0, fscal1, fscal2, idacmux, idacmag, refmux, tdacp,
                      tdacn, gpiocon, gpiodir, gpiodat, adc2cfg, adc2mux, adc2ofc0, adc2ofc1,
                      adc2fsc0, adc2fsc1]
    writeToConsecutiveRegisters(connection, POWER_ADDRESS, registervalues)


def read_all_regs(connection):
    """reads the values of all the registers on the ADS1262. starting with
    the ID register (register 0)

    Arguments
    ----------
    Connection : SpiDev object
        The spi connection you use to communicate with the ADC. See spidev
        documentation for more details (https://pypi.org/project/spidev/)
    """
    return readFromConsecutiveRegisters(connection, 0, 26)
