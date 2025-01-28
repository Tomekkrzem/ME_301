import time
import utility

if __name__ == "__main__":
    utility.reset_legs()
    time.sleep(1)

    #utility.walk_forward()
    #print(utility.end_timer(timer))
    
    timer = utility.start_timer()
    for i in range(5):
        timer = utility.start_timer()
        utility.turn(False, 180)
        print(utility.end_timer(timer))
        i = i + 1
        utility.reset_legs()
        time.sleep(2.5)
    #utility.turn(False, 90)
    #time.sleep(3)
    #utility.turn(True, 90)
    #time.sleep(3)
    #utility.turn(False, 180)
    #time.sleep(3)
    #utility.turn(True, 180)

    utility.reset_legs()