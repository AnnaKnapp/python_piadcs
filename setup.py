import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="pyADS1262",
    version="0.1.0",
    description="A python package for interfacing the ADS1262 32-bit ADC with a Raspberry Pi",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/AnnaKnapp/pyADS1262",
    author="Anna Knapp",
    author_email="aknapp01@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["."],
    include_package_data=True,
    install_requires=["spidev", "RPi.GPIO"],
)