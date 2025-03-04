import time
import utility

if __name__ == "__main__":
    utility.reset_legs()
    
    utility.turn_sensor(500)
    time.sleep(1)
    utility.turn_sensor(125)
    time.sleep(1)
    utility.turn_sensor(875)
    time.sleep(1)
    utility.turn_sensor(500)
    time.sleep(1)

    utility.reset_legs()