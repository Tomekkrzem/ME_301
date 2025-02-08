import utility
import time
from sonar import Sonar

sonar = Sonar()

# Main loop to continuously walk forward
if __name__ == "__main__":
    utility.reset_legs()
    count = 0
    for i in range (3):
        dist = sonar.getDistance()
        print(dist)
        if dist <= 400:
            count += 1
        time.sleep(1)
        print(f"Count: {count}")

    if count == 1:
        utility.turn(False,90)
    if count == 2:
        utility.turn(True,90)
    if count == 3:
        utility.turn(False,180)
    print("Done.")
    time.sleep(1)

    #for i in range(5):#assuming 1 is front, 2 is left, 3 is right
    #    dists = utility.scan([1])
    #    if(dists[0] <= 2500):
    #        if(dists[1] <= 2500 and dists[2]>2500):
    #            utility.turn(False, 90)
    #        elif(dists[1] > 2500):
    #            utility.turn(True, 90)
    #        else:
    #            utility.turn(False, 180)

    #for i in range(5):
        #if (sonar.getDistance() < 350):
            #utility.walk_forward()
