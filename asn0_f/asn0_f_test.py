import utility

# Main loop to continuously walk forward
if __name__ == "__main__":
    #prepare legs
    utility.reset_legs()

    for i in range(10):
        utility.walk_forward()
        i = i + 1
        
    utility.turn(True, 90)