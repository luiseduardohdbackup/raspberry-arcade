import smbus
import autopy
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
  OLATB) = range(0x00, 0x16)

PRESSED_VALUE = 0

devices = [0x20, 0x21, 0x22]	
keystrokes = []
keys = [ autopy.key.K_UP, autopy.key.K_LEFT,
         autopy.key.K_RIGHT,autopy.key.K_DOWN,
         'a',  'b',  'c', 'd',  'e', 'f',  'g',  
         'h',  'i',  'j', 'k',  'l', 'm',  'n',
         'o',  'p',  'q', 'r',  's', 't',  'u',
         'v',  'w',  'x', 'y',  'z', '0',  '1',
         '2',  '3',  '4', '5',  '6', '7',  '8',
         '9',  autopy.key.K_PAGEDOWN, 
         autopy.key.K_DELETE, autopy.key.K_HOME, 
         autopy.key.K_F12, autopy.key.K_F11, 
         autopy.key.K_F10, autopy.key.K_F9, 
         autopy.key.K_F8 ]

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
		autopy.key.toggle(keystroke, True)
	
	time.sleep(0.1)
	
	for keystroke in keystrokes:
		autopy.key.toggle(keystroke, False)