import utility
import time

# Main loop to continuously walk forward
if __name__ == "__main__":
    utility.reset_legs()
    utility.turn(False, 90)
    time.sleep(1)
    utility.turn(True, 90)
