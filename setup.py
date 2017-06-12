from setuptools import setup

setup(
    name='kraken',
    packages=['kraken'],
    scripts=['bin/colctl'],
    install_requires=['pyusb'],
)
