import numpy as np


def leg_IK(desired_pos):
    coxa = 44.6

    femur = 75.0

    tibia = 126.5

    x, y, z = map(float, desired_pos)

    l = np.sqrt(x ** 2 + y ** 2)

    L = np.sqrt(z ** 2 + (l - coxa) ** 2)

    gamma = np.degrees(np.atan2(x, y))

    alpha1 = np.acos(z / L)

    alpha2 = np.acos((tibia ** 2 - femur ** 2 - L ** 2) / (-2 * femur * L))

    alpha = np.degrees(alpha1 + alpha2)

    beta = np.degrees(np.acos((L ** 2 - tibia ** 2 - femur ** 2) / (-2 * tibia * femur)))

    return (round(120 + gamma), round(alpha), round(270 - beta))


def linear_interpol(x_i, y_i, x_f, y_f, res):
    walk_path = []
    z_height = 25

    # print(x_i)
    # print(y_i)

    # print(x_f)
    # print(y_f)

    move_x = abs(x_f - x_i) / res
    move_y = abs(y_f - y_i) / res

    curr_x = x_i
    curr_y = y_i
    for i in range(res + 1):
        walk_path.append(leg_IK((curr_x, curr_y, z_height)))
        curr_x = curr_x - move_x
        curr_y = curr_y - move_y
        i = i + 1

    return (walk_path)


def rotate_2D(x, y, rot_ang):
    rad_ang = np.radians(rot_ang)
    x_p = x * np.cos(rad_ang) + y * np.sin(rad_ang)
    y_p = -x * np.sin(rad_ang) + y * np.cos(rad_ang)

    return round(x_p), round(y_p)


p1 = rotate_2D(150, 100, 45)
p2 = rotate_2D(-125, 100, 45)

print(linear_interpol(150, 175, -150, 175, 3))
print(linear_interpol(*rotate_2D(150, 150, -45), *rotate_2D(-150, 150, -45), 5))