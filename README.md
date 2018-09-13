# NZXT-cooler
Python script to control NZXT cooler Kraken X52/X62/X72 in Linux and Windows.

## Supported devices:

- NZXT Kraken X52/X62/X72 (Vendor/Product ID: 0x1e71:0x170e)

Note: It's possible that other devices are supported as well

## Python pip note:

The public Python pip package installed with the pip install command might be outdated. You can check the [pip release history](https://pypi.org/project/krakenx/#history) and [Install from source](#install-from-source) if a newer version is required.

## Linux installation:

`sudo python3 -m pip install krakenx`

## Windows installation

Install libusb or libusbK device driver for the NZXT USB device. [Zadig](http://zadig.akeo.ie/) is a tool to accomplish this. Select "Options -> List All Devices", select your NZXT device, change target driver to libusb-win32 or libusbK and install the driver. CAM software will not detect the device after this. See [libwdi FAQ](https://github.com/pbatard/libwdi/wiki/FAQ#Help_Zadig_replaced_the_driver_for_the_wrong_device_How_do_I_restore_it) for uninstallation instructions.

Now krakenx can be installed using PIP (use Python 3, no adminstrative privileges required):

`python -m pip install krakenx`

`colctl` works with user privileges. Other accounts may need `PATH` updates for Python main and script folders in system environment (only available in user environment by default).

The `colctl` command might only work in a Unix shell like git bash. Use `colctl.py` in Windows command line environments instead which just redirects your command.

## Install from source

From cloned project source folder execute (use `sudo` on Linux, user account on Windows):  
`python -m pip install -e .`

To uninstall use:
`python -m pip uninstall krakenx`

## Usage:

Use `sudo` on Linux. Use `colctl.py` instead of `colctl` in Windows command line environment without Unix support.

There are 8 separate LEDs on the rim, and text color is controlled separately
too. There are 7 different color modes: Solid, SolidAll, Breathing, Pulse,
Fading, CoveringMarquee, SpectrumWave which are controled via command line flag
`--mode`.

Control lights using `--mode`, `--animation_speed`, `--color_count`, `--color0`,
`--color1`, ... `--color7`, as well as `--text_color`.

Depending on mode, different flags are used:

**Solid**

Only use flag color0, if not set it will have default color(red), example:  
`colctl --mode solid --color0 50,0,90`

**Solid All**

Use flags text_color and color0-7, colors that are not set will have default
color (red), example:  
`colctl --mode solidall --text_color 0,255,0 -c0 50,0,90 -c1 40,50,60`

**Breathing, Pulse, Fading, Covering Marquee**

Set flags text_color, animation_speed, color0-7 and color_count. If text_color
is not set, the current animation color will be used as text color.
Flag color_count needs only to be set when there is more than one color flag
and it represents number of colors being used, example:  
`colctl --mode fading --color0 50,0,90 --color1 56,98,0 --color2 20,20,20 --color3 0,90,90 --color_count 4`

**Marquee, Police, Spinner**

Set flags color0-1 and color count. Text color is always black. Examples:  
`colctl --mode spinner --color0 9,33,71 --color1 2,7,15 --color_count 2 --animation_speed 2`  
`colctl --mode marquee --color0 9,33,71 --color1 2,7,15 --color_count 2 --animation_speed 0`

**Chaser**

Color flags are ignored. Called "Tai Chi" in CAM software.

**Spectrum Wave**

Only use flag animation speed, if flag is not set it will have default value
(0). Example:  
`colctl --mode spectrumwave --animation_speed 3`

**Fan and pump speeds**

Fan and pump speeds can be controled via the `--fan_speed` and `--pump_speed`
options.  They are always set in duty percentages (multiplied by 100), and can
either be fixed values (by passing a single integer number) or profiles
depending on liquid temperatue (by passing multiple comma-separated
`(<temperature>, <speed>)` tuples).

```
colctl --fan_speed 50 --pump_speed 60 [...]
colctl --fan_speed "(20,30),(30,50),(40,90),(45,100)" [...]
```

If either flag is not set, a default profile will be applied in its place.

---

See also `colctl --help`

Note: Solid and Solid All mode settings are not remembered after restart, I
think that is due to the firmware bug.

