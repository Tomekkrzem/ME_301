import time
import sys
import signal
import threading
import ros_robot_controller_sdk as rrc
from sonar import Sonar
import utility


s = Sonar()
s.setRGBMode(0)
s.setPixelColor(0,(255,0,0))
s.setPixelColor(0,(255,0,0))

board = rrc.Board()
legs = {
    1: (1, 2, 3),       # Back Left
    2: (4, 5, 6),       # Middle Left
    3: (7, 8, 9),       # Front Left
    4: (10, 11, 12),    # Back right
    5: (13, 14, 15),    # Middle right
    6: (16, 17, 18)     # Front right
}

start_time = time.time()

while time.time() - start_time < 1:
    time.sleep(0.1)
    print(s.getDistance())

for i in range(5):
    print(i)
    if s.getDistance() < 450:
        utility.turn(False,45)
    else:
        utility.turn(True,45)



