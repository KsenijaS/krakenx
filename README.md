# NZXT-cooler
Python script to control NZXT cooler KrakenX52/X62 in Linux and Windows.

## Supported devices:

- NZXT Kraken X52/X62 (Vendor/Product ID: 0x1e71:0x170e)

Note: It's possible that other devices are supported as well

## Linux installation:

sudo python3 -m pip install krakenx

## Windows installation

Install libusb or libusbK device driver for the NZXT USB device. [Zadig](http://zadig.akeo.ie/) is a tool to accomplish this. Select "Options -> List All Devices", select your NZXT device, change target driver to libusb-win32 or libusbK and install the driver. CAM software will not detect the device after this. See [libwdi FAQ](https://github.com/pbatard/libwdi/wiki/FAQ#Help_Zadig_replaced_the_driver_for_the_wrong_device_How_do_I_restore_it) for uninstallation instructions.

Now krakenx can be installed using PIP:

pip install krankenx

## Usage:

There are 8 separate LEDs on the rim, and text color is controlled separately
too. There are 7 different color modes: Solid, SolidAll, Breathing, Pulse,
Fading, CoveringMarquee, SpectrumWave which are controled via command line flag
--mode.

Control lights using --mode, --animation_speed, --color_count, --color0,
--color1, ... --color7, as well as --text_color.

Depending on mode, different flags are used:

**Solid**

Only use flag color0, if not set it will have default color(red), example:
sudo colctl --mode solid --color0 50,0,90

**Solid All**

Use flags text color and color 0-7, colors that are not set will have default
color (red), example: sudo colctl --mode solidall -text_color 0,255,0 -c0
50,0,90 -c1 40,50,60

**Breathing, Pulse, Fading, Covering Marquee**

Set flags color0-7 and color_count. Flag color_count needs only to be set when
there is more than one color flag and it represents number of colors being
used, example: sudo colctl --mode fading --color0 50,0,90 --color1 56,98,0
--color2 20,20,20 --color3 0,90,90 --color_count 4

**Spectrum Wave**

Only use flag animation_speed, if flag is not set it will have default value
(0). Example: sudo colctl --mode spectrumwave --animation_speed 3

Pump speed and fan speed are controled via --pump_speed and --fan_speed modes,
but I could not verify that the flag works because I can't read fan and pump
speed on my AMD B350 motherboard. If flags are not set, pump speed will have
default value of 60% and fan speed 30%. 

See also colctl --help

Note: Solid and Solid All mode settings are not remembered after restart, I
think that is due to the firmware bug.
