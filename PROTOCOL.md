#Reverse engineered protocol of the NZXT Kraken X52

##Message

**Messages sent by the host**

The 1st byte of the message is always 0x02
The 2nd and 3rd byte of the message represents the message type:

| Type     |   Description   |
|----------|-----------------|
|0x4c 0x00 |      Color      |
|0x4d 0x00 |    Fan speed    |
|0x4d 0x40 |   Pump speed    |


**Color message**

|   Byte   |   Meaning   |
|----------|-------------|
|    0     |     0x02    |
|   1-2    | Type: color |
|   3-4    | Color mode  |
|   5-7    | Text color  |
|   8-10   |   Color 0   |
|  11-13   |   Color 1   |
|  14-16   |   Color 2   |
|  17-19   |   Color 3   |
|  20-22   |   Color 4   |
|  23-25   |   Color 5   |
|  26-28   |   Color 6   |
|  29-31   |   Color 7   |

Text color represents led in the middle that controls lighting of letters NZXT,
Color 0-7 are leds on the rim. Each of these leds can be controled separately.
Note: Text color is written in grb format (except in Spectrum Wave mode),
whereas colors 0-7 have rgb format.

There are 7 color modes:

| Color mode |  Description  |
|------------|---------------|
| 0x00 0x02  |    Solid      |
| 0x06 0x02  |   Breathing   |
| 0x07 0x02  |     Pulse     |
| 0x01 0x02  |    Fading     |
| 0x04 0x02  |CoveringMarquee|
| 0x02 0x01  | SpectrumWave  |

CAM software only lets users set the same color for all 9 leds, but it's
possible to set a different color for each of the 9 leds separately. I created
the Solid All mode to use this capability, but in terms of protocol, Solid
All is the same as Solid.

Modes Breathing, Pulse, Fading, and Covering Marquee can use up to 8 different
colors. CAM software sends one message to the device per color set. The highest
3 bits of the 2nd byte of the mode denotes the index of the color being set in
that message.

For example, if three colors are being set for Breathing mode, the host is
sending three messages where the 2nd byte of the Breathing mode is:
1st message: 0x06 0x02
2nd message: 0x06 0x22
3rd message: 0x06 0x42

**Fan speed message**

|   Byte   |    Meaning   |
|----------|--------------|
|    0     |     0x02     |
|   1-2    |Type:fan speed|
|    3     |     0x00     |
|    4     |  fan speed   |

**Pump speed message**

|   Byte   |    Meaning    |
|----------|---------------|
|    0     |     0x02      |
|   1-2    |Type:pump speed|
|    3     |     0x00      |
|    4     |  pump speed   |
