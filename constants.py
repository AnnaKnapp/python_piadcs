RREG    = 0x20      #Read n nnnn registers starting at address r rrrr
                                #first byte 001r rrrr (2xh)(2) - second byte 000n nnnn(2)
WREG    = 0x40      #Write n nnnn registers starting at address r rrrr
                                #first byte 010r rrrr (2xh)(2) - second byte 000n nnnn(2)
START   = 0x08      #Start/restart (synchronize) conversions
STOP    = 0x0A      #Stop conversion
RDATAC  = 0x10      #Enable Read Data Continuous mode. 
#This mode is the default mode at power-up.
SDATAC  = 0x11      #Stop Read Data Continuously mode
RDATA   = 0x12      #Read data by command; supports multiple read back.


#define ALL of the register addresses
POWER       = 0x01
INTERFACE   = 0x02
MODE0       = 0x03
MODE1       = 0x04
MODE2       = 0x05 #sets PGA and datarate
INPMUX      = 0x06 #this sets the inputs - a value of 01 means that +input is Ain0 and -input is Ain1. for other configurations see datasheet
OFCAL0      = 0x07
OFCAL1      = 0x08
OFCAL2      = 0x09
FSCAL0      = 0x0A
FSCAL1      = 0x0B
FSCAL2      = 0x0C
IDACMUX     = 0x0D
IDACMAG     = 0x0E
REFMUX      = 0x0F
TDACP       = 0x10
TDACN       = 0x11
GPIOCON     = 0x12
GPIODIR     = 0x13
GPIODAT     = 0x14
ADC2CFG     = 0x15
ADC2MUX     = 0x16
ADC2OFC0    = 0x17
ADC2OFC1    = 0x18
ADC2FSC0    = 0x19
ADC2FSC1    = 0x1A