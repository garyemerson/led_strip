# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
import time
import sys
import math
import random
import time



from neopixel import *


# LED strip configuration:
LED_COUNT      = 60 #16      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering



# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
	"""Wipe color across display a pixel at a time."""
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, color)
		strip.show()
		time.sleep(wait_ms/1000.0)

def theaterChase(strip, color, wait_ms=50, iterations=10):
	"""Movie theater light style chaser animation."""
	for j in range(iterations):
		for q in range(3):
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, color)
			strip.show()
			time.sleep(wait_ms/1000.0)
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, 0)

def wheel(pos):
	"""Generate rainbow colors across 0-255 positions."""
	if pos < 85:
		return Color(pos * 3, 255 - pos * 3, 0)
	elif pos < 170:
		pos -= 85
		return Color(255 - pos * 3, 0, pos * 3)
	else:
		pos -= 170
		return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=20, iterations=1):
	"""Draw rainbow that fades across all pixels at once."""
	for j in range(256*iterations):
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, wheel((i+j) & 255))
		strip.show()
		time.sleep(wait_ms/1000.0)

def rainbowCycle(strip, wait_ms=20, iterations=5):
	"""Draw rainbow that uniformly distributes itself across all pixels."""
	for j in range(256*iterations):
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
		strip.show()
		time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
	"""Rainbow movie theater light style chaser animation."""
	for j in range(256):
		for q in range(3):
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, wheel((i+j) % 255))
			strip.show()
			time.sleep(wait_ms/1000.0)
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, 0)

def studyLighting(strip, color):
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, color)
		# strip.show()
		# time.sleep(50/1000.0)
	strip.show()
	# for i in range(strip.numPixels()):
	# 	strip.setPixelColor(i, )

def firelord(strip):
	levels = [1,24,87,166,229,254,229,166,87,24]
	wait_ms = 140

	# t0 = time.time()
	for j in range(10000):
		for i in range(0, strip.numPixels()):
			index = i % len(levels)

			# index = ((i + j) % strip.numPixels()) % len(levels)
			# strip.setPixelColor(i, Color(levels[index] / 4, levels[index] / 2, levels[index]))

			# index = random.randint(max(0, (i % len(levels)) - 1), min(len(levels) - 1, (i % len(levels)) + 1)) % len(levels)
			# strip.setPixelColor(i, Color(levels[index], levels[index] / 2, levels[index] / 4))

			intensity = random.randint(max(0, levels[index] - (levels[index] / 4)), min(255, levels[index] + (levels[index] / 4)))
			strip.setPixelColor(i, Color(intensity, intensity / 3, intensity / 4))
		strip.show()
		time.sleep(wait_ms/1000.0)
	# t1 = time.time()
	# total = t1-t0
	# print "it took " + str(total)

def fade_in_out_step(strip, px, start, end):
	target = random.randint(start, end)
	curr = start
	while True:
		if curr != target:
			if curr < target:
				curr += 1
				strip.setPixelColor(px, Color(curr, curr / 4, 0))
				yield
			else:
				curr -= 1
				strip.setPixelColor(px, Color(curr, curr / 4, 0))
				yield
		else:
			target = random.randint(start, end)

	# while True:
	# 	for i in range(start, end + 1):
	# 		strip.setPixelColor(px, Color(i, i / 4, 0))
	# 		yield
	# 	for i in range(end, start - 1, -1):
	# 		strip.setPixelColor(px, Color(i, i / 4, 0))
	# 		yield

def test(strip):
	lights = [fade_in_out_step(strip, t[0], t[1], t[2]) for t in [
        (47, 0, 255),
        (48, 0, 255),
        (49, 0, 255),
        (50, 0, 255),
        (51, 0, 255),
        (52, 0, 255),
        (53, 0, 255),
        (54, 0, 255),
        (55, 0, 255),
        (56, 0, 255),
        (57, 0, 255),
        (58, 0, 255)]]
		# (51, 50, 150),
		# (52, 100, 200),
		# (53, 150, 250),
		# (54, 200, 255),
		# (55, 150, 250),
		# (56, 100, 200),
		# (57, 50, 150)]]
	while True:
		for l in lights:
			next(l)
		strip.show()
		time.sleep(0.005)

	# strip.setPixelColor(50, Color(8, 2, 0))
	# strip.setPixelColor(52, Color(16, 4, 0))
	# strip.setPixelColor(51, Color(32, 8, 0))
	# strip.setPixelColor(52, Color(64, 16, 0))
	# strip.setPixelColor(52, Color(128, 32, 0))
	# strip.setPixelColor(53, Color(255, 64, 0))
	# strip.setPixelColor(56, Color(50, 2, 0))
	# strip.setPixelColor(57, Color(50, 2, 0))
	# strip.setPixelColor(58, Color(50, 2, 0))
	strip.show()

# Main program logic follows:
if __name__ == '__main__':
	# Create NeoPixel object with appropriate configuration.
	strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
	# Intialize the library (must be called once before other functions).
	strip.begin()

	# print ('Press Ctrl-C to quit.')

	if (len(sys.argv) > 1):
		# print sys.argv
		# print c
		c = Color(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
		studyLighting(strip, c)
	else:		
		# for i in range(0, 10, 1):
		# 	print (127 * math.sin(2 * math.pi * (i / 10.0) - (math.pi / 2)) + 127)
		# firelord(strip)
		print str(strip.numPixels()) + " pixels"
		test(strip)

	# while True:
		# print ('Color wipe animations.')
		# colorWipe(strip, Color(255, 0, 0))  # Red wipe
		# colorWipe(strip, Color(0, 255, 0))  # Blue wipe
		# colorWipe(strip, Color(0, 0, 255))  # Green wipe
		# print ('Theater chase animations.')
		# theaterChase(strip, Color(127, 127, 127))  # White theater chase
		# theaterChase(strip, Color(127,   0,   0))  # Red theater chase
		# theaterChase(strip, Color(  0,   0, 127))  # Blue theater chase
		# print ('Rainbow animations.')
		# rainbow(strip)
		# rainbowCycle(strip)
		# theaterChaseRainbow(strip)
