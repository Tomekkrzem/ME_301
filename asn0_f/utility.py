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
        if(i < 4):
            move_leg(i, 500, 375, 225)
        else:
            move_leg(i, 500, 625, 775)
    time.sleep(1)

def turn(RorL, degree):
    #Will setup degree once turn rate is known
    for i in range(int(degree/45)):
        if(RorL):#Turning left
            #Lift second set
            move_leg(2, 600, 350, 500)
            move_leg(4, 600, 650, 500)
            move_leg(6, 600, 650, 500)
            time.sleep(0.5)

            #Stand on second
            move_leg(2, 600, 375, 225)
            move_leg(4, 600, 625, 775)
            move_leg(6, 600, 625, 775)
            time.sleep(1)

            #Lift first
            move_leg(1, 600, 350, 500)
            move_leg(3, 600, 350, 500)
            move_leg(5, 600, 650, 500)
            time.sleep(0.5)

            #Turn on second
            move_leg(2, 400, 375, 225)
            move_leg(4, 400, 625, 775)
            move_leg(6, 400, 625, 775)
            time.sleep(1)

            #Stand on first
            move_leg(1, 600, 375, 225)
            move_leg(3, 600, 375, 225)
            move_leg(5, 600, 625, 775)
            time.sleep(1)

            #Lift second set
            move_leg(2, 600, 350, 500)
            move_leg(4, 600, 650, 500)
            move_leg(6, 600, 650, 500)
            time.sleep(0.5)

            #Turn on first
            move_leg(1, 400, 375, 225)
            move_leg(3, 400, 375, 225)
            move_leg(5, 400, 625, 775)
            time.sleep(1)

        else:#turning right
            #Lifted legs and move first set
            move_leg(1, 400, 350, 500)
            move_leg(3, 400, 350, 500)
            move_leg(5, 400, 650, 500)
            time.sleep(0.5)

            move_leg(1, 400, 375, 225)
            move_leg(3, 400, 375, 225)
            move_leg(5, 400, 625, 775)
            time.sleep(1)

            #Lift second set
            move_leg(2, 400, 350, 500)
            move_leg(4, 400, 650, 500)
            move_leg(6, 400, 650, 500)
            time.sleep(0.5)

            #Turn on first
            move_leg(1, 600, 375, 225)
            move_leg(3, 600, 375, 225)
            move_leg(5, 600, 625, 775)
            time.sleep(1)

            #Stand on second
            move_leg(2, 400, 375, 225)
            move_leg(4, 400, 625, 775)
            move_leg(6, 400, 625, 775)
            time.sleep(1)

            #Lift first
            move_leg(1, 400, 350, 500)
            move_leg(3, 400, 350, 500)
            move_leg(5, 400, 650, 500)
            time.sleep(0.5)

            #Turn on second
            move_leg(2, 600, 375, 225)
            move_leg(4, 600, 625, 775)
            move_leg(6, 600, 625, 775)
            time.sleep(1)

    #reset on legs
    if(RorL):
        move_leg(2, 500, 375, 225)
        move_leg(4, 500, 625, 775)
        move_leg(6, 500, 625, 775)
        time.sleep(1)

        move_leg(1, 500, 350, 500)
        move_leg(3, 500, 350, 500)
        move_leg(5, 500, 650, 500)
        time.sleep(0.5)

        move_leg(1, 500, 325, 225)
        move_leg(3, 500, 325, 225)
        move_leg(5, 500, 625, 775)

    else:
        move_leg(1, 500, 375, 225)
        move_leg(3, 500, 375, 225)
        move_leg(5, 500, 625, 775)
        time.sleep(1)

        move_leg(2, 500, 350, 500)
        move_leg(4, 500, 650, 500)
        move_leg(6, 500, 650, 500)
        time.sleep(0.5)

        move_leg(2, 500, 325, 225)
        move_leg(4, 500, 625, 775)
        move_leg(6, 500, 625, 775)
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