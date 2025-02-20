import time
from collections import deque
import sys
import signal
import threading
import map_301
import movement
import ros_robot_controller_sdk as rrc
from sonar import Sonar


board = rrc.Board()
robot = movement.Spyder(0.057)
sonar = Sonar()
start = True
speed = 0.25

# Assumed leg-motor relations
legs = {
    1: (1, 2, 3),   # Back Left
    2: (4, 5, 6),   # Middle Left
    3: (7, 8, 9),   # Front Left
    4: (10, 11, 12), # Back right?
    5: (13, 14, 15),# Middle right
    6: (16, 17, 18) # Front right?
}

def uSleep(timing):
    time.sleep(speed * timing)

# Set parameters for leg movement
def move_leg(leg_id, horizontal_pos, first_segment_pos, second_segment_pos):
    motor_ids = legs[leg_id]
    board.bus_servo_set_position(speed, [[motor_ids[0], horizontal_pos], [motor_ids[1], first_segment_pos], [motor_ids[2], second_segment_pos]])

# Walking sequence
def walk_forward():
    #Lifted legs and move first set
    move_leg(1, 300, 350, 375)
    move_leg(3, 500, 350, 375)
    move_leg(5, 600, 650, 625)
    uSleep(0.5)
    
    move_leg(1, 300, 375, 225)
    move_leg(3, 500, 375, 225)
    move_leg(5, 600, 625, 775)
    uSleep(1)

    #Lift second set
    move_leg(2, 400, 350, 375)
    move_leg(4, 700, 650, 625)
    move_leg(6, 600, 650, 625)
    uSleep(0.5)

    #Move on first
    move_leg(1, 550, 375, 225)
    move_leg(3, 750, 375, 225)
    move_leg(5, 400, 625, 775)
    uSleep(1)

    #Stand on second
    move_leg(2, 400, 375, 225)
    move_leg(4, 700, 625, 775)
    move_leg(6, 600, 625, 775)
    uSleep(1)

    #Lift first
    move_leg(1, 300, 350, 375)
    move_leg(3, 500, 350, 375)
    move_leg(5, 600, 650, 625)
    uSleep(0.5)

    #Turn on second
    move_leg(2, 600, 375, 225)
    move_leg(4, 470, 625, 775)
    move_leg(6, 420, 625, 775)
    uSleep(1)


#Sets all legs to default standing positions
def reset_legs():
    for i in range(6):
        i = i+1
        if(i < 4):
            move_leg(i, 500, 375, 225)
        else:
            move_leg(i, 500, 625, 775)
    board.bus_servo_set_position(0.01, [[21, 500]])
    uSleep(1)

#new turn
def turn(RorL, degree):
    newdeg = min(45, degree)
    differance = int(110 / (45/newdeg)) - 4
    if RorL:
        differance -= 15
    forwards = 500 - differance
    backwards = 500 + differance
    if(RorL):#Turning left
        forwards = 500 + differance
        backwards = 500 - differance

    #Lift second set
    move_leg(2, forwards, 150, 100)
    move_leg(4, forwards, 850, 900)
    move_leg(6, forwards, 850, 900)
    uSleep(0.5)

    #Stand on second
    move_leg(2, forwards, 375, 225)
    move_leg(4, forwards, 625, 775)
    move_leg(6, forwards, 625, 775)
    uSleep(1)

    #Lift first
    move_leg(1, forwards, 150, 100)
    move_leg(3, forwards, 150, 100)
    move_leg(5, forwards, 850, 900)
    uSleep(0.5)

    #Turn on second
    move_leg(2, backwards, 375, 225)
    move_leg(4, backwards, 625, 775)
    move_leg(6, backwards, 625, 775)
    uSleep(1)

    #Stand on first
    move_leg(1, forwards, 375, 225)
    move_leg(3, forwards, 375, 225)
    move_leg(5, forwards, 625, 775)
    uSleep(1)

    #Lift second set
    move_leg(2, forwards, 150, 100)
    move_leg(4, forwards, 850, 900)
    move_leg(6, forwards, 850, 900)
    uSleep(0.5)

    #Turn on first
    move_leg(1, backwards, 375, 225)
    move_leg(3, backwards, 375, 225)
    move_leg(5, backwards, 625, 775)
    uSleep(1)

    if (degree > 45):
        turn(RorL, degree - 45)

    else:
        if(RorL):
            move_leg(2, 500, 375, 225)
            move_leg(4, 500, 625, 775)
            move_leg(6, 500, 625, 775)
            uSleep(1)

            move_leg(1, 500, 350, 375)
            move_leg(3, 500, 350, 375)
            move_leg(5, 500, 650, 625)
            uSleep(0.5)

            move_leg(1, 500, 375, 225)
            move_leg(3, 500, 375, 225)
            move_leg(5, 500, 625, 775)

        else:
            move_leg(1, 500, 375, 225)
            move_leg(3, 500, 375, 225)
            move_leg(5, 500, 625, 775)
            uSleep(1)

            move_leg(2, 500, 350, 375)
            move_leg(4, 500, 650, 625)
            move_leg(6, 500, 650, 625)
            uSleep(0.5)

            move_leg(2, 500, 375, 225)
            move_leg(4, 500, 625, 775)
            move_leg(6, 500, 625, 775)
        uSleep(1)

def scan():
    dist = sonar.getDistance()
    print(f"Distance: {dist}")
    return dist

def turn_sensor(turn):
    #utility.turn_sensor(125) = right
    #utility.turn_sensor(875) = left
    board.bus_servo_set_position(0.01, [[21, turn]])
    uSleep(6)
    return scan()

# North = 1, East = 2, South = 3, West = 4
def move_cardinal(blocks, curpos, newdir):
    
    turn_cardinal(curpos[2], newdir)

    reset_legs()

    uSleep(1)

    robot.resting_pos()
    for i in range(blocks):
        walk_block()

    if newdir % 2 == 1:
        return [curpos[0] + blocks * (newdir - 2), curpos[1], newdir]
    else:
        return [curpos[0], curpos[1] + blocks * (newdir - 3) * -1, newdir]

def turn_cardinal(curdir, newdir):
    if newdir == 0:
        newdir = 4
    diffdir = newdir - curdir
    if(abs(diffdir) == 2):
        turn(False, 90)
        turn(False, 90)
    elif(diffdir == 1 or diffdir == -3):
        turn(False, 90)
    elif(diffdir == 3 or diffdir == -1):
        turn(True, 90)

def walk_block():
    for i in range(4):
        robot.tripod_gait(105,7)
    reset_legs()

# maps out the cost of each tile in a given map by their distance from the start
def mapmap(map, goal):
    tileQueue = deque([])
    # North = 1, East = 2, South = 3, West = 4
    for i in range(4):
        if map.getNeighborObstacle(goal[0], goal[1], i+1) == 0:
            tileQueue.append(getTile(goal, i+1))
    
    _mapmap(map, tileQueue)

    map.setCost(goal[0], goal[1], 0)

def _mapmap(map, tileQueue):
    map_size = [map.getCostmapSize(True), map.getCostmapSize(False)]
    cost = 1
    while tileQueue:
        level_size = len(tileQueue)  # Number of tiles at the current depth

        for _ in range(level_size):
            tile = tileQueue.popleft()

            if tile[0] < 0 or tile[1] < 0 or tile[0] >= map_size[0] or tile[1] >= map_size[1]:
                continue  # Ignore out-of-bounds tiles

            # If this tile has already been assigned a lower cost, skip it
            current_cost = map.getCost(tile[0], tile[1])
            if current_cost != 0 and current_cost <= cost:
                continue

            map.setCost(tile[0], tile[1], cost)

            for i in range(4):
                if map.getNeighborObstacle(tile[0], tile[1], i + 1) == 0 and (map.getCost(*getTile(tile, i + 1)) == 0):
                        tileQueue.append(getTile(tile, i + 1))
        
        cost += 1

def explore_map(map, curpos):
    tileQueue = deque([])
    completed = []
    dist = 0

    mapSize = [map.getCostmapSize(True), map.getCostmapSize(False)]

    # North = 1, East = 2, South = 3, West = 4
    for i in range(3):
        dist = turn_sensor(125 + i * 375)
        nextTile = getTile(curpos, curpos[2] - i + 1)
        if dist < 500 :
            map.setObstacle(curpos[0], curpos[1], 1, curpos[2] - i + 1)
        elif 0 <= nextTile[0] and nextTile[0] < mapSize[0] and 0 <= nextTile[1] and nextTile[1] < mapSize[1]:
            tileQueue.append(nextTile)
    
    turn_cardinal(curpos[2], 2)
    curpos[2] = 2
    dist = turn_sensor(125)

    if dist < 500 :
        map.setObstacle(curpos[0], curpos[1], 1, 3)
    else:
        tileQueue.append(getTile(curpos, 3))

    completed.append(curpos)
    
    while tileQueue:
        print(f"Tile queue: {tileQueue}")
        map.clearCostMap()
        tile = tileQueue.pop()
        
        mapmap(map, tile)
        moves = find_path(map, curpos, tile)

        for move in moves:
            curpos = move_cardinal(1, curpos, move)
            reset_legs()

        for i in range(3):
            if not getTile(curpos, curpos[2] - i + 1) in completed:
                dist = turn_sensor(125 + i * 375)
                nextTile = getTile(curpos, curpos[2] - i + 1)
                if dist < 500 :
                    map.setObstacle(curpos[0], curpos[1], 1, curpos[2] - i + 1)
                elif 0 <= nextTile[0] and nextTile[0] < mapSize[0] and 0 <= nextTile[1] and nextTile[1] < mapSize[1]:
                    tileQueue.append(nextTile)
            
            completed.append(curpos)
        map.printCostMap()

def find_path(map, start, goal):
    path = []
    currCost = map.getCost(start[0],start[1])
    currTile = start
    map_size = [map.getCostmapSize(True), map.getCostmapSize(False)]

    while currCost != 0:
        for i in range(4):
            nextTile = getTile(currTile, i + 1)
            if not(nextTile[0] < 0 or nextTile[1] < 0 or nextTile[0] >= map_size[0] or nextTile[1] >= map_size[1]):
                nextCost = map.getCost(nextTile[0], nextTile[1])
                if map.getNeighborObstacle(currTile[0], currTile[1], i + 1) == 0 and currCost > nextCost:
                    path.append(i + 1)
                    currTile = nextTile
                    currCost = nextCost
    
    return path

def getTile(currTile, dir):
    if dir == 1:
        return [currTile[0] - 1, currTile[1]]
    elif dir == 2:
        return [currTile[0], currTile[1] + 1]
    elif dir == 3:
        return [currTile[0] + 1, currTile[1]]
    elif dir == 4 or dir == 0:
        return [currTile[0], currTile[1] - 1]
    
def inputPos():
    pos = input("Please input your start position in the form of 'X,Y,Direction': ").split(",")
    
    if(len(pos) != 3):
        print("invalid string, please input a correct string\n")
        return inputPos()
    
    return [int(pos[0]), int(pos[1]), int(pos[2])]

def start_timer():
    return time.time()

def end_timer(timer):
    return time.time() - timer
