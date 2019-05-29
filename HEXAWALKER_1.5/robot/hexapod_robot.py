#coding: UTF-8
######################################################################################################
#
# Cuerpo del código del robot, se definen las funciones base del robot.
# 
# RLP 2019
#
######################################################################################################

from core.hexapod_core import HexapodCore
from time import sleep

class HexapodFull(HexapodCore):

	def boot_up(self):

		self.look()
		self.lie_down()
		self.curl_up()
		self.lie_flat()
		self.get_up()

	def shut_down(self):

		self.look()
		self.lie_down()
		self.lie_flat()
		self.curl_up(die = True)

	def curl_up(self, die = False, t = 0.2):

		for leg in self.legs:
			leg.pose(hip_angle = 0, 
					 knee_angle = -(leg.knee.max + leg.knee.leeway), 
					 ankle_angle = leg.ankle.max)

		sleep(t)

		if die: self.off()
		
	def lie_flat(self, t = 0.15):
		
		for leg in self.legs:
			leg.pose()
			
		sleep(t)

	def lie_down(self, maxx = 50, step = 4, t = 0.15):
		
		for angle in xrange(maxx, -(maxx + 1), -step):
			self.squat(angle)

		sleep(t)

	def get_up(self, maxx = 70, step = 4):

		for angle in xrange(-maxx, maxx + 1, step):
			self.squat(angle)

		self.default()

	def look(self, angle = 0, t = 0.05):
		self.neck.pose(angle)
		sleep(t)

	def twist_hip(self, angle = 0, t = 0.1):

		for hip in self.hips:
			hip.pose(angle)

		sleep(t)
		
	def squat(self, angle, t = 0):

		for leg in self.legs:
			leg.move(knee_angle = angle)

		sleep(t)

	def walk(self, offset = 25 , swing =  25, raised = -30, floor = 50, repetitions = 4, t = 0.2):
		""" if swing > 0, hexy moves forward else backward """
		
		swings = [offset - swing, swing, -(offset + swing)]
		reverse_swings = [-x for x in swings]
		
		for r in xrange(repetitions):
			self.stride(self.tripod1, self.tripod2, swings, raised, floor, t)
			self.stride(self.tripod2, self.tripod1, reverse_swings, raised, floor, t)

	def rotate(self, offset = 40, raised = -30, floor = 50, repetitions = 5, t = 0.2):
		""" if offset > 0, hexy rotates left, else right """
	
		for r in xrange(repetitions):
			
			#replant tripod2 with an offset
			self.uniform_move(self.tripod2, None, raised, t)
			self.uniform_move(self.tripod2, offset, floor, t)

			#raise tripod1
			self.uniform_move(self.tripod1, -offset, raised) 
			
			#swing tripod2's hips to an -offset 
			self.uniform_move(self.tripod2, -offset, None, t)
			
			#lower tripod1
			self.uniform_move(self.tripod1, 0, floor, t)

			
	def stride(self, first_tripod, second_tripod, swing, raised, floor, t):
		""" first_tripod's legs replant to propel towards a direction while
			second_tripod's legs retrack by swinging to the opposite direction """

		self.simultaneous_move(first_tripod, knee_angle = raised)
		sleep(t)
		
		self.simultaneous_move(second_tripod, swing[::-1])
		self.simultaneous_move(first_tripod, swing, floor)
		sleep(t)

	def tilt_side(self, left_angle = 50, right_angle = 0, t = 0.2):
		""" if left_angle > right_angle, left side is higher than right side """
		
		self.uniform_move(legs = self.left_legs, knee_angle = left_angle)
		self.uniform_move(legs = self.right_legs, knee_angle = right_angle)
		sleep(t)

	def tilt(self, front_angle = 50, middle_angle = 25, back_angle = 0, t = 0.2):
		""" if front_angle > middle_angle > back_angle hexy's front is higher than his back """

		self.right_front.move(knee_angle = front_angle)
		self.left_front.move(knee_angle = front_angle)

		self.right_middle.move(knee_angle = middle_angle)
		self.left_middle.move(knee_angle = middle_angle)

		self.right_back.move(knee_angle = back_angle)
		self.left_back.move(knee_angle = back_angle)

		sleep(t)

	def default(self, offset = 45, floor = 60, raised = -30,  t = 0.2):
		""" Hexy's default pose, offset > 0 brings the front and back legs to the side """ 
		
		swings = [offset, 0, -offset]

		self.look()
		self.squat(floor, t)
		
		self.simultaneous_move(self.tripod1, swings, raised, t)
		self.simultaneous_move(self.tripod1, swings, floor, t)
		self.simultaneous_move(self.tripod2, swings[::-1], raised, t)
		self.simultaneous_move(self.tripod2, swings[::-1], floor, t)

	def uniform_move(self, legs, hip_angle = None, knee_angle = None, t = 0):
		""" moves all legs with hip_angle, knee_angle """
		
		for leg in legs:
			leg.move(knee_angle, hip_angle)

		sleep(t)

	def simultaneous_move(self, legs, swings = [None, None, None], knee_angle = None, t = 0):
		""" moves all legs with knee_angle to the respective hip angles at 'swing' """
		
		for leg, hip_angle in zip(legs, swings):
			leg.move(knee_angle, hip_angle)

		sleep(t)

	def shake_head(self, maxx = 60, repetitions = 5, t = 0.2):

		for r in xrange(repetitions):
			self.look(maxx, t)
			self.look(-maxx, t)
		
		self.look()

	def point(self, t = 0.75):
		
		self.left_front.hip.pose(-45)
		self.left_front.knee.pose(-50)
		self.left_front.ankle.pose(-55)

		sleep(t)

	def wave(self, repetitions = 5, t = 0.2):
		
		self.left_front.ankle.pose()
		self.left_front.knee.pose(-50)
		
		for r in xrange(repetitions):
			self.left_front.hip.pose(-45)
			sleep(t)
			self.left_front.hip.pose(45)
			sleep(t)

	def dance_twist(self, maxx = 45, step = 5, repetitions = 3, t = 0.01):

		self.squat(60, t)

		for r in xrange(repetitions):
			
			for angle in xrange(-maxx, maxx, step):
				self.twist_hip(angle, t)
			
			for angle in xrange(maxx, -maxx, -step):
				self.twist_hip(angle, t)

		self.twist_hip()
		self.squat(60, t)


	def lean_back(self, offset = 45, back_knee = 0, middle_knee = 40, raised = -30, t = 0.2):
		""" brings the back legs even further to the back and the middle legs to the front
			and then brings his front legs up in the air """ 
		
		self.left_back.replant(raised, back_knee, offset, t)
		self.right_back.replant(raised, back_knee, -offset, t)
		self.left_middle.replant(raised, middle_knee, -offset, t)
		self.right_middle.replant(raised, middle_knee, offset, t)
		
		self.left_front.pose(-offset, 0, 0)
		self.right_front.pose(offset, 0, 0)

		sleep(t)

	def type_stuff(self, up = -40, down = 40, repetitions = 5, t = 0.2):

		self.lean_back()

		for r in xrange(repetitions):

			self.left_front.knee.pose(up)
			self.right_front.knee.pose(down)
			sleep(t)

			self.right_front.knee.pose(up)
			self.left_front.knee.pose(down)
			sleep(t)
		
		sleep(t)

	def tilt_left_and_right(self, raised = 60, floor = 20, repetitions = 5, t = 0.15):
		
		for r in xrange(repetitions):
			self.tilt_side(left_angle = floor, right_angle = raised)
			self.tilt_side(left_angle = raised, right_angle = floor)

		self.squat(raised, t)

	def tilt_front_and_back(self, up = 60, mid = 40, down = 20, repetitions = 5, t = 0.15):
		
		for r in xrange(repetitions):
			self.tilt(up, mid, down)
			self.tilt(down, mid, up)

		self.squat(up, t)
	
	def dance_tilt(self, raised = 60, mid = 40, floor = 20, repetitions = 3, t = 0.15):

		for r in xrange(repetitions):
			
			self.tilt(floor, mid, raised, t) # front
			self.tilt_side(raised, floor, t) # right
			self.tilt(raised, mid, floor, t) # back
			self.tilt_side(floor, raised, t) # left

		self.squat(raised, t)

	def rock_body(self,  offset = 45, floor = 50, repetitions = 7):

		for r in xrange(repetitions):
			self.uniform_move(self.left_legs, offset, floor, 0)
			self.uniform_move(self.right_legs, -offset, floor, 0.2)
			self.uniform_move(self.left_legs, -offset, floor, 0)
			self.uniform_move(self.right_legs, offset, floor, 0.2)



	def light(self, numLed, RGB = "R", onOff = True):

		if RGB == "R":
			self.leds[numLed].red(onOff)
		elif RGB =="G":
			self.leds[numLed].green(onOff)
		elif RGB == "B":
			self.leds[numLed].blue(onOff)

	def lightOff(self, numLed):
		self.leds[numLed].off()

	def afraid(self):
		self.light(0)
		self.lie_down()
		self.lie_flat()
		self.lightOff(0)

	# Dancing

	def prepare(self, offset = 45, back_knee = 0, middle_knee = 50, front_knee = 60, raised = -30, t = 0.2):
		""" brings the back legs even further to the back and the middle legs to the front
			and then brings his further to the front """ 
		
		self.left_back.replant(raised, back_knee, offset, t)
		self.right_back.replant(raised, back_knee, -offset, t)
		self.left_middle.replant(raised, middle_knee, -offset, t)
		self.right_middle.replant(raised, middle_knee, offset, t)
		
		self.left_front.replant(raised, front_knee, -offset, t)
		self.right_front.replant(raised, front_knee, offset, t)

		self.neck.pose()

		sleep(t)
		
	def wave_right_arm_up(self):
	
		self.right_front.knee.pose(-60)
		self.right_front.ankle.pose(0)
		self.right_front.hip.pose(-45)
		self.neck.pose(-40)

	def wave_right_arm_down(self):
		self.right_front.knee.pose(50)
		self.right_front.ankle.pose(-50)
		self.right_front.hip.pose(45)
		self.neck.pose(0)
		
	def dip_body(self, mid = 50, back = 0):
		
		self.left_middle.move(knee_angle = mid)
		self.right_middle.move(knee_angle = mid)
		self.left_back.move(knee_angle = -back)
		self.right_back.move(knee_angle = -back)

	def raise_body(self, mid = 70, back = 20):
		
		self.left_middle.move(knee_angle = mid)
		self.right_middle.move(knee_angle = mid)
		self.left_back.move(knee_angle = back)
		self.right_back.move(knee_angle = back)

	def night_fever(self):

		self.prepare()
		
		for r in xrange(4):
			self.wave_right_arm_up()
			self.left_front.move(knee_angle = 40)
			self.dip_body()
			sleep(0.4)
			self.wave_right_arm_down()
			self.left_front.move(knee_angle = 60)
			self.raise_body()
			sleep(0.4)

	def arms_up_left(self):
		self.right_front.pose(knee_angle = -60, ankle_angle = -80, hip_angle = -45)
		self.left_front.pose(knee_angle = -60, ankle_angle = -80, hip_angle = -45)
		self.neck.pose(-45)

	def arms_up_right(self):
		self.right_front.pose(knee_angle = -60, ankle_angle = -80, hip_angle = 45)
		self.left_front.pose(knee_angle = -60, ankle_angle = -80, hip_angle = 45)
		self.neck.pose(45)

	def arms_down_center(self):
		self.right_front.pose(knee_angle = 30, ankle_angle = -60, hip_angle = 0)
		self.left_front.pose(knee_angle = 30, ankle_angle = -60, hip_angle = 0)
		self.neck.pose()

	def thriller_routine0(self):
		self.arms_down_center()
		self.raise_body()
		sleep(0.3)
		
	def thriller_routine1(self):
		self.thriller_routine0()
		self.arms_up_left()
		self.dip_body()
		sleep(0.3)
		
	def thriller_routine2(self):
		self.thriller_routine0()
		self.arms_up_right()
		self.dip_body()
		sleep(0.3)

	def thriller(self):
		
		self.prepare()

		for r in xrange(3):
			self.thriller_routine1()
			self.thriller_routine2()

