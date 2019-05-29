#coding: UTF-8
##########################################################################################################
#
# Main del robot
# Se definen las acciones principales del robot a partir de las funciones base.
# Se define la funcion de vision por computador, que permite al robot seguir a un objeto hasta alcanzarlo.
#
# RLP 2019
#
###########################################################################################################

#import os
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/pi/SpeechToText/HexaWalker-85461d491b16.json"


from __future__ import print_function
from imutils.video import VideoStream
import argparse
import imutils
import time
import cv2
import os
import RPi.GPIO as GPIO

from robot.hexapod_robot import HexapodFull
from speech_to_text import *

#import os
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/pi/SpeechToText/HexaWalker-85461d491b16.json"

class HexaWalker():

	sit = True

	def __init__(self):
		
		self.hexa = HexapodFull()
		self.hexa.light(0, "R", False)
		self.hexa.light(0, "G", False)
		self.hexa.light(0, "B", False)
		self.hexa.boot_up()
		self.parpaeda("G")
		self.parpaeda("R")
		self.parpaeda("B")
		self.hexa.light(0, "B", True)
		self.sit = False


	def demoDance(self):
		
		self.hexa.boot_up()
		self.hexa.rock_body()
		self.hexa.default()
		self.hexa.dance_twist()
		self.hexa.default()
		self.hexa.shake_head()
		self.hexa.default()
		self.hexa.point()
		self.hexa.default()
		self.hexa.type_stuff()
		self.hexa.default()
		self.hexa.wave()
		self.hexa.default()
		self.hexa.tilt_left_and_right()
		self.hexa.default()
		self.hexa.tilt_front_and_back()
		self.hexa.default()
		self.hexa.dance_tilt()
		self.hexa.default()
		self.hexa.shut_down()

	def move(self):
		
		self.hexa.dance_twist(repetitions = 1)


	def parpaeda(self, s = "R"):

		self.hexa.light(0, s, True)
		sleep(0.15)
		self.hexa.light(0, s, False)
		sleep(0.15)
		self.hexa.light(0, s, True)
		sleep(0.15)
		self.hexa.light(0, s, False)
		sleep(0.15)
		self.hexa.light(0, s, True)
		sleep(0.15)
		self.hexa.light(0, s, False)
		sleep(0.15)

		
	def move2(self):

		self.hexa.dance_tilt(repetitions = 1)
		self.hexa.default()


	def shut_down(self):

		self.hexa.default()
		self.hexa.shut_down()


	def boot_up(self):

		self.hexa.boot_up()
		self.hexa.light(0, "B", True)
		sleep(0.1)
		self.hexa.light(0, "B", False)
		sleep(0.1)
		self.hexa.light(0, "B", True)
		sleep(0.1)
		self.hexa.light(0, "B", False)
		sleep(0.1)
		self.hexa.light(0, "G", True)


	def listen(self, t):

		self.hexa.light(0, "B", True)
		text = speech2text(t)
		print(text)		
		if self.sit:
			self.hexa.boot_up()
			self.sit = False

		if "avanza" in text:
			print("Adelante.................................................................")
			self.hexa.light(0, "B", False)
			self.hexa.light(0, "G", True)
			self.hexa.walk(swing = 40, repetitions = 4, raised = -30, floor = 50, t = 0.3)
			self.hexa.default()
			self.hexa.light(0, "G", False)
			self.hexa.light(0, "G", False)

		elif "retroceder" in text or "retrocede" in text:
			print("atras.................................................................")
			self.hexa.light(0, "B", False)
			self.hexa.light(0, "G", True)
			self.hexa.walk(swing = -40, repetitions = 4, raised = -30, floor = 50, t = 0.3)
			self.hexa.default()
			self.hexa.light(0, "G", False)

		elif "programa" in text or "programar" in text:
			self.hexa.light(0, "B", False)
			self.hexa.light(0, "G", True)
			self.hexa.type_stuff()
			self.hexa.default()
			self.hexa.light(0, "G", False)

		elif "izquierda" in text or "izquierdo" in text:
			print("izquierda.................................................................")
			self.hexa.light(0, "B", False)
			self.hexa.light(0, "G", True)
			self.hexa.rotate(offset = 40)
			self.hexa.default()
			self.hexa.light(0, "G", False)

		elif "derecha" in text:
			print("derecha.................................................................")
			self.hexa.light(0, "B", False)
			self.hexa.light(0, "G", True)
			self.hexa.rotate(offset = -40)
			self.hexa.default()
			self.hexa.light(0, "G", False)

		elif "descansa" in text:
			print("sientate.................................................................")
			self.hexa.light(0, "B", False)
			self.hexa.light(0, "G", True)
			self.hexa.shut_down()
			self.sit = True
			self.hexa.light(0, "G", False)

		elif "baila" in text or "baile" in text:
			print("baila...................s..............................................")
			self.hexa.light(0, "B", False)
			self.hexa.light(0, "G", True)
			self.hexa.default()			
			self.hexa.rock_body()
			self.hexa.dance_twist()
			self.hexa.tilt_left_and_right()
			self.hexa.default()
			self.hexa.light(0, "G", False)

		elif "hola" in text:
			print("saludando.................................................................")
			self.hexa.light(0, "B", False)
			self.hexa.light(0, "G", True)
			self.hexa.wave()
			self.hexa.default()
			self.hexa.light(0, "G", False)

		elif "demo" in text:
			print("saludando.................................................................")
			self.hexa.light(0, "B", False)
			self.hexa.light(0, "G", True)
			self.demoDance()
			self.hexa.light(0, "G", False)

		elif "busca" in text:
			print(".camara................................................................")
			self.cam_loop()

		else:
			self.hexa.light(0, "B", False)
			self.hexa.light(0, "R", True)
			self.move()
			self.hexa.light(0, "R", False)
		

	def cam_loop(self):

		self.hexa.light(0, "B", False)
		# construct the argument parse and parse the arguments
		print("[INFO] waiting for camera to warmup...")
		vs = VideoStream(0).start()
		time.sleep(2.0)

		# define the lower and upper boundaries of the object
		# to be tracked in the HSV color space
		colorLower = (-2, 100, 100)
		colorUpper = (18, 255, 255)

		# Start with LED off
		# GPIO.output(redLed, GPIO.LOW)
		# ledOn = False

		# loop over the frames from the video stream
		while True:
			# grab the next frame from the video stream, Invert 180o, resize the
			# frame, and convert it to the HSV color space
			frame = vs.read()
			frame = imutils.resize(frame, width=500)
		#	frame = imutils.rotate(frame, angle=180)
			hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

			# construct a mask for the object color, then perform
			# a series of dilations and erosions to remove any small
			# blobs left in the mask
			mask = cv2.inRange(hsv, colorLower, colorUpper)
			mask = cv2.erode(mask, None, iterations=2)
			mask = cv2.dilate(mask, None, iterations=2)

			# find contours in the mask and initialize the current
			# (x, y) center of the object
			cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
				cv2.CHAIN_APPROX_SIMPLE)
			cnts = cnts[0] if imutils.is_cv2() else cnts[1]
			center = None

			# only proceed if at least one contour was found
			if len(cnts) > 0:
				self.hexa.light(0, "G", True)
				self.hexa.light(0, "R", False)
				# find the largest contour in the mask, then use
				# it to compute the minimum enclosing circle and
				# centroid
				c = max(cnts, key=cv2.contourArea)
				((x, y), radius) = cv2.minEnclosingCircle(c)
				M = cv2.moments(c)
				center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

				# only proceed if the radius meets a minimum size
				print (radius)
				if radius >110:
					break
				if radius > 10:
					# draw the circle and centroid on the frame,
					# then update the list of tracked points
					cv2.circle(frame, (int(x), int(y)), int(radius),
						(0, 255, 255), 2)
					cv2.circle(frame, center, 5, (0, 0, 255), -1)
					
					# position Servo at center of circle
					#print ("[INFO] Object Center coordenates at X0 = {0} and Y0 =  {1}".format(x, y))
					if (x < 220): 
						print ("[ACTION] GIRAR IZQUIERDA")
						self.hexa.rotate(offset = 15, repetitions = 1)
				 
					if (x > 280):
						print ("[ACTION] GIRAR DERECHA")
						self.hexa.rotate(offset = -15, repetitions = 1)

					if radius < 105:
						self.hexa.walk(swing = 40, repetitions = 1, raised = -30, floor = 50, t = 0.3)
				
			else:
				self.hexa.light(0, "G", False)
				self.hexa.light(0, "R", True)


					
					# if the led is not already on, turn the LED on
					# if not ledOn:
						# GPIO.output(redLed, GPIO.HIGH)
						# ledOn = True

			# if the ball is not detected, turn the LED off
			# elif ledOn:
				# GPIO.output(redLed, GPIO.LOW)
				# ledOn = False

			# show the frame to our screen
			cv2.imshow("Frame", frame)
			
			# if [ESC] key is pressed, stop the loop
			key = cv2.waitKey(1) & 0xFF
			if key == 27:
					break
		self.hexa.point()
		self.parpaeda( s = "G")
		sleep(1)
		# do a bit of cleanup
		print("\n [INFO] Exiting Program and cleanup stuff \n")
		cv2.destroyAllWindows()
		vs.stop()
	
			
def main():

	robot = HexaWalker()
	count = 0
	
	while True:		
		robot.listen(100)

		if count >=8:
			robot.move2()
			robot.sit = True
			count = 0		

		count += 1
		

		

if __name__ == '__main__':
	
	main()
