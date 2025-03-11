import time
import utility
import knn
import csv
from csv_generator import update_csv

utility.reset_legs()
timer = utility.start_timer()

#utility.walk_block()

train = []

with open('dataset.csv', 'r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        row.reverse()
        row = list(map(int,row))
        train.append(row)
    file.close()

readings = []

for i in range(13):
    turn_angle = 21 * i
    print(f"Angle: {turn_angle}", end=", ")
    readings.append(utility.turn_sensor(turn_angle))

left = False

if((sum(readings) / len(readings)) > 500):
    readings = []
    left = True
    for i in range(13):
        turn_angle = 1000 -  21 * i
        print(f"Angle: {turn_angle}", end=", ")
        readings.append(utility.turn_sensor(turn_angle))

angle = knn.knn(train, readings, 9)
print(f"Correction: {round(angle, 3)}")
time.sleep(2)

#if(angle > 3 or angle < -3):
if angle != 0:
    if(left):
        knn.correction(-angle)
    else:
        knn.correction(angle)
    
timer_data = utility.end_timer(timer)

if left:
    update_csv("labdata.csv",[readings,angle,1,timer_data])
else:
    update_csv("labdata.csv",[readings,angle,0,timer_data])

utility.reset_legs()
