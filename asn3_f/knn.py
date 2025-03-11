import math
import csv
import numpy as np
from utility import turn

def knn(x_train, x_Test, k):
    
    neighbors = []
    for x in x_train:
        x_temp = x[-1]
        x = [y for i,y in enumerate(x[:-1]) if i%5 != 0]
        x.append(x_temp)
        x_test = [x for i,x in enumerate(x_Test) if i%5 != 0]

        # x_test = x_Test

        # d = euclid_dist(x,x_test)
        d = cosine_dist(x,x_test)
        if len(neighbors) < k:
            neighbors.append([d,x])
        elif d < max([dist[0] for dist in neighbors]):
            max_d = max([dist[0] for dist in neighbors])
            count = 0
            for j in range(len(neighbors)):
                if max_d not in neighbors[j]:
                    count += 1
                else:
                    break

            neighbors[count] = [d,x]
    return sum([goal[-1] for d, goal in neighbors]) / k

def euclid_dist(p1,p2):
    d = 0
    for i in range(len(p2)):
        d += (p2[i] - p1[i])**2

    return math.sqrt(d)

def cosine_dist(p1,p2):
    return float(1 - (np.dot(p1[:-1],p2) / (np.linalg.norm(p1[:-1]) * np.linalg.norm(p2))))

train = []

with open('dataset.csv', 'r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        row.reverse()
        row = list(map(int,row))
        train.append(row)
    file.close()

test = []

with open('testset.csv', 'r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        row.reverse()
        row = list(map(int,row))
        test.append(row)
    file.close()

error = 0
k = 3

# for j in range(11):
#     error = 0
#     for i in range(len(test)):
#         print(f"Test {i:<3}: {round(knn(train,test[i][:-1],j+1),2):<6} | Expected: {test[i][-1]:<4} | Error: {round((test[i][-1]-round(knn(train,test[i][:-1],j+1),2)),2):<4}")
#         # error += abs(round((test[i][-1]-round(knn(train,test[i][:-1],j+1),2)),2))
#     print(f"k: {j+1} | Error: {error / 18}")


def correction(deg):
    if deg < 0:
        turn(1,abs(deg))
    else:
        turn(0,deg)

print(round(knn(train,test[0][:-1],k),2))


