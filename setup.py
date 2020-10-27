from setuptools import setup

setup(
    name='krakenx',
    version='0.0.3',
    packages=['krakenx'],
    scripts=['bin/colctl', 'bin/colctl.py'],
    install_requires=['liquidctl>=1.2.0'],
)
