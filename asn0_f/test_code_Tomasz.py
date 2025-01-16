import time
import sys
import signal
import threading
# import ros_robot_controller_sdk as rrc

# board = rrc.Board()
curr_legs = {
        1 : (1, 2, 3),          # Back Left
        2 : (4, 5, 6),          # Middle Left
        3 : (7, 8, 9),          # Front Left
        4 : (10, 11, 12),       # Back Right
        5 : (13, 14, 15),       # Middle Right
        6 : (16, 17, 18)        # Front Right
    }

class Spyder:

    def __init__(self, s_speed, legs):
        
        # Servo Control Speed
        self.s_speed = s_speed

        # Sleep Time
        self.sleep_t = s_speed + 0.1
        
        # Robot Legs
        self.legs = legs

        # Map Servo Range to Degrees for Right Leg
        self.deg_to_serv_r = lambda x : int(round(1000/240 * x))

        # Map Servo Range to Degrees for Left Leg
        self.deg_to_serv_l = lambda x : int(round(1000 - 1000/240 * x))


    def move_leg(self, leg_id, inner_serv_ang, mid_serv_ang, end_serv_ang):

        if leg_id > 3:
            # Inner Servo Position
            isp = self.deg_to_serv_r(inner_serv_ang)

            # Middle Servo Position
            msp = self.deg_to_serv_r(mid_serv_ang)

            # End Servo Positon
            esp = self.deg_to_serv_r(end_serv_ang)
        else:
            # Inner Servo Position
            isp = self.deg_to_serv_l(inner_serv_ang)

            # Middle Servo Position
            msp = self.deg_to_serv_l(mid_serv_ang)

            # End Servo Positon
            esp = self.deg_to_serv_l(end_serv_ang)

        # Leg for Motor Control
        leg = self.legs[leg_id]

        # board.bus_servo_set_position(self.s_speed, [leg[0], isp], [leg[1], msp], [leg[2], esp])

        print(leg_id, [leg[0], isp], [leg[1], msp], [leg[2], esp])


    def resting_pos(self):
        
        print("\nResting Position")

        for i in range(6):

            # Resting Configuration of Each Leg
            # Degrees to Servo Positions
            #    90.0 --> 500
            #   112.5 --> 625
            #   139.5 --> 775    
            self.move_leg(i+1, 120, 150, 186)

            # Turns off Servos in Leg
            # board.bus_servo_stop([*self.legs[i]])

            i += 1

        print("\n")

    def turn_30(self, R_or_L, num_turns):
        
        # Reset Robot to Resting Configuration
        self.resting_pos()
        time.sleep(self.sleep_t)

        if R_or_L:  # Turn Right
            
            alternate_cycle_r = False
            i = 0

            while i != num_turns:
                if not alternate_cycle_r:
                    # Turn and Lift Legs 2, 4, 6 by 30 Degrees
                    self.move_leg(2, 160.19, 160, 180)
                    self.move_leg(4, 166.02, 160, 180)
                    self.move_leg(6, 160.9, 160, 180)
                    time.sleep(self.sleep_t)

                    # Drop Legs 2, 4, 6
                    self.move_leg(2, 160.19, 150, 186)
                    self.move_leg(4, 166.02, 150, 186)
                    self.move_leg(6, 160.9, 150, 186)
                    time.sleep(self.sleep_t)

                    # Lift Leg 1, 3, 5
                    self.move_leg(1, 120, 160, 180)
                    self.move_leg(3, 120, 160, 180)
                    self.move_leg(5, 120, 160, 180)
                    time.sleep(self.sleep_t)

                    # Restore Legs 2, 4, 6
                    self.move_leg(2, 120, 150, 186)
                    self.move_leg(4, 120, 150, 186)
                    self.move_leg(6, 120, 150, 186)
                    time.sleep(self.sleep_t)

                    i += 1
                    alternate_cycle_r = True
                    print("\n")

                else:

                    # Turn and Lift Legs 1, 3, 5 by 30 Degrees
                    self.move_leg(1, 160.19, 160, 180)
                    self.move_leg(3, 166.02, 160, 180)
                    self.move_leg(5, 160.9, 160, 180)
                    time.sleep(self.sleep_t)

                    # Drop Legs 1, 3, 5
                    self.move_leg(1, 160.19, 150, 186)
                    self.move_leg(3, 166.02, 150, 186)
                    self.move_leg(5, 160.9, 150, 186)
                    time.sleep(self.sleep_t)

                    # Lift Leg 2, 4, 6
                    self.move_leg(2, 120, 160, 180)
                    self.move_leg(4, 120, 160, 180)
                    self.move_leg(6, 120, 160, 180)
                    time.sleep(self.sleep_t)

                    # Restore Legs 1, 3, 5
                    self.move_leg(1, 120, 150, 186)
                    self.move_leg(3, 120, 150, 186)
                    self.move_leg(5, 120, 150, 186)
                    time.sleep(self.sleep_t)

                    i += 1
                    alternate_cycle_r = False
                    print("\n")

            self.resting_pos()

        else:   # Turn Left

            alternate_cycle_l = False
            i = 0

            while i != num_turns:
                if not alternate_cycle_l:
                    # Turn and Lift Legs 2, 4, 6 by 30 Degrees
                    self.move_leg(2, 79.81, 160, 180)
                    self.move_leg(4, 73.98, 160, 180)
                    self.move_leg(6, 79.91, 160, 180)
                    time.sleep(self.sleep_t)

                    # Drop Legs 2, 4, 6
                    self.move_leg(2, 79.81, 150, 186)
                    self.move_leg(4, 73.98, 150, 186)
                    self.move_leg(6, 79.91, 150, 186)
                    time.sleep(self.sleep_t)

                    # Lift Leg 1, 3, 5
                    self.move_leg(1, 120, 160, 180)
                    self.move_leg(3, 120, 160, 180)
                    self.move_leg(5, 120, 160, 180)
                    time.sleep(self.sleep_t)

                    # Restore Legs 2, 4, 6
                    self.move_leg(2, 120, 150, 186)
                    self.move_leg(4, 120, 150, 186)
                    self.move_leg(6, 120, 150, 186)
                    time.sleep(self.sleep_t)

                    i += 1
                    alternate_cycle_l = True
                    print("\n")

                else:

                    # Turn and Lift Legs 1, 3, 5 by 30 Degrees
                    self.move_leg(1, 79.81, 160, 180)
                    self.move_leg(3, 73.98, 160, 180)
                    self.move_leg(5, 79.91, 160, 180)
                    time.sleep(self.sleep_t)

                    # Drop Legs 1, 3, 5
                    self.move_leg(1, 79.81, 150, 186)
                    self.move_leg(3, 73.98, 150, 186)
                    self.move_leg(5, 79.91, 150, 186)
                    time.sleep(self.sleep_t)

                    # Lift Leg 2, 4, 6
                    self.move_leg(2, 120, 160, 180)
                    self.move_leg(4, 120, 160, 180)
                    self.move_leg(6, 120, 160, 180)
                    time.sleep(self.sleep_t)

                    # Restore Legs 1, 3, 5
                    self.move_leg(1, 120, 150, 186)
                    self.move_leg(3, 120, 150, 186)
                    self.move_leg(5, 120, 150, 186)
                    time.sleep(self.sleep_t)

                    i += 1
                    alternate_cycle_l = False
                    print("\n")

            self.resting_pos()
            
    def turn_90(self, R_or_L):

        self.turn_30(R_or_L,3)






if __name__ == "__main__":
    robot = Spyder(0.25,curr_legs)

    robot.resting_pos()
    print("\n")

    robot.turn_30(1,1)
    print("Right 30 Degree Turn Complete")

    robot.turn_30(0,1)
    print("Left 30 Degree Turn Complete")

    robot.turn_90(1)
    print("Right 90 Degree Turn Complete")

    robot.turn_90(0)
    print("Left 90 Degree Turn Complete")