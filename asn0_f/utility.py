import time
import sys
import signal
import threading
import ros_robot_controller_sdk as rrc
from sonar import Sonar


board = rrc.Board()
sonar = Sonar()
start = True
speed = 0.375

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
    move_leg(1, 300, 350, 500)
    move_leg(3, 550, 350, 500)
    move_leg(5, 600, 650, 500)
    uSleep(0.5)

    move_leg(1, 300, 375, 225)
    move_leg(3, 550, 375, 225)
    move_leg(5, 600, 625, 775)
    uSleep(1)

    #Lift second set
    move_leg(2, 400, 350, 500)
    move_leg(4, 700, 650, 500)
    move_leg(6, 600, 650, 500)
    uSleep(0.5)

    #Move on first
    move_leg(1, 500, 375, 225)
    move_leg(3, 700, 375, 225)
    move_leg(5, 400, 625, 775)
    uSleep(1)

    #Stand on second
    move_leg(2, 400, 375, 225)
    move_leg(4, 700, 625, 775)
    move_leg(6, 600, 625, 775)
    uSleep(1)


    #Lift first
    move_leg(1, 300, 350, 500)
    move_leg(3, 550, 350, 500)
    move_leg(5, 600, 650, 500)
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

def turn(RorL, degree):
    #Will setup degree once turn rate is known
    for i in range(int(degree/45)):
        if(RorL):#Turning left
            #Lift second set
            move_leg(2, 600, 350, 500)
            move_leg(4, 600, 650, 500)
            move_leg(6, 600, 650, 500)
            uSleep(0.5)

            #Stand on second
            move_leg(2, 600, 375, 225)
            move_leg(4, 600, 625, 775)
            move_leg(6, 600, 625, 775)
            uSleep(1)

            #Lift first
            move_leg(1, 600, 350, 500)
            move_leg(3, 600, 350, 500)
            move_leg(5, 600, 650, 500)
            uSleep(0.5)

            #Turn on second
            move_leg(2, 400, 375, 225)
            move_leg(4, 400, 625, 775)
            move_leg(6, 400, 625, 775)
            uSleep(1)

            #Stand on first
            move_leg(1, 600, 375, 225)
            move_leg(3, 600, 375, 225)
            move_leg(5, 600, 625, 775)
            uSleep(1)

            #Lift second set
            move_leg(2, 600, 350, 500)
            move_leg(4, 600, 650, 500)
            move_leg(6, 600, 650, 500)
            uSleep(0.5)

            #Turn on first
            move_leg(1, 400, 375, 225)
            move_leg(3, 400, 375, 225)
            move_leg(5, 400, 625, 775)
            uSleep(1)

        else:#turning right
            #Lifted legs and move first set
            move_leg(1, 400, 350, 500)
            move_leg(3, 400, 350, 500)
            move_leg(5, 400, 650, 500)
            uSleep(0.5)

            move_leg(1, 400, 375, 225)
            move_leg(3, 400, 375, 225)
            move_leg(5, 400, 625, 775)
            uSleep(1)

            #Lift second set
            move_leg(2, 400, 350, 500)
            move_leg(4, 400, 650, 500)
            move_leg(6, 400, 650, 500)
            uSleep(0.5)

            #Turn on first
            move_leg(1, 600, 375, 225)
            move_leg(3, 600, 375, 225)
            move_leg(5, 600, 625, 775)
            uSleep(1)

            #Stand on second
            move_leg(2, 400, 375, 225)
            move_leg(4, 400, 625, 775)
            move_leg(6, 400, 625, 775)
            uSleep(1)

            #Lift first
            move_leg(1, 400, 350, 500)
            move_leg(3, 400, 350, 500)
            move_leg(5, 400, 650, 500)
            uSleep(0.5)

            #Turn on second
            move_leg(2, 600, 375, 225)
            move_leg(4, 600, 625, 775)
            move_leg(6, 600, 625, 775)
            uSleep(1)

    #reset on legs
    if(RorL):
        move_leg(2, 500, 375, 225)
        move_leg(4, 500, 625, 775)
        move_leg(6, 500, 625, 775)
        uSleep(1)

        move_leg(1, 500, 350, 500)
        move_leg(3, 500, 350, 500)
        move_leg(5, 500, 650, 500)
        uSleep(0.5)

        move_leg(1, 500, 325, 225)
        move_leg(3, 500, 325, 225)
        move_leg(5, 500, 625, 775)

    else:
        move_leg(1, 500, 375, 225)
        move_leg(3, 500, 375, 225)
        move_leg(5, 500, 625, 775)
        uSleep(1)

        move_leg(2, 500, 350, 500)
        move_leg(4, 500, 650, 500)
        move_leg(6, 500, 650, 500)
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

def start_timer():
    return time.time() * 1000

def end_timer(timer):
    return (time.time() * 1000) - timer