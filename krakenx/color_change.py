#!/usr/bin/python3
from collections import namedtuple
import sys
import usb.core
import itertools

VENDOR = 0x1e71
PRODUCT = 0x170e

class KrakenX52:

  DEFAULT_COLOR = (255, 0, 0)

  Mode = namedtuple('Mode', ['name','mode'])
  MODE_SOLID = Mode('Solid', (0, 2))
  MODE_SOLID_ALL = Mode('SolidAll', (0, 2))
  MODE_BREATHING = Mode('Breathing', (6, 2))
  MODE_PULSE = Mode('Pulse', (7, 2))
  MODE_FADING = Mode('Fading', (1, 2))
  MODE_COVERING_MARQUEE = Mode('CoveringMarquee', (4, 2))
  MODE_SPECTRUM_WAVE = Mode('SpectrumWave', (2, 1))
  COLOR_MODES = [MODE_SOLID, MODE_SOLID_ALL, MODE_BREATHING, MODE_PULSE,
		 MODE_FADING, MODE_COVERING_MARQUEE, MODE_SPECTRUM_WAVE]

  @classmethod
  def _check_color(cls, color):
    if len(color) != 3 or not all(
       [isinstance(c, int) and c >= 0 and c <= 255 for c in color]):
        raise ValueError("colors must be tuples of 3 int between 0 and 255")

  @classmethod
  def _flatten(cls, *args):
    return list(itertools.chain(*args))

  @classmethod
  def _grb_color(cls, color):
    return (color[1], color[0], color[2])

  def _validate(self):
    if self._mode not in self.COLOR_MODES:
      raise ValueError("color mode must be one of {}".format(self.COLOR_MODES))

    if self._aspeed < 0 or self._aspeed > 4 or not isinstance(self._aspeed, int):
      raise ValueError("Animation speed must be integer number between 0 and 4")

    if self._fspeed < 25 or self._fspeed > 100 or not isinstance(self._fspeed, int):
      raise ValueError("Fan speed must be integer number between 25 and 100")

    if self._pspeed < 60 or self._pspeed > 100 or not isinstance(self._pspeed, int):
      raise ValueError("Pump speed must be integer number between 60 and 100")

    self._check_color(self._text_color)

    for j in range(self._color_count):
      self._check_color(self._colors[j])


  def __init__(self, dev, **kwargs):
    self.dev = dev

    self._mode = kwargs.pop('mode', self.MODE_SOLID)

    self._text_color = kwargs.pop('text_color', self.DEFAULT_COLOR)

    self._colors = []
    for i in range(8):
      self._colors.insert(i, kwargs.pop('color' + str(i), self.DEFAULT_COLOR))

    self._color_count = kwargs.pop('color_count', 1)

    self._aspeed = kwargs.pop('aspeed', 0)

    self._fspeed = kwargs.pop('fspeed', 30)

    self._pspeed = kwargs.pop('pspeed', 60)

  def _mode_bytes(self, i=0):
    # set the higher 3 bits of the 2rd byte to denote the number of colors being set
    return (self._mode.mode[0], self._mode.mode[1] + 16 * (i) * 2)

  def _mode_speed(self):
    return (self._mode.mode[0], self._aspeed)

  def _send_pump_speed(self):
    self.dev.write(0x01, [0x02, 0x4d, 0x40, 0x00, self._pspeed])

  def _send_fan_speed(self):
    self.dev.write(0x01, [0x02, 0x4d, 0x00, 0x00, self._fspeed])

  def _send_color(self):
    if self._mode==self.MODE_SOLID:
      color = self._colors[0]
      self.dev.write(0x01, KrakenX52._flatten(
        [0x02, 0x4c, 0x00],
        self._mode_bytes(),
        self._grb_color(self._colors[0]),
        *itertools.repeat(color, 8)))
    elif self._mode==self.MODE_SOLID_ALL:
      self.dev.write(0x01, KrakenX52._flatten(
		[0x02, 0x4c, 0x00],
		self._mode_bytes(),
		self._grb_color(self._text_color),
		*self._colors))
    elif self._mode==self.MODE_SPECTRUM_WAVE:
      self.dev.write(0x01, KrakenX52._flatten(
		[0x02, 0x4c, 0x00],
		self._mode_speed(),
		*itertools.repeat(self.DEFAULT_COLOR, 9)))
    elif self._mode in [
      self.MODE_FADING,
      self.MODE_COVERING_MARQUEE,
      self.MODE_PULSE,
      self.MODE_BREATHING]:
      for i in range(self._color_count):
        self.dev.write(0x01, KrakenX52._flatten(
		  [0x02, 0x4c, 0x00],
		  self._mode_bytes(i),
		  self._grb_color(self._colors[i]),
		  *itertools.repeat(self._colors[i], 8)))
    else:
      raise Exception("!")

  def update(self):
    self._validate()
    self._send_color()
    self._send_fan_speed()
    self._send_pump_speed()
