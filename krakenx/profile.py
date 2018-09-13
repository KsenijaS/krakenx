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

def normalize(profile, critx):
  """Normalize a [(x:int, y:int), ...] profile.

  The normalized profile will ensure that:

   - the profile is a monotonically increasing function
     (i.e. for every i, i > 1, x[i] - x[i-1] > 0 and y[i] - y[i-1] >= 0)
   - the profile is sorted
   - a (critx, 100) failsafe is enforced

  >>> normalize([(30, 40), (25, 25), (35, 30), (40, 35), (40, 80)], 60)
  [(25, 25), (30, 40), (35, 40), (40, 80), (60, 100)]
  """
  profile = sorted(list(profile) + [(critx, 100)], key=lambda p: (p[0], -p[1]))
  mono = profile[0:1]
  for (x, y), (xb, yb) in zip(profile[1:], profile[:-1]):
    if x == xb:
      continue
    if y < yb:
      y = yb
    mono.append((x, y))
  return mono

def interpolate(profile, x):
  """Interpolate y given x and a [(x: int, y: int), ...] profile.

  Requires the profile to be sorted by x, with no duplicate x values (see
  normalize).  Expects profiles with integer x and y values, and
  returns duty rounded to the nearest integer.

  >>> interpolate([(20, 50), (50, 70), (60, 100)], 33)
  59
  >>> interpolate([(20, 50), (50, 70)], 19)
  50
  >>> interpolate([(20, 50), (50, 70)], 51)
  70
  >>> interpolate([(20, 50)], 20)
  50
  """
  lower, upper = profile[0], profile[-1]
  for step in profile:
    if step[0] <= x:
      lower = step
    if step[0] >= x:
      upper = step
      break
  if lower[0] == upper[0]:
    return lower[1]
  return round(lower[1] + (x - lower[0])/(upper[0] - lower[0])*(upper[1] - lower[1]))

