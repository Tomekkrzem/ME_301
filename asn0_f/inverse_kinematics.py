import math

def leg_IK(desired_pos):

    coxa = 44.6

    femur = 75.0

    tibia = 126.5

    x, y, z = map(float,desired_pos)

    l = math.sqrt(x**2 + y**2)

    L = math.sqrt(z**2 + (l - coxa)**2)

    gamma = math.degrees(math.atan2(x,y))

    alpha1 = math.acos(z/L)

    alpha2 = math.acos((tibia**2 - femur**2 - L**2)/(-2 * femur * L))

    alpha = math.degrees(alpha1 + alpha2)

    beta = math.degrees(math.acos((L**2 - tibia**2 - femur**2)/(-2 * tibia * femur)))


    return (120 - gamma, alpha, 270 - beta)



f_b_ang = 74.5


x = 50 
y = 150

x_p = x * math.cos(f_b_ang) - y * math.sin(f_b_ang)
y_p = x * math.sin(f_b_ang) + y * math.cos(f_b_ang)

t1,t2,t3 = leg_IK((50,150,25))
print(t1,t2,t3)

t1,t2,t3 = leg_IK((25,150,25))
print(t1,t2,t3)

t1,t2,t3 = leg_IK((0,150,25))
print(t1,t2,t3)

t1,t2,t3 = leg_IK((-25,150,25))
print(t1,t2,t3)

t1,t2,t3 = leg_IK((-50,150,25))
print(t1,t2,t3)


print('\n')

x_p1 = 50 * math.cos(f_b_ang) - 150 * math.sin(f_b_ang)
y_p1 = 50 * math.sin(f_b_ang) + 150 * math.cos(f_b_ang)
t1,t2,t3 = leg_IK((x_p1,y_p1,25))
print(t1,t2,t3)

x_p2 = 25 * math.cos(f_b_ang) - 150 * math.sin(f_b_ang)
y_p2 = 25 * math.sin(f_b_ang) + 150 * math.cos(f_b_ang)
t1,t2,t3 = leg_IK((x_p2,y_p2,25))
print(t1,t2,t3)

x_p3 = 0 * math.cos(f_b_ang) - 150 * math.sin(f_b_ang)
y_p3 = 0 * math.sin(f_b_ang) + 150 * math.cos(f_b_ang)
t1,t2,t3 = leg_IK((x_p3,y_p3,25))
print(t1,t2,t3)

x_p4 = -25 * math.cos(f_b_ang) - 150 * math.sin(f_b_ang)
y_p4 = -25 * math.sin(f_b_ang) + 150 * math.cos(f_b_ang)
t1,t2,t3 = leg_IK((x_p4,y_p4,25))
print(t1,t2,t3)

x_p5 = -50 * math.cos(f_b_ang) - 150 * math.sin(f_b_ang)
y_p5 = -50 * math.sin(f_b_ang) + 150 * math.cos(f_b_ang)
t1,t2,t3 = leg_IK((x_p5,y_p5,25))
print(t1,t2,t3)
