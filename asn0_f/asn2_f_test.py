import utility
import map_
import time
from sonar import Sonar

sonar = Sonar()

# Main loop to continuously walk forward
if __name__ == "__main__":
    utility.reset_legs()
    curpos = [0,0,3]#Left, Top, facing South
    #map = map_.CSME301Map()
    endpos = [1,0,1]
    #moves = utility.mapmap(map)
    
    print(f"curpos south: {curpos[0]}, endpos south: {endpos[0]}")
    if curpos[0] < endpos[0]:
        curpos = utility.move_cardinal(endpos[0] - curpos[0], curpos, 3)

    print(f"curpos south: {curpos[1]}, endpos south: {endpos[1]}")
    if curpos[1] < endpos[1]:
        curpos = utility.move_cardinal(endpos[1] - curpos[1], curpos, 2)
    print(f"end position: {curpos}")

    utility.turn_cardinal(curpos[2], endpos[2])

    utility.reset_legs()