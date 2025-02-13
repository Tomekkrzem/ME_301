import utility
import map_301
import time
from sonar import Sonar

sonar = Sonar()

# Main loop to continuously walk forward
if __name__ == "__main__":
    utility.reset_legs()
    map = map_301.CSME301Map()
    map.printObstacleMap()
    curpos = utility.inputPos()
    endpos = utility.inputPos()

    utility.mapmap(map, endpos)
    map.printCostMap()

    moves = utility.find_path(map, curpos, endpos)
    print(moves)

    for i in range(len(moves)):
        dir = moves[i]
        count = 1
        while moves[i] == moves[i+1]:
            count += 1
            i += 1
        utility.move_cardinal(count, curpos, dir)
        utility.reset_legs()

    utility.reset_legs()

    # #Exploring
    # utility.reset_legs()
    # map = map_.CSME301Map()
    # map.clearObstacleMap()
    # map.clearCostMap()
    # curpos = [0,0,1]
    


    # #Localization
    # utility.turn_cardinal(curpos[2], endpos[2])
    
    # if curpos[0] < endpos[0]:
    #     curpos = utility.move_cardinal(endpos[0] - curpos[0], curpos, 3)

    # if curpos[1] < endpos[1]:
    #     curpos = utility.move_cardinal(endpos[1] - curpos[1], curpos, 2)

    # utility.turn_cardinal(curpos[2], endpos[2])