import time
import sys
import signal
import threading
import math

# import matplotlib.pyplot as plt

import ros_robot_controller_sdk as rrc
from sonar import Sonar

board = rrc.Board()
s = Sonar()


def rotate_2D(pos, rot_ang):
    x = pos[0]
    y = pos[1]
    rad_ang = math.radians(rot_ang)
    x_p = x * math.cos(rad_ang) + y * math.sin(rad_ang)
    y_p = -x * math.sin(rad_ang) + y * math.cos(rad_ang)

    return round(x_p), round(y_p)


def leg_IK(leg_id, desired_pos):
    # print(desired_pos)

    add = 120

    if leg_id in [1, 4]: add = -120

    coxa = 44.6

    femur = 75.0

    tibia = 126.5

    x, y, z = map(float, desired_pos)

    l = math.sqrt(x ** 2 + y ** 2)

    L = math.sqrt(z ** 2 + (l - coxa) ** 2)

    gamma = math.degrees(math.atan2(x, y))

    alpha1 = math.acos(z / L)

    alpha2 = math.acos((tibia ** 2 - femur ** 2 - L ** 2) / (-2 * femur * L))

    alpha = math.degrees(alpha1 + alpha2)

    beta = math.degrees(math.acos((L ** 2 - tibia ** 2 - femur ** 2) / (-2 * tibia * femur)))

    print(leg_id, round(120 + gamma), round(alpha), round(120 - beta + 180))

    return round(abs(add + gamma)), round(120 + alpha - 90), round(120 - beta + 180)


def body_IK(body_offsets, desired_pos):
    foot_to_body = []

    for leg in range(6):
        x_off = body_offsets[leg][0]
        y_off = body_offsets[leg][1]
        angle_off = body_offsets[leg][2]

    pass


def linear_interpol(leg_id, pos_i, pos_f, rot_ang, res):
    x_i, y_i = rotate_2D(pos_i[:2], rot_ang)
    x_f, y_f = rotate_2D(pos_f[:2], rot_ang)
    z = pos_i[2]

    # List of Leg Angles
    walk_path = []

    # List of X Points for Foot
    x_list = []
    # List of Z Points for Foot
    z_list = []
    # List of Y Points for Foot
    y_list = []

    move_x = abs(x_f - x_i) / (res - 1)
    move_y = abs(y_f - y_i) / (res - 1)

    curr_x = round(x_i)
    curr_y = round(y_i)
    for i in range(res):
        print(curr_x)
        print(curr_y)
        # Updating Leg Angles
        walk_path.append((leg_id, *leg_IK(leg_id, (curr_x, curr_y, z))))

        # Updating List of Foot Positions
        x_list.append(curr_x)
        y_list.append(curr_y)
        z_list.append(z)

        # Updating x and y Coordinates for Foot
        curr_x = round(curr_x - move_x)
        curr_y = round(curr_y - move_y)
        i += 1

    if leg_id == 1 or leg_id == 4:
        walk_path.reverse()
        x_list.reverse()
        y_list.reverse()
        z_list.reverse()

    return walk_path, x_list, y_list, z_list


def bezier_curve(leg_id, points, res):
    t_range = [i / (res - 1) for i in range(res)]
    x_list = []
    y_list = []
    z_list = []
    xyz_list = []

    for t in t_range:
        x, y, z = 0, 0, 0
        for i, (px, py, pz) in enumerate(points):
            weight = (math.comb(len(points) - 1, i) * (t ** i) * ((1 - t) ** (len(points) - 1 - i)))
            x += weight * px
            z += weight * pz
            y += weight * py

        x_list.append(round(x))
        y_list.append(round(y))
        z_list.append(round(z))
        xyz_list.append((leg_id, *leg_IK(leg_id, (round(x), round(y), round(z)))))

    if leg_id == 1 or leg_id == 4:
        x_list.reverse()
        y_list.reverse()
        z_list.reverse()
        xyz_list.reverse()
        return x_list, y_list, z_list, xyz_list

    return x_list, y_list, z_list, xyz_list


# def plot_angles(leg, walk, ax):
#     inner = [["I" + str(c), i[1]] for c, i in enumerate(walk)]
#     middle = [["M" + str(c), i[2]] for c, i in enumerate(walk)]
#     outer = [["O" + str(c), i[3]] for c, i in enumerate(walk)]
#
#     ax.axhline(y=240, color='red', linestyle='--', label=f'Threshold: {240}')
#     ax.bar([i[0] for i in inner], [i[1] for i in inner], label="Inner")
#     ax.bar([i[0] for i in middle], [i[1] for i in middle], label="Middle")
#     ax.bar([i[0] for i in outer], [i[1] for i in outer], label="Outer")
#
#     ax.set_title(f"Joint Angles for Leg {leg}")
#     ax.set_xlabel("Servos")
#     ax.set_ylabel("Angle (deg)")


class Spyder:

    def __init__(self, s_speed):

        # Servo Control Speed
        self.s_speed = s_speed

        # Sleep Time
        self.sleep_t = s_speed + 0.01

        # Robot Legs
        self.legs = {
            1: (1, 2, 3),  # Back Left
            2: (4, 5, 6),  # Middle Left
            3: (7, 8, 9),  # Front Left
            4: (10, 11, 12),  # Back Right
            5: (13, 14, 15),  # Middle Right
            6: (16, 17, 18)  # Front Right
        }

        # Map Servo Range to Degrees for Right Leg
        self.deg_to_serv_r = lambda x: int(round(1000 / 240 * x))

        # Map Servo Range to Degrees for Left Leg
        self.deg_to_serv_l = lambda x: int(round(1000 - 1000 / 240 * x))

        # self.foot_offsets = {1 : (-58.5, -119.5, -45),
        #                   2 : (-91.5, 0, 0),
        #                   3 : (-58.5, 119.5, -45),
        #                   4 : (58.5, -119.5, -45),
        #                   5 : (91.5, 0, 0),
        #                   6 : (58.5, 119.5, -45)}

        self.servo_offset = {1: -45,
                             2: 0,
                             3: -45,
                             4: -45,
                             5: 0,
                             6: -45}

        # Turn on Sonar LED
        s.setRGBMode(0)

        # Set Left Sonar to Red
        s.setPixelColor(0, (255, 0, 0))

        # Set Right Sonar to Red
        s.setPixelColor(1, (255, 0, 0))

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

            leg_joints = [[leg[0], isp], [leg[1], msp], [leg[2], esp]]
            for i in range(3):
                leg_drive_list.append(leg_joints[i])
                i += 1

        board.bus_servo_set_position(self.s_speed, leg_drive_list)

    def resting_pos(self):

        print("\nResting Position")

        for i in range(6):
            # Resting Configuration of Each Leg
            # Degrees to Servo Positions
            #    90.0 --> 500
            #   112.5 --> 625
            #   139.5 --> 775

            # Old Rest Position
            # self.move_legs([[i+1, 120, 150, 186]])
            self.move_legs([[i + 1, 120, 154, 186]])

            i += 1

        print("\n")

    def compose_walk(self, leg, start_pos, end_pos, p_lst, res):

        rot_ang = self.servo_offset[leg]

        if leg in [1, 3, 4, 6]:
            start_pos = [start_pos[0] + 70, start_pos[1] - 17, start_pos[2]]
            end_pos = [end_pos[0] + 70, end_pos[1] - 17, end_pos[2]]
            p_lst = [(p[0] + 70, p[1] - 17, p[2]) for p in p_lst]

        move_path = linear_interpol(leg, start_pos, end_pos, rot_ang, res)[0]

        raise_points = [(*rotate_2D([point[0], point[1]], rot_ang), point[2]) for point in p_lst]

        print(raise_points)

        raise_path = bezier_curve(leg, raise_points, res)[-1]

        if leg in [2, 4, 6]:
            return [*raise_path, *move_path]
        else:
            return [*move_path, *raise_path]

    def tripod_gait(self, travel_dist, res):

        y_dist = 191

        s_pos = [travel_dist / 2, y_dist, 17]
        e_pos = [-travel_dist / 2, y_dist, 17]

        P_List = [(-travel_dist / 2, y_dist, -25),
                  ((-travel_dist / 2 - 25), y_dist, -30),
                  ((-travel_dist / 2 - 50), y_dist, -50),
                  (0, y_dist, -100),
                  ((travel_dist / 2 + 50), y_dist, -50),
                  ((travel_dist / 2 + 25), y_dist, -30),
                  (travel_dist / 2, y_dist, -25)]

        leg_paths = [self.compose_walk(leg + 1, s_pos, e_pos, P_List, res) for leg in range(6)]

        count = 3
        walk_complete = False

        while not walk_complete:
            if count == res * 2: count = 0
            print(count)
            walk_points = []
            for leg in leg_paths:
                walk_points.append(leg[count])

            self.move_legs(walk_points)
            count += 1
            time.sleep(self.sleep_t)
            if count == 3: walk_complete = True

        return


if __name__ == "__main__":
    robot = Spyder(0.047)

    robot.resting_pos()




