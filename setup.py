from setuptools import setup

setup(
    name='krakenx',
    version='0.0.1',
    packages=['krakenx'],
    scripts=['bin/colctl'],
    install_requires=['pyusb'],
)
