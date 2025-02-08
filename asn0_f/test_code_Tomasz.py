import time
import sys
import signal
import threading
import numpy as np
import matplotlib.pyplot as plt
# import ros_robot_controller_sdk as rrc
# from sonar import Sonar

# board = rrc.Board()
# s = Sonar()

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

        # # Turn on Sonar LED
        # s.setRGBMode(0)

        # # Set Left Sonar to Red
        # s.setPixelColor(0,(255,0,0))

        # # Set Right Sonar to Red
        # s.setPixelColor(1,(255,0,0))


    def move_legs(self, lst_of_legs):
        
        leg_drive_list = []
        for curr_leg in lst_of_legs:

            leg_id = curr_leg[0]
            inner_serv_ang = curr_leg[1]
            mid_serv_ang = curr_leg[2]
            end_serv_ang = curr_leg[3]

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

            leg = self.legs[leg_id]
            
            leg_joints = [[leg[0],isp],[leg[1],msp],[leg[2],esp]]
            for i in range(3):
                leg_drive_list.append(leg_joints[i])
                i += 1

        # board.bus_servo_set_position(self.s_speed, leg_drive_list)

        print(leg_drive_list)

    import numpy as np

    def leg_IK(self,leg_id,desired_pos):
        if leg_id == 1 or leg_id == 4:
            gamma_add = -120
        else:
            gamma_add = 120
            
        coxa = 44.6

        femur = 75.0

        tibia = 126.5

        x, y, z = map(float,desired_pos)

        l = np.sqrt(x**2 + y**2)

        L = np.sqrt(z**2 + (l - coxa)**2)

        gamma = np.degrees(np.atan2(x,y))

        alpha1 = np.acos(z/L)

        alpha2 = np.acos((tibia**2 - femur**2 - L**2)/(-2 * femur * L))

        alpha = np.degrees(alpha1 + alpha2)

        beta = np.degrees(np.acos((L**2 - tibia**2 - femur**2)/(-2 * tibia * femur)))

        return (round(abs(gamma_add + gamma)), round(alpha), round(270 - beta))

    def linear_interpol(self,leg_id,x_i,y_i,x_f,y_f,res):
        walk_path = []
        z_height = 25
        
        move_x = abs(x_f-x_i)/res
        move_y = abs(y_f-y_i)/res

        curr_x = x_i
        curr_y = y_i
        for i in range(res+1):
            walk_path.append((leg_id,*self.leg_IK(leg_id,(curr_x,curr_y,z_height))))
            curr_x = curr_x-move_x
            curr_y = curr_y-move_y
            i+=1

        if leg_id == 1 or leg_id == 4:
            walk_path.reverse()

        print(walk_path)
        return(walk_path)

    def rotate_2D(self,x,y,rot_ang):
        rad_ang = np.radians(rot_ang)
        x_p = x * np.cos(rad_ang) + y * np.sin(rad_ang)
        y_p = -x * np.sin(rad_ang) + y * np.cos(rad_ang)

        return round(x_p), round(y_p)

    def resting_pos(self):
        
        print("\nResting Position")

        for i in range(6):

            # Resting Configuration of Each Leg
            # Degrees to Servo Positions
            #    90.0 --> 500
            #   112.5 --> 625
            #   139.5 --> 775    
            self.move_legs([[i+1, 120, 150, 186]])

            i += 1

        print("\n")
    
    def compose_walk(self):

        # Lift Leg From Rest 

        # First-Half Raising Parabolic Motion 

        # Linear Moving Motion

        # Second-Half Parabolic Raising Motion


        pass

    def tripod_gait(self):
        pass


if __name__ == "__main__":
    robot = Spyder(0.25,curr_legs)

    robot.resting_pos()
    #print("\n")

    walk_leg1 = robot.linear_interpol(1,*robot.rotate_2D(150,190,-45),*robot.rotate_2D(-150,190,-45),7)
    walk_leg2 = robot.linear_interpol(2,*robot.rotate_2D(150,190,0),*robot.rotate_2D(-150,190,0),7)
    walk_leg3 = robot.linear_interpol(3,*robot.rotate_2D(150,190,-45),*robot.rotate_2D(-150,190,-45),7)
    walk_leg4 = robot.linear_interpol(4,*robot.rotate_2D(150,190,-45),*robot.rotate_2D(-150,190,-45),7)
    walk_leg5 = robot.linear_interpol(5,*robot.rotate_2D(150,190,0),*robot.rotate_2D(-150,190,0),7)
    walk_leg6 = robot.linear_interpol(6,*robot.rotate_2D(150,190,-45),*robot.rotate_2D(-150,190,-45),7)
    
    inner = [["I" + str(i),i[1]] for i in walk_leg1]
    middle = [["M" + str(i),i[2]] for i in walk_leg1]
    outer = [["O" + str(i),i[3]] for i in walk_leg1]

    plt.bar([i[0] for i in inner],[i[1] for i in inner])
    plt.bar([i[0] for i in middle],[i[1] for i in middle])
    plt.bar([i[0] for i in outer],[i[1] for i in outer])
    plt.show()
    
    print(robot.leg_IK(2,(0,190,50)))


    # robot.move_legs(walk_leg1)
    