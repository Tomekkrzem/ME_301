import utility
import map_
import time
from sonar import Sonar

sonar = Sonar()

# Main loop to continuously walk forward
if __name__ == "__main__":
    utility.reset_legs()
    map = map_.CSME301Map()
    map.printObstacleMap()
    curpos = utility.inputPos()
    endpos = utility.inputPos()

    utility.mapmap(map, endpos)
    map.printCostMap()

    moves = utility.find_path(map, curpos, endpos)
    print(moves)
    
    
    # if curpos[0] < endpos[0]:
    #     curpos = utility.move_cardinal(endpos[0] - curpos[0], curpos, 3)

    # if curpos[1] < endpos[1]:
    #     curpos = utility.move_cardinal(endpos[1] - curpos[1], curpos, 2)

    # utility.turn_cardinal(curpos[2], endpos[2])

    utility.reset_legs()