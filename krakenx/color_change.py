#!/usr/bin/python3
from collections import namedtuple
from krakenx import profile
from liquidctl.driver.kraken_two import KrakenTwoDriver

VENDOR = 0x1e71
PRODUCT = 0x170e
CRITICAL_TEMP = 60

class KrakenX52(KrakenTwoDriver):

  DEFAULT_COLOR = (255, 0, 0)

  Mode = namedtuple('Mode', ['name', 'lname', 'uses_text_color'])
  MODE_SOLID = Mode('Solid', 'fixed', False)
  COLOR_MODES = [
    Mode('Off', 'off', False),
    MODE_SOLID,
    Mode('SolidAll', 'super-fixed', True),
    Mode('Fading', 'fading', False),
    Mode('SpectrumWave', 'spectrum-wave', False),
    Mode('CustomWave', 'super-wave', True),
    Mode('Marquee', 'marquee-3', False),
    Mode('CoveringMarquee', 'covering-marquee', False),
    Mode('Alternating', 'alternating', False),
    Mode('MovingAlternating', 'moving-alternating', False),
    Mode('Breathing', 'breathing', False),
    Mode('CustomBreathing', 'super-breathing', True),
    Mode('Pulse', 'pulse', False),
    Mode('Chaser', 'tai-chi', False),
    Mode('Spinner', 'water-cooler', False),
    Mode('Loading', 'loading', False),
    Mode('Police', 'wings', False),
  ]
  COLOR_CHANNELS = {'Both': 'sync', 'Ring': 'ring', 'Text': 'logo'}

  @classmethod
  def _check_color(cls, color):
    if len(color) != 3 or not all(
       [isinstance(c, int) and c >= 0 and c <= 255 for c in color]):
        raise ValueError("colors must be tuples of 3 int between 0 and 255")

  @classmethod
  def _build_msg(cls, *args):
    payload = list(itertools.chain(*args))
    return payload + [0]*(65 - len(payload))

  @classmethod
  def _grb_color(cls, color):
    return (color[1], color[0], color[2])

  def _validate(self):
    if self._mode not in self.COLOR_MODES:
      raise ValueError("color mode must be one of {}".format(self.COLOR_MODES))
    if not self._color_channel in self.COLOR_CHANNELS:
      raise ValueError("color channel must be one of {}".format(self.COLOR_CHANNELS.keys()))
    if self._aspeed < 0 or self._aspeed > 4 or not isinstance(self._aspeed, int):
      raise ValueError("Animation speed must be integer number between 0 and 4")
    self._fspeed = profile.parse(self._fspeed, 25, 100, CRITICAL_TEMP - 1)
    self._pspeed = profile.parse(self._pspeed, 50, 100, CRITICAL_TEMP - 1)
    self._check_color(self._text_color)
    for j in range(self._color_count):
      self._check_color(self._colors[j])

  def __init__(self, dev, **kwargs):
    super(KrakenX52, self).__init__(dev, 'NZXT Kraken X42/X52/X62/X72')
    self._mode = kwargs.pop('mode', self.MODE_SOLID)
    self._color_channel = kwargs.pop('color_channel')
    self._text_color = kwargs.pop('text_color', self.DEFAULT_COLOR)
    self._colors = []
    for i in range(8):
      self._colors.insert(i, kwargs.pop('color' + str(i), self.DEFAULT_COLOR))
    self._color_count = kwargs.pop('color_count', 1)
    self._aspeed = kwargs.pop('aspeed', 0)
    self._fspeed = kwargs.pop('fspeed')
    self._pspeed = kwargs.pop('pspeed')
    self.dev = dev

  def _send_pump_speed(self):
    self.set_speed_profile('pump', self._pspeed)

  def _send_fan_speed(self):
    self.set_speed_profile('fan', self._fspeed)

  def _send_color(self):
    lchannel = self.COLOR_CHANNELS[self._color_channel]
    lcolors = self._colors[0:self._color_count]
    if self._mode.uses_text_color:
      lcolors.insert(0, self._text_color)
    lspeed = ['slowest', 'slower', 'normal', 'faster', 'fastest'][self._aspeed]
    self.set_color(lchannel, self._mode.lname, lcolors, lspeed)

  def print_status(self):
    print("Device status:")
    for key, value, unit in sorted(self.get_status()):
      print(key.lower().replace(' ', '_'), value)

  def update(self):
    self._validate()
    self._send_color()
    self._send_fan_speed()
    self._send_pump_speed()

