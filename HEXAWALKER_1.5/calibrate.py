

from core import HexapodCore
from time import sleep

def calibrate_joint(joint, t, mn, mx, z):

    while True:
        for angle in [mn, z, mx, z]:
            joint.pose(angle)
            sleep(t)
            
hexy = HexapodCore()

#calibrate_joint( hexy.right_front.hip, t = 2, mn = -50, mx = 50, z = 0)

calibrate_joint ( hexy.left_front.knee, t = 2, mn = -45, mx = 45, z = 0)

#calibrate_joint ( hexy.right_back.ankle, t = 2, mn = -90, mx = 90, z = 0)

#hexy.off()

