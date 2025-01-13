import time
import sys
import signal
import threading
import ros_robot_controller_sdk as rrc


board = rrc.Board()
start = True

# Assumed leg-motor relations
legs = {
    1: (1, 2, 3),   # Back Left
    2: (4, 5, 6),   # Middle Left
    3: (7, 8, 9),   # Front Left
    4: (10, 11, 12), # Back right?
    5: (13, 14, 15),# Middle right
    6: (16, 17, 18) # Front right?
}

# Set parameters for leg movement
def move_leg(leg_id, horizontal_pos, first_segment_pos, second_segment_pos):
    motor_ids = legs[leg_id]
    board.bus_servo_set_position(1, [[motor_ids[0], horizontal_pos], [motor_ids[1], first_segment_pos], [motor_ids[2], second_segment_pos]])

# Walking sequence
def walk_forward():
    #Tri-pod setup for first set of legs
    move_leg(2, 400, 900, 1000)
    move_leg(4, 750, 900, 1000)
    move_leg(6, 650, 900, 1000)
    time.sleep(0.5)

    move_leg(2, 400, 400, 500)
    move_leg(4, 750, 400, 500)
    move_leg(6, 650, 400, 500)
    time.sleep(1)

    #Lifted legs setup for second set of legs
    move_leg(1, 250, 900, 1000)
    move_leg(3, 350, 900, 1000)
    move_leg(5, 600, 900, 1000)
    time.sleep(0.5)
    
    #Move on first set
    move_leg(2, 600, 400, 500)
    move_leg(4, 300, 400, 500)#Figure out angle to smooth out movement
    move_leg(6, 300, 400, 500)
    time.sleep(1)

    #Stand on second set
    move_leg(1, 250, 400, 500)
    move_leg(3, 350, 400, 500)
    move_leg(5, 600, 400, 500)
    time.sleep(0.5)

    #Lift first set
    move_leg(2, 400, 900, 1000)
    move_leg(4, 750, 900, 1000)
    move_leg(6, 650, 900, 1000)
    time.sleep(0.5)

    #Move on second set
    move_leg(1, 700, 400, 500)
    move_leg(3, 700, 400, 500)
    move_leg(5, 400, 400, 500)
    time.sleep(1)

#Sets all legs to default standing positions
def reset_legs():
    for i in range(6):
        i = i+1
        move_leg(i, 500, 900, 1000)
    time.sleep(1)

def turn(RorL, degree):
    #Will setup degree once turn rate is known
    #for i in range(degree/turn_rate)
    if(RorL):#Turning left
        #Lifted legs and move first set
        move_leg(1, 700, 900, 1000)
        move_leg(3, 700, 900, 1000)
        move_leg(5, 600, 900, 1000)
        time.sleep(0.5)

        move_leg(1, 700, 400, 500)
        move_leg(3, 700, 400, 500)
        move_leg(5, 600, 400, 500)
        time.sleep(1)

        #Lift second set
        move_leg(2, 600, 900, 1000)
        move_leg(4, 750, 900, 1000)
        move_leg(6, 650, 900, 1000)
        time.sleep(0.5)

        #Turn on first
        move_leg(1, 250, 400, 500)
        move_leg(3, 350, 400, 500)
        move_leg(5, 400, 400, 500)
        time.sleep(1)

        #Stand on second
        move_leg(2, 600, 400, 500)
        move_leg(4, 750, 400, 500)
        move_leg(6, 650, 400, 500)
        time.sleep(1)

        #Lift first
        move_leg(1, 700, 900, 1000)
        move_leg(3, 700, 900, 1000)
        move_leg(5, 600, 900, 1000)
        time.sleep(0.5)

        #Move on second
        move_leg(2, 400, 400, 500)
        move_leg(4, 200, 400, 500)
        move_leg(6, 300, 400, 500)
        time.sleep(1)

    else:#turning right
        #Lifted legs and move first set
        move_leg(1, 250, 900, 1000)
        move_leg(3, 350, 900, 1000)
        move_leg(5, 400, 900, 1000)
        time.sleep(0.5)

        move_leg(1, 250, 400, 500)
        move_leg(3, 350, 400, 500)
        move_leg(5, 400, 400, 500)
        time.sleep(1)

        #Lift second set
        move_leg(2, 400, 900, 1000)
        move_leg(4, 200, 900, 1000)
        move_leg(6, 300, 900, 1000)
        time.sleep(0.5)

        #Turn on first
        move_leg(1, 700, 400, 500)
        move_leg(3, 700, 400, 500)
        move_leg(5, 600, 400, 500)
        time.sleep(1)

        #Stand on second
        move_leg(2, 400, 400, 500)
        move_leg(4, 200, 400, 500)
        move_leg(6, 300, 400, 500)
        time.sleep(1)

        #Lift first
        move_leg(1, 250, 900, 1000)
        move_leg(3, 350, 900, 1000)
        move_leg(5, 400, 900, 1000)
        time.sleep(0.5)

        #Move on second
        move_leg(2, 600, 400, 500)
        move_leg(4, 750, 400, 500)
        move_leg(6, 650, 400, 500)
        time.sleep(1)

def safe_leg_move(UorD, ForB, legs):
    for leg in legs:
        segs = [900, 1000]
        if (UorD):
            segs = [400, 500]
        
        match leg:
            case 1:
                if ForB:
                    move_leg(leg, 250, segs[0], segs[1])
                else:
                    move_leg(leg, 700, segs[0], segs[1])
            case 2:
                if ForB:
                    move_leg(leg, 400, segs[0], segs[1])
                else:
                    move_leg(leg, 600, segs[0], segs[1])
            case 3:
                if ForB:
                    move_leg(leg, 350, segs[0], segs[1])
                else:
                    move_leg(leg, 700, segs[0], segs[1])
            case 4:
                if ForB:
                    move_leg(leg, 750, segs[0], segs[1])
                else:
                    move_leg(leg, 300, segs[0], segs[1])
            case 5:
                if ForB:
                    move_leg(leg, 600, segs[0], segs[1])
                else:
                    move_leg(leg, 400, segs[0], segs[1])
            case 6:
                if ForB:
                    move_leg(leg, 650, segs[0], segs[1])
                else:
                    move_leg(leg, 300, segs[0], segs[1])


# Process Before Closing
def Stop(signum, frame):
    global start
    start = False
    print('Closing Process')