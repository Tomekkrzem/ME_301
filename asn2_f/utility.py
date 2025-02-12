import time
from collections import deque
import sys
import signal
import threading
import map_
import ros_robot_controller_sdk as rrc
from sonar import Sonar


board = rrc.Board()
sonar = Sonar()
start = True
speed = 0.1

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
    uSleep(1)

#new turn
def turn(RorL, degree):
    newdeg = min(45, degree)
    differance = int(110 / (45/newdeg))
    if RorL:
        differance -= 7
    forwards = 500 - differance
    backwards = 500 + differance
    if(RorL):#Turning left
        forwards = 500 + differance
        backwards = 500 - differance

    #Lift second set
    move_leg(2, forwards, 350, 375)
    move_leg(4, forwards, 650, 625)
    move_leg(6, forwards, 650, 625)
    uSleep(0.5)

    #Stand on second
    move_leg(2, forwards, 375, 225)
    move_leg(4, forwards, 625, 775)
    move_leg(6, forwards, 625, 775)
    uSleep(1)

    #Lift first
    move_leg(1, forwards, 350, 375)
    move_leg(3, forwards, 350, 375)
    move_leg(5, forwards, 650, 625)
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
    move_leg(2, forwards, 350, 375)
    move_leg(4, forwards, 650, 625)
    move_leg(6, forwards, 650, 625)
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

            move_leg(1, 500, 325, 225)
            move_leg(3, 500, 325, 225)
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

            move_leg(2, 500, 325, 225)
            move_leg(4, 500, 625, 775)
            move_leg(6, 500, 625, 775)
        uSleep(1)

def scan(sonars):
    dists = []
    for son in sonars:
        dists.add(son.get_distance())
    return dists

def turn_sensor(turn):
    #utility.turn_sensor(125) = right
    #utility.turn_sensor(875) = left
    board.bus_servo_set_position(speed, [[21, turn]])

# North = 1, East = 2, South = 3, West = 4
def move_cardinal(blocks, curpos, newdir):
    
    turn_cardinal(curpos[2], newdir)

    for i in range(blocks):
        walk_block()

    if newdir % 2 == 1:
        return [curpos[0] + blocks * (curpos[2] - 2), curpos[1], newdir]
    else:
        return [curpos[0], curpos[1] + blocks * (curpos[3] - 3) * -1, newdir]

def turn_cardinal(curdir, newdir):
    diffdir = newdir - curdir
    if(abs(diffdir) == 2):
        turn(False, 90)
        turn(False, 90)
    elif(diffdir < 0):
        turn(True, 90)
    elif(diffdir > 0):
        turn(False, 90)

def walk_block():
    for i in range(3):
        walk_forward()
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

    
def find_path(map, start, goal):
    path = []
    currCost = map.getCost(start[0],start[1])
    currTile = start
    map_size = [map.getCostmapSize(True), map.getCostmapSize(False)]

    while currCost != 0:
        for i in range(4):
            nextTile = getTile(currTile, i + 1)
            if nextTile[0] < 0 or nextTile[1] < 0 or nextTile[0] >= map_size[0] or nextTile[1] >= map_size[1]:
                continue  # Ignore out-of-bounds tiles

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
    elif dir == 4:
        return [currTile[0], currTile[1] - 1]
    
def inputPos():
    pos = input("Please input your start position in the form of 'X,Y,Direction': ")
    curpos = [0,0,0]
    for i in range(2):
        if pos.index(",") != -1:
            curpos[i] = int(pos[:pos.index(",")])
            pos = pos[pos.index(",") + 1:]
        else:
            print("invalid string, please input a correct string\n")
            return inputPos()
    
    curpos[2] = int(pos)

    return curpos

def start_timer():
    return time.time()

def end_timer(timer):
    return time.time() - timer