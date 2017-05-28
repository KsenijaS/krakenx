# NZXT-cooler
Python script to control NZXT cooler KrakenX52 in Linux

Supported devices:
 NZXT Kraken X52
 
Usage:
There are 8 separate LEDs on the rim, and text color is controlled separately too. There are 7 different color modes:
Solid, SolidAll, Breathing, Pulse, Fading, CoveringMarquee, SpectrumWave which are controled via command line flag --mode.
Control lights using --mode, --animation_speed, --color_count, --color0, --color1, ... --color7, as well as --text_color.
 Example:
 sudo python3 colctl --mode solidall --color0 50,0,90 --color1 56,98,0 --color2 20,20,20 --color3 0,90,90 --color_count 4
