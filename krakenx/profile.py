from ast import literal_eval

def parse(arg, minduty, maxduty, maxtemp):
  """Parse and validate duty profiles or fixed values.

  >>> parse('(20,30),(30,50),(34,80),(40,90),(50,100)', 25, 100, 59)
  [(20, 30), (30, 50), (34, 80), (40, 90), (50, 100)]
  >>> parse('35', 25, 100, 59)
  [(0, 35), (59, 35)]

  Because of how Kraken52 initializes and validates values in different places,
  this function can be called with already parsed profiles; in those cases,
  only validation is perfomed.

  >>> parse([(20, 30), (50, 100)], 25, 100, 59)
  [(20, 30), (50, 100)]
  >>> parse([(0, 35), (59, 35)], 25, 100, 59)
  [(0, 35), (59, 35)]

  The profile is validated in structure and acceptable ranges.  Duty is checked
  against `minduty`  and `maxduty`.  Liquid temperature must be between 0°C and
  `maxtemp`.

  >>> parse('(20,30),(50,100', 25, 100, 59)
  Traceback (most recent call last):
    ...
  ValueError: Profile must be comma-separated (temperature, duty) tuples
  >>> parse('(20,30),(50,100,2)', 25, 100, 59)
  Traceback (most recent call last):
    ...
  ValueError: Profile must be comma-separated (temperature, duty) tuples
  >>> parse('(20,30),(50,97.6)', 25, 100, 59)
  Traceback (most recent call last):
    ...
  ValueError: Duty must be integer number between 25 and 100
  >>> parse('(20,15),(50,100)', 25, 100, 59)
  Traceback (most recent call last):
    ...
  ValueError: Duty must be integer number between 25 and 100
  >>> parse('(20,30),(70,100)', 25, 100, 59)
  Traceback (most recent call last):
    ...
  ValueError: Liquid temperature must be integer number between 0 and 59
  """
  generror = ValueError("Profile must be comma-separated (temperature, duty) tuples")
  if isinstance(arg, str):
    try:
      val = literal_eval('[' + arg + ']')
      if len(val) == 1 and isinstance(val[0], int):
        # for arg == '<number>' set fixed duty between 0 and 59 °C
        val = [(0, val[0]), (59, val[0])]
    except:
      raise generror
  elif isinstance(arg, int):
    val = [(0, arg), (59, arg)]
  elif isinstance(arg, list):
    val = arg
  else:
    raise generror
  for step in val:
    if not isinstance(step, tuple) or len(step) != 2:
      raise generror
    temp, duty = step
    if not isinstance(temp, int) or temp < 0 or temp > maxtemp:
      raise ValueError("Liquid temperature must be integer number between 0 and {}".format(maxtemp))
    if not isinstance(duty, int) or duty < minduty or duty > maxduty:
      raise ValueError('Duty must be integer number between {} and {}'.format(minduty, maxduty))
  return val

