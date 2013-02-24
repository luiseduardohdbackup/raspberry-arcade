import smbus
import uinput
import time

( IODIRA, 
  IODIRB, 
  IPOLA, 
  IPOLB, 
  GPINTENA, 
  GPINTENB, 
  DEFVALA, 
  DEFVALB, 
  INTCONA, 
  INTCONB, 
  IOCON, 
  IOCON, 
  GPPUA, 
  GPPUB, 
  INTFA, 
  INTFB, 
  INTCAPA, 
  INTCAPB, 
  GPIOA, 
  GPIOB,
  OLATA,
  OLATB ) = range(0x00, 0x16)

PRESSED_VALUE = 0

devices = [0x20, 0x21, 0x22]	
keystrokes = []
keys = [ uinput.KEY_UP, uinput.KEY_LEFT, uinput.KEY_RIGHT,
         uinput.KEY_DOWN, uinput.KEY_A, uinput.KEY_B,
         uinput.KEY_C, uinput.KEY_D, uinput.KEY_E, uinput.KEY_F,
         uinput.KEY_G, uinput.KEY_H, uinput.KEY_I, uinput.KEY_J,
         uinput.KEY_K, uinput.KEY_L, uinput.KEY_M, uinput.KEY_N,
         uinput.KEY_O, uinput.KEY_P, uinput.KEY_Q, uinput.KEY_R,
         uinput.KEY_S, uinput.KEY_T, uinput.KEY_U, uinput.KEY_V,
         uinput.KEY_W, uinput.KEY_X, uinput.KEY_Y, uinput.KEY_Z,
         uinput.KEY_0, uinput.KEY_1, uinput.KEY_2, uinput.KEY_3,
         uinput.KEY_4, uinput.KEY_5, uinput.KEY_6, uinput.KEY_7,
         uinput.KEY_8, uinput.KEY_9, uinput.KEY_PAGEDOWN, 
         uinput.KEY_DELETE, uinput.KEY_HOME, uinput.KEY_F12,
         uinput.KEY_F11, uinput.KEY_F10, uinput.KEY_F9,
         uinput.KEY_F8 ]

keyboard = uinput.Device(keys)

I2C = smbus.SMBus(1)

for device in devices:
	I2C.write_word_data(device, IPOLA, 0x0000)
	I2C.write_word_data(device, IODIRA, 0xFFFF)
	I2C.write_word_data(device, GPPUA, 0xFFFF)
	
while True:
	buttons = 0
	del keystrokes[:]
	
	for dev in reversed(devices):
		buttons <<= 16
		buttons += I2C.read_word_data(dev, GPIOA)

	for button in range(len(keys)):
		pressed = buttons >> button & 1
		if pressed == PRESSED_VALUE:
			keystrokes.append(keys[button])
	
	for keystroke in keystrokes:
		keyboard.emit(keystroke, 1)
	
	time.sleep(0.1)
	
	for keystroke in keystrokes:
		keyboard.emit(keystroke, 0)