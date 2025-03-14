import asn3_f.utility as utility
import map_301
import time

# Main loop to continuously walk forward
if __name__ == "__main__":
    utility.reset_legs()

    #Mapping
    # map = map_301.CSME301Map()
    # map.printCostMap()
    curpos = utility.inputPos()
    endpos = utility.inputPos()

    timer = utility.start_timer()
    # utility.turn_cardinal(2, 1)
    # time.sleep(3)
    # utility.turn_cardinal(1, 2)

    # utility.mapmap(map, endpos)
    # map.printCostMap()

    # moves = utility.find_path(map, curpos, endpos)
    # print(moves)

    # for move in moves:
    #     curpos = utility.move_cardinal(1, curpos, move)
    #     utility.reset_legs()

    # utility.turn_cardinal(curpos[2], endpos[2])
    # curpos[2] = endpos[2]

    #Exploring
    # map = map_301.CSME301Map(8, 8)
    # map.clearObstacleMap()
    # map.clearCostMap()
    # map.printCostMap()
    # curpos = [0,0,1]
    # utility.explore_map(map, curpos)
    # map.printCostMap()
    
    # #Localization
    #utility.turn_cardinal(curpos[2], endpos[2])
    
    if curpos[0] < endpos[0]:
        curpos = utility.move_cardinal(endpos[0] - curpos[0], curpos, 3)

    if curpos[1] < endpos[1]:
        curpos = utility.move_cardinal(endpos[1] - curpos[1], curpos, 2)

    utility.turn_cardinal(curpos[2], endpos[2])

    
    print(f"Execution time: {utility.end_timer(timer)}")

    utility.reset_legs()