# piadcs
A python package for interfacing a Raspberry Pi with TI ADCs (currently only supports ADS126x 32 bit ADC)

## How to install
There are different ways to install this package. The most straightforward is installing directly from the github repository.
```bash
pip3 install git+https://github.com/AnnaKnapp/python_piadcs.git
```

Alternatively you can download the piadcs-0.1.0.tar.gz file located in the dist folder of this repository. To install from a tar.gz use the following command
```bash
pip3 install piadcs-0.1.0.tar.gz
```
## How to use
Import the main library and the subfolder with the library for the adc you want to use (at this time only the ads126x is supported)

```python
import piadcs
from piadcs import ads126x as adc
```
Please check out the examples folder for usage examples. These examples are intended to run on a Raspberry Pi running Raspberry Pi OS and assume the connections shown in the schematics folder. The testing was done using a ProtoCentral ADS126x breakout board and a Raspberry Pi 4 B (other Pi models should also work). 

These examples demonstrate how to use the functions provided by the library to change the ADC settings by writing to the registers, how to read conversion data, and how to store it as a .csv file.

## Documentation
Full documentation can be found here:
https://annaknapp.github.io/python_piadcs/
