import time
import sys
import signal
import threading
import ros_robot_controller_sdk as rrc

board = rrc.Board()
legs = {
    1: (1, 2, 3),       # Back Left
    2: (4, 5, 6),       # Middle Left
    3: (7, 8, 9),       # Front Left
    4: (10, 11, 12),    # Back right
    5: (13, 14, 15),    # Middle right
    6: (16, 17, 18)     # Front right
}

def move_leg(leg_id, horizontal_pos, first_segment_pos, second_segment_pos):
    motor_ids = legs[leg_id]
    board.bus_servo_set_position(1, [[motor_ids[0], horizontal_pos], [motor_ids[1], first_segment_pos], [motor_ids[2], second_segment_pos]])

def resting_pos():

    # Rest Leg 1-3
    for i in range(3):
        move_leg(i, 500, 375, 225)

    for i in range(3,6):
        move_leg(i, 500, 625, 775)

def walk_forward():

    # Leg 1 Lift
    move_leg(1, 500, 425, 275)

    # Leg 2 Twist
    move_leg(2, 600, 375, 225)

    # Leg 3 Lift
    move_leg(3, 500, 425, 275)

    # Leg 4 Push
    move_leg(4, 500, 550, 750)

    # Leg 5 Lift + Twist
    move_leg(5, 600, 700, 775)

    # Leg 6 Pull
    move_leg(6, 500, 675, 700)

    time.sleep(1)

if __name__ == "__main__":
    resting_pos()

    time.sleep(2)

    walk_forward()