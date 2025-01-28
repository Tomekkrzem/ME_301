import utility
import time
from sonar import Sonar

sonar = Sonar()

# Wave function
# if __name__ == "__main__":
#     utility.reset_legs()
#     count = 0
#     for i in range (3):
#         dist = sonar.getDistance()
#         print(dist)
#         if dist <= 400:
#             count += 1
#         time.sleep(1)
#         print(f"Count: {count}")

#     if count == 1:
#         utility.turn(False,90)
#     if count == 2:
#         utility.turn(True,90)
#     if count == 3:
#         utility.turn(False,180)
#     print("Done.")
#     time.sleep(1)

# for i in range(4):
#     dist = sonar.getDistance()
#     print(dist)
#     if (dist <= 350):
#         utility.walk_forward()
#     else:
#         utility.turn(False, 45)

while True:
    dist = sonar.getDistance()
    print(dist)
    time.sleep(0.1)