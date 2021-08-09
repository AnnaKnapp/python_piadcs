
#opcodes
RREG    = 0x20      #Read registers
WREG    = 0x40      #Write registers

RESET = 0x06 #Reset the ADC

START1   = 0x08      #Start ADC1 conversions
STOP1    = 0x0A      #Stop ADC1 conversion

RDATA1   = 0x12      #Read ADC1 data



#define ALL of the register addresses and options
ID_ADDRESS = 0x00 #address only this register is read-only


POWER_ADDRESS       = 0x01
POWER_DEFAULT  = 0x11

#reset indicator (Indicates ADC reset has occurred. Clear this bit to detect the next device reset.)
POWER_RESET_NO   = 0b00000000
POWER_RESET_YES  = 0b00010000

#level shift voltage enable (Enables the internal level shift voltage to the AINCOM pin. VBIAS = (VAVDD + VAVSS)/2)
POWER_VBIAS_DISABLED  = 0b00000000
POWER_VBIAS_ENABLED   = 0b00000010

#Internal reference ebable (Enables the 2.5 V internal voltage reference. Note the IDAC and temperature sensor require the internal voltage reference.)
POWER_INTREF_DISABLED  = 0b00000000
POWER_INTREF_ENABLED   = 0b00000001



INTERFACE_ADDRESS  = 0x02
INTERFACE_DEFAULT  = 0x05

#Serial Interface Time-Out Enable (Enables the serial interface automatic time-out mode)
INTERFACE_TIMEOUT_DISABLED  = 0b00000000
INTERFACE_TIMEOUT_ENABLED   = 0b00001000

#Status  Enable (Enables the inclusion of the status  during conversion data read-back)
INTERFACE_STATUS_DISABLED  = 0b00000000
INTERFACE_STATUS_ENABLED   = 0b00000100

#Checksum  Enable (Enables the inclusion of the checksum  during conversion data read-back)
INTERFACE_CRC_DISABLED  = 0b00000000 #checksum disabled
INTERFACE_CRC_CHECKSUM  = 0b00000001 #checksum mode
INTERFACE_CRC_CRC       = 0b00000010 #Cyclic redundancy check


#Mode0 sets reference mux polarity, ADC conversion mode, chop mode and conversion delay.
MODE0_ADDRESS      = 0x03
MODE0_DEFAULT  = 0x00

#Reference Mux Polarity Reversal (Reverses the ADC1 reference multiplexer output polarity)
MODE0_REFREV_NORMALPOLARITY   = 0b00000000
MODE0_REFREV_REVERSEPOLARITY  = 0b10000000

#ADC Conversion Run Mode (Selects the ADC conversion (run) mode)
MODE0_RUNMODE_CONTINUOUS  = 0b00000000 # continuous conversion
MODE0_RUNMODE_PULSE       = 0b01000000 #one shot conversion

#Chop Mode Enable (Enables the ADC chop and IDAC rotation options)
MODE0_CHOP_DISABLED               = 0b00000000 #Input chop and IDAC rotation disabled
MODE0_CHOP_CHOPENABLED            = 0b00010000 #input chop enabled
MODE0_CHOP_IDACROTATION           = 0b00100000 #IDAC rotation enabled
MODE0_CHOP_CHOP_AND_IDACROTATION  = 0b00110000

#Conversion Delay (Provides additional delay from conversion start to the beginning of the actual conversion)
MODE0_DELAY_NONE   = 0b00000000
MODE0_DELAY_8U7S   = 0b00000001 #8.7 µs
MODE0_DELAY_17US   = 0b00000010 #17 µs
MODE0_DELAY_35US   = 0b00000011 #35 µs
MODE0_DELAY_69US   = 0b00000100 #69 µs
MODE0_DELAY_139US  = 0b00000101 #139 µs
MODE0_DELAY_278US  = 0b00000110 #278 µs
MODE0_DELAY_555US  = 0b00000111 #555 µs
MODE0_DELAY_1M1S   = 0b00001000 #1.1ms
MODE0_DELAY_2M2S   = 0b00001001 #2.2ms
MODE0_DELAY_4M4S   = 0b00001010 #4.4ms
MODE0_DELAY_8M8S   = 0b00001011 #8.8ms



# MODE1 sets the digital filter and Sensor Bias
MODE1_ADDRESS  = 0x04
MODE1_DEFAULT  = 0x80

# Digital Filter (Configures the ADC digital filter)
MODE1_FILTER_SINC1  = 0b00000000
MODE1_FILTER_SINC2  = 0b00100000
MODE1_FILTER_SINC3  = 0b01000000
MODE1_FILTER_SINC4  = 0b01100000
MODE1_FILTER_FIR    = 0b10000000 #default

#Sensor Bias ADC Connection (Selects the ADC to connect the sensor bias)
MODE1_SBADC_ADC1  = 0b00000000 #Sensor bias connected to ADC1 mux out (default)
MODE1_SBADC_ADC2  = 0b00000000 #Sensor bias connected to ADC2 mux out

#Sensor Bias Polarity Selects the sensor bias for pull-up or pull-down
MODE1_SBPOL_PULLUP    = 0b00000000 #Sensor bias pull-up mode (AINP pulled high, AINN pulled low) (default)
MODE1_SBPOL_PULLDOWN  = 0b00001000 #Sensor bias pull-down mode (AINP pulled low, AINN pulled high)

# Sensor Bias Magnitude (Selects the sensor bias current magnitude or the bias resistor)
MODE1_SBMAG_NONE   = 0b00000000 #No sensor bias current or resistor (default)
MODE1_SBMAG_500NA  = 0b00000001 #0.5-µA sensor bias current
MODE1_SBMAG_2UA    = 0b00000000 #2-µA sensor bias current
MODE1_SBMAG_10UA   = 0b00000000 #10-µA sensor bias current
MODE1_SBMAG_50UA   = 0b00000000 #50-µA sensor bias current
MODE1_SBMAG_200UA  = 0b00000000 #200-µA sensor bias current
MODE1_sbmag_10MΩ   = 0b00000000 #10-MΩ resistor



# MODE@ sets the PGA (programable gain amplifier) and the data rate
MODE2_ADDRESS  = 0x05
MODE2_DEFAULT  = 0x04

#PGA Bypass Mode Selects PGA bypass mode
MODE2_BYPASS_PGAENABLED   = 0b00000000 #default
MODE2_BYPASS_PGADISABLED  = 0b10000000

#PGA Gain - selects PGA gain
MODE2_GAIN_1   = 0b00000000 #1 V/V default
MODE2_GAIN_2   = 0b00010000 #1 V/V
MODE2_GAIN_4   = 0b00100000 #1 V/V
MODE2_GAIN_8   = 0b00110000 #1 V/V
MODE2_GAIN_16  = 0b01000000 #1 V/V
MODE2_GAIN_32  = 0b01010000 #1 V/V

#Data rate (Selects the ADC data rate. In FIR filter mode, the available data rates are limited to 2.5, 5, 10 and 20 SPS.)
MODE2_DR_2_5    = 0b00000000 #2.5 samples per second
MODE2_DR_5      = 0b00000001
MODE2_DR_10     = 0b00000010
MODE2_DR_16_6   = 0b00000011 #16.6~ samples per second
MODE2_DR_20     = 0b00000100
MODE2_DR_50     = 0b00000101
MODE2_DR_60     = 0b00000110
MODE2_DR_100    = 0b00000111
MODE2_DR_400    = 0b00001000
MODE2_DR_1200   = 0b00001001
MODE2_DR_2400   = 0b00001010
MODE2_DR_4800   = 0b00001011
MODE2_DR_7200   = 0b00001100
MODE2_DR_14400  = 0b00001101
MODE2_DR_19200  = 0b00001110
MODE2_DR_38400  = 0b00001111



#INPMUX sets the input channels for ADC1
INPMUX_ADDRESS  = 0x06
INPMUX_DEFAULT  = 0x01

#Positive Input Multiplexer (Selects the positive input multiplexer.)
INPMUX_MUXP_AIN0            = 0b00000000 #positive input is AIN0 (default)
INPMUX_MUXP_AIN1            = 0b00010000 #positive input is AIN1
INPMUX_MUXP_AIN2            = 0b00100000 #positive input is AIN1
INPMUX_MUXP_AIN3            = 0b00110000 #positive input is AIN3
INPMUX_MUXP_AIN4            = 0b01000000 #positive input is AIN4
INPMUX_MUXP_AIN5            = 0b01010000 #positive input is AIN5
INPMUX_MUXP_AIN6            = 0b01100000 #positive input is AIN6
INPMUX_MUXP_AIN7            = 0b01110000 #positive input is AIN7
INPMUX_MUXP_AIN8            = 0b10000000 #positive input is AIN8
INPMUX_MUXP_AIN9            = 0b10010000 #positive input is AIN9
INPMUX_MUXP_AINCOM          = 0b10100000 #positive input is AINCOM
INPMUX_MUXP_TEMPSENSORP     = 0b10110000 #Temperature sensor monitor positive
INPMUX_MUXP_ANALOGSUPPLYP   = 0b11000000 #Analog power supply monitor positive
INPMUX_MUXP_DIGITALSUPPLYP  = 0b11010000 #Digital power supply monitor positive
INPMUX_MUXP_TDACP           = 0b11100000 #TDAC test signal positive
INPMUX_MUXP_FLOAT           = 0b11110000 #Float (open connection)

INPMUX_MUXN_AIN0            = 0b00000000 #negative input is AIN0
INPMUX_MUXN_AIN1            = 0b00000001 #negative input is AIN1 (default)
INPMUX_MUXN_AIN2            = 0b00000010 #negative input is AIN2
INPMUX_MUXN_AIN3            = 0b00000011 #negative input is AIN3
INPMUX_MUXN_AIN4            = 0b00000100 #negative input is AIN4
INPMUX_MUXN_AIN5            = 0b00000101 #negative input is AIN5
INPMUX_MUXN_AIN6            = 0b00000110 #negative input is AIN6
INPMUX_MUXN_AIN7            = 0b00000111 #negative input is AIN7
INPMUX_MUXN_AIN8            = 0b00001000 #negative input is AIN8
INPMUX_MUXN_AIN9            = 0b00001001 #negative input is AIN9
INPMUX_MUXN_AINCOM          = 0b00001010 #negative input is AINCOM
INPMUX_MUXN_TEMPSENSORN     = 0b00001011 #Temperature sensor monitor negative
INPMUX_MUXN_ANALOGSUPPLYN   = 0b00001100 #Analog power supply monitor negative
INPMUX_MUXN_DIGITALSUPPLYN  = 0b00001101 #Digital power supply monitor negative
INPMUX_MUXN_TDACP           = 0b00001110 #TDAC test signal negative
INPMUX_MUXN_FLOAT           = 0b00001111 #Float (open connection)



#Offset calibration register - Use calibration to correct internal ADC errors or overall system errors. the value of the offset calibration register is subtracted from the filter output and then multiplied by the full-scale register value divided by 400000h. The data are then clipped to a 32-bit value to provide the final output. (see section 9.4.9 of the datasheet for more information)
OFCAL0_ADDRESS  = 0x07
OFCAL1_ADDRESS  = 0x08
OFCAL2_ADDRESS  = 0x09



#Full-scale calibration register - Use calibration to correct internal ADC errors or overall system errors. the value of the offset calibration register is subtracted from the filter output and then multiplied by the full-scale register value divided by 400000h. The data are then clipped to a 32-bit value to provide the final output. (see section 9.4.9 of the datasheet for more information)
FSCAL0_ADDRESS  = 0x0A
FSCAL1_ADDRESS  = 0x0B
FSCAL2_ADDRESS  = 0x0C


#IDAC Multiplexer register - selects analog input pins to connect to IDAC1 and IDAC2 (IDAC refers to current sources)
IDACMUX_ADDRESS  = 0x0D
IDACMUX_DEFAULT  = 0xBB



#IDAC2 Output Multiplexer Selects the analog input pin to connect IDAC2
IDACMUX_MUX2_AIN0    = 0b00000000 #IDAC2 output is AIN0
IDACMUX_MUX2_AIN1    = 0b00010000 #IDAC2 output is AIN1
IDACMUX_MUX2_AIN2    = 0b00100000 #IDAC2 output is AIN1
IDACMUX_MUX2_AIN3    = 0b00110000 #IDAC2 output is AIN3
IDACMUX_MUX2_AIN4    = 0b01000000 #IDAC2 output is AIN4
IDACMUX_MUX2_AIN5    = 0b01010000 #IDAC2 output is AIN5
IDACMUX_MUX2_AIN6    = 0b01100000 #IDAC2 output is AIN6
IDACMUX_MUX2_AIN7    = 0b01110000 #IDAC2 output is AIN7
IDACMUX_MUX2_AIN8    = 0b10000000 #IDAC2 output is AIN8
IDACMUX_MUX2_AIN9    = 0b10010000 #IDAC2 output is AIN9
IDACMUX_MUX2_AINCOM  = 0b10100000 #IDAC2 output is AINCOM
IDACMUX_MUX2_NONE    = 0b10110000 #No connection (default)



#IDAC1 Output Multiplexer Selects the analog input pin to connect IDAC1
IDACMUX_MUX1_AIN0    = 0b00000000 #IDAC1 output is AIN0
IDACMUX_MUX1_AIN1    = 0b00000001 #IDAC1 output is AIN1
IDACMUX_MUX1_AIN2    = 0b00000010 #IDAC1 output is AIN2
IDACMUX_MUX1_AIN3    = 0b00000011 #IDAC1 output is AIN3
IDACMUX_MUX1_AIN4    = 0b00000100 #IDAC1 output is AIN4
IDACMUX_MUX1_AIN5    = 0b00000101 #IDAC1 output is AIN5
IDACMUX_MUX1_AIN6    = 0b00000110 #IDAC1 output is AIN6
IDACMUX_MUX1_AIN7    = 0b00000111 #IDAC1 output is AIN7
IDACMUX_MUX1_AIN8    = 0b00001000 #IDAC1 output is AIN8
IDACMUX_MUX1_AIN9    = 0b00001001 #IDAC1 output is AIN9
IDACMUX_MUX1_AINCOM  = 0b00001010 #IDAC1 output is AINCOM
IDACMUX_MUX1_NONE    = 0b00001011 #No connection (default)



#IDAC magnitude register (IDAC refers to current sources)
IDACMAG_ADDRESS  = 0x0E
IDACMAG_DEFAULT  = 0x00
#IDAC2 Output Multiplexer Selects the analog input pin to connect IDAC2
IDACMAG_MAG2_OFF   = 0b00000000 #IDAC2 is off (default)
IDACMAG_MAG2_50    = 0b00010000 #IDAC2 output is 50 µA
IDACMAG_MAG2_100   = 0b00100000 #IDAC2 output is 100 µA
IDACMAG_MAG2_250   = 0b00110000 #IDAC2 output is 250 µA
IDACMAG_MAG2_500   = 0b01000000
IDACMAG_MAG2_750   = 0b01010000
IDACMAG_MAG2_1000  = 0b01100000
IDACMAG_MAG2_1500  = 0b01110000
IDACMAG_MAG2_2000  = 0b10000000
IDACMAG_MAG2_3000  = 0b10010000

#IDAC1 Output Multiplexer Selects the analog input pin to connect IDAC1
IDACMAG_MAG1_OFF   = 0b00000000 #IDAC1 is off
IDACMAG_MAG1_50    = 0b00000001 #IDAC1 output is 50 µA
IDACMAG_MAG1_100   = 0b00000010 #IDAC1 output is 100 µA
IDACMAG_MAG1_250   = 0b00000011 #IDAC1 output is 250 µA
IDACMAG_MAG1_500   = 0b00000100
IDACMAG_MAG1_750   = 0b00000101
IDACMAG_MAG1_1000  = 0b00000110
IDACMAG_MAG1_1500  = 0b00000111
IDACMAG_MAG1_2000  = 0b00001000
IDACMAG_MAG1_2500  = 0b00001001
IDACMAG_MAG1_3000  = 0b00001010



#Reference multiplexer register - selects reference inputs
REFMUX      = 0x0F
REFMUX_ADDRESS  = 0x0F
REFMUX_DEFAULT  = 0x00
#Reference Positive Input (Selects the positive reference input)
REFMUX_RMUXP_INTERNALREF    = 0b00000000 #Internal 2.5 V reference - P (default)
REFMUX_RMUXP_AIN0           = 0b00001000 #External AIN0
REFMUX_RMUXP_AIN2           = 0b00010000
REFMUX_RMUXP_AIN4           = 0b00011000
REFMUX_RMUXP_INTERNALVAVDD  = 0b00100000 # Internal analog supply (VAVDD )
#Reference Negative Input (Selects the negative reference input)
REFMUX_RMUXN_INTERNALREF    = 0b00000000 #Internal 2.5 V reference - N (default)
REFMUX_RMUXN_AIN1           = 0b00000001 #External AIN1
REFMUX_RMUXN_AIN3           = 0b00000010
REFMUX_RMUXN_AIN5           = 0b00000011
REFMUX_RMUXP_INTERNALVAVSS  = 0b00000100 #Internal analog supply (VAVSS)




#TDACP control register - Test DAC (positive)
TDACP_ADDRESS  = 0x10
TDACP_DEFAULT  = 0x00
# TDACP Output Connection (Connects TDACP output to pin AIN6)
TDACP_OUTP_NONE  = 0b00000000
TDACP_OUTP_AIN6  = 0b10000000
# MAGP Output Magnitude Select the TDACP output magnitude. (The TDAC output voltages are ideal and are with respect to VAVSS)
TDACP_MAGP_4_5        = 0b00001001 # 4.5 V
TDACP_MAGP_3_5        = 0b00001000 # 3.5 V
TDACP_MAGP_3          = 0b00000111 # 3 V
TDACP_MAGP_2_75       = 0b00000110 # 2.75 V
TDACP_MAGP_2_625      = 0b00000101 # 2.625 v
TDACP_MAGP_2_5626     = 0b00000100 # 2.5625 V
TDACP_MAGP_2_53125    = 0b00000011 # 2.53125 V
TDACP_MAGP_2_515625   = 0b00000010 # 2.515625 V
TDACP_MAGP_2_5078125  = 0b00000001 # 2.5078125 V
TDACP_MAGP_2_5        = 0b00000000 # 2.5 V
TDACP_MAGP_2_4921875  = 0b00010001 # 2.4921875 V
TDACP_MAGP_2_484375   = 0b00010010 # 2.484375 V
TDACP_MAGP_2_46875    = 0b00010011 # 2.46875 V
TDACP_MAGP_2_4375     = 0b00010100 # 2.4375 V
TDACP_MAGP_2_375      = 0b00010101 # 2.375 V
TDACP_MAGP_2_25       = 0b00010110 # 2.25 V
TDACP_MAGP_2          = 0b00010111 # 2 V
TDACP_MAGP_1_5        = 0b00011000 # 1.5 V
TDACP_MAGP_0_5        = 0b00011001 # 0.5 V




#TDACN control register - Test DAC (negative)
TDACN_ADDRESS  = 0x11
TDACN_DEFAULT  = 0x00
# TDACN Output Connection (Connects TDACN output to pin AIN6)
TDACN_OUTN_NONE  = 0b00000000
TDACN_OUTN_AIN7  = 0b10000000
# MAGN Output Magnitude Select the TDACN output magnitude. (The TDAC output voltages are ideal and are with respect to VAVSS)
TDACN_MAGN_4_5        = 0b00001001 # 4.5 V
TDACN_MAGN_3_5        = 0b00001000 # 3.5 V
TDACN_MAGN_3          = 0b00000111 # 3 V
TDACN_MAGN_2_75       = 0b00000110 # 2.75 V
TDACN_MAGN_2_625      = 0b00000101 # 2.625 v
TDACN_MAGN_2_5626     = 0b00000100 # 2.5625 V
TDACN_MAGN_2_53125    = 0b00000011 # 2.53125 V
TDACN_MAGN_2_515625   = 0b00000010 # 2.515625 V
TDACN_MAGN_2_5078125  = 0b00000001 # 2.5078125 V
TDACN_MAGN_2_5        = 0b00000000 # 2.5 V
TDACN_MAGN_2_4921875  = 0b00010001 # 2.4921875 V
TDACN_MAGN_2_484375   = 0b00010010 # 2.484375 V
TDACN_MAGN_2_46875    = 0b00010011 # 2.46875 V
TDACN_MAGN_2_4375     = 0b00010100 # 2.4375 V
TDACN_MAGN_2_375      = 0b00010101 # 2.375 V
TDACN_MAGN_2_25       = 0b00010110 # 2.25 V
TDACN_MAGN_2          = 0b00010111 # 2 V
TDACN_MAGN_1_5        = 0b00011000 # 1.5 V
TDACN_MAGN_0_5        = 0b00011001 # 0.5 V




GPIOCON     = 0x12
GPIODIR     = 0x13
GPIODAT     = 0x14
ADC2CFG     = 0x15
ADC2MUX     = 0x16
ADC2OFC0    = 0x17
ADC2OFC1    = 0x18
ADC2FSC0    = 0x19
ADC2FSC1    = 0x1A




