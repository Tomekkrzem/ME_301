import time
import sys
import signal
import threading
import ros_robot_controller_sdk as rrc

board = rrc.Board()
curr_legs = {
        1 : (1, 2, 3),          # Back Left
        2 : (4, 5, 6),          # Middle Left
        3 : (7, 8, 9),          # Front Left
        4 : (10, 11, 12),       # Back Right
        5 : (13, 14, 15),       # Middle Right
        6 : (16, 17, 18)        # Front Right
    }

class Spyder:

    def __init___(self, s_speed, legs):
        
        # Servo Control Speed
        self.s_speed = s_speed

        # Sleep Time
        self.sleep_t = s_speed + 0.1
        
        # Robot Legs
        self.legs = legs

        # Map Servo Range to Degrees
        self.deg_to_serv = lambda x : int(round(1000/180 * x))

    def move_leg(self, leg_id, inner_serv_ang, mid_serv_ang, end_serv_ang):

        # Inner Servo Position
        isp = self.deg_to_serv(inner_serv_ang)

        # Middle Servo Position
        msp = self.deg_to_serv(mid_serv_ang)

        # End Servo Positon
        esp = self.deg_to_serv(end_serv_ang)

        # Leg for Motor Control
        leg = self.legs[leg_id]

        board.bus_servo_set_position(self.s_speed, [leg[0], isp], [leg[1], msp], [leg[2], esp])


    def resting_pos(self):

        for i in range(6):
            
            # Resting Configuration of Each Leg
            # Degrees to Servo Positions
            #    90.0 --> 500
            #   112.5 --> 625
            #   139.5 --> 775    
            self.move_leg(i, 90, 112.5, 139.5)

            # Turns off Servos in Leg
            board.bus_servo_stop([*self.legs[i]])

            i += 1

        print("Resting Position")

    def turn_30(self, R_or_L):
        
        # Reset Robot to Resting Configuration
        self.resting_pos()
        time.sleep(self.sleep_t)

        if R_or_L:  # Turn Right

            # Turn Legs 1, 3, 5 by 30 Degrees to the Right and Lift Them
            self.move_leg(1, 60, 120, 145)
            self.move_leg(3, 60, 120, 145)
            self.move_leg(5, 120, 120, 145)
            time.sleep(self.sleep_t)

            # Drop Legs 1, 3, 5
            self.move_leg(1, 60, 112.5, 139.5)
            self.move_leg(3, 60, 112.5, 139.5)
            self.move_leg(5, 120, 112.5, 139.5)
            time.sleep(self.sleep_t)

            # Lift Legs 2, 4, 6
            self.move_leg(2, 90, 120, 145)
            self.move_leg(4, 90, 120, 145)
            self.move_leg(6, 90, 120, 145)
            time.sleep(self.sleep_t)

            # Straighten Legs 1, 3, 5
            self.move_leg(1, 90, 112.5, 139.5)
            self.move_leg(3, 90, 112.5, 139.5)
            self.move_leg(5, 90, 112.5, 139.5)
            time.sleep(self.sleep_t)

            # Drop Legs 2, 4, 6
            self.move_leg(2, 90, 112.5, 139.5)
            self.move_leg(4, 90, 112.5, 139.5)
            self.move_leg(6, 90, 112.5, 139.5)
            time.sleep(self.sleep_t)

        else:   # Turn Left
            
            # Turn Legs 1, 3, 5 by 30 Degrees to the Left and Lift Them
            self.move_leg(1, 120, 120, 145)
            self.move_leg(3, 120, 120, 145)
            self.move_leg(5, 60, 120, 145)
            time.sleep(self.sleep_t)

            # Drop Legs 1, 3, 5
            self.move_leg(1, 120, 112.5, 139.5)
            self.move_leg(3, 120, 112.5, 139.5)
            self.move_leg(5, 60, 112.5, 139.5)
            time.sleep(self.sleep_t)

            # Lift Legs 2, 4, 6
            self.move_leg(2, 90, 120, 145)
            self.move_leg(4, 90, 120, 145)
            self.move_leg(6, 90, 120, 145)
            time.sleep(self.sleep_t)

            # Straighten Legs 1, 3, 5
            self.move_leg(1, 90, 112.5, 139.5)
            self.move_leg(3, 90, 112.5, 139.5)
            self.move_leg(5, 90, 112.5, 139.5)
            time.sleep(self.sleep_t)

            # Drop Legs 2, 4, 6
            self.move_leg(2, 90, 112.5, 139.5)
            self.move_leg(4, 90, 112.5, 139.5)
            self.move_leg(6, 90, 112.5, 139.5)
            time.sleep(self.sleep_t)

    def turn_90(self, R_or_L):

        for i in range(3):
            self.turn_30(R_or_L)
            i += 1
