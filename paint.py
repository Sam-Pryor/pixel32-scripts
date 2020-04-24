import PixelKit as kit
from time import sleep

hue = True;
temp_percent = 0
position_x = 1
position_y = 1
total = 4095
brightness = 10
black = [0, 0, 0]
colour = [10, 10, 10]
render_list = []

def go_left():
  global position_x
  position_x = position_x - 1
  check()

def go_right():
  global position_x
  position_x = position_x + 1
  check()

def go_up():
  global position_y
  position_y = position_y - 1
  check()

def go_down():
  global position_y
  position_y = position_y + 1
  check()

def click():
  render_list.append([position_x, position_y, colour])

def toggle():
  global hue
  global temp_percent
  temp_percent = get_percentage()
  if hue:
    hue = False
  else:
    hue = True

def joystick():
  check()

def check():
  global position_y
  global position_x
  if position_y <= 0:
	position_y = 0
  if position_y >= 7:
	position_y = 7
  if position_x <= 0:
	position_x = 0
  if position_x >= 15:
	position_x = 15

def get_colour(percentage):
  global colour
  dial = get_dial(percentage)
  red = 0
  green = 0
  blue = 0
  if dial < 17:
    level = get_colour_level(dial)
    red = brightness
    green = level
    blue = 0
  if dial >= 17 and dial < 33:
    block = dial - 17;
    level = get_colour_level(block) * -1
    red = brightness + level
    green = brightness
    blue = 0
  if dial >= 33 and dial < 50:
    block = dial - 33;
    level = get_colour_level(block)
    red = 0
    green = brightness
    blue = level
  if dial >= 50 and dial < 67:
    block = dial - 50;
    level = get_colour_level(block) * -1
    red = 0
    green = brightness + level
    blue = brightness
  if dial >= 67 and dial < 84:
    block = dial - 67;
    level = get_colour_level(block)
    red = level
    green = 0
    blue = brightness
  if dial >= 84:
    block = dial - 84;
    level = get_colour_level(block) * -1
    red = brightness
    green = 0
    blue = brightness + level
  colour = [red, green, blue]

def get_dial(percentage):
  return round(100 * percentage)

def get_colour_level(dial):
  if dial == 0:
    return 0
  return round(brightness * (dial / 17))

def get_percentage():
  dial = kit.dial.read()
  return dial/total

def render_drawing():
  global render
  for x in render_list:
    kit.set_pixel(x[0], x[1], x[2])

def get_brightness(percentage):
  global brightness
  brightness = round(255 * percentage)
  get_colour(temp_percent)

kit.on_joystick_left = go_left
kit.on_joystick_right = go_right
kit.on_joystick_up = go_up
kit.on_joystick_down = go_down
kit.on_button_a = click
kit.on_button_b = toggle
kit.on_joystick_click = joystick

while True:
  percentage = get_percentage()
  if hue:
    get_colour(percentage)
  else:
    get_brightness(percentage)
  kit.check_controls()
  kit.set_background(black)
  render_drawing()
  kit.set_pixel(position_x, position_y, colour)
  kit.render()
  sleep(0.1)