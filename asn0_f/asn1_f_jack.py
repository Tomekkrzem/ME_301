import utility
import time
from sonar import Sonar

sonar = Sonar()

for i in range(5): #Made for only one sensor, currently on left side
    dist = sonar.getDistance()
    print(dist)
    if (dist <= 330):
        utility.turn(False, 10)
    elif (dist >= 370):
        utility.turn(True, 10)
    else:
        utility.walk_forward()
