import math
import csv
import numpy as np

def knn(x_train, x_test, k):
    neighbors = []
    for x in x_train:
        d = euclid_dist(x,x_test)
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
    return float(1 - (np.dot(p1[:-1],p2) / (np.linalg.norm(p1[:-1]) * np.linalg.norm(p2[:-1]))))

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

print(f"Expected Value 1: {test[-4][-1]}")
print(f"Expected Value 2: {test[-5][-1]}")
print(f"Expected Value 3: {test[-6][-1]}")
print(f"Expected Value 4: {test[-7][-1]}")


for i in range(len(train)):
    print(f"{i:<3}: {round(knn(train,test[-4][:-1],i+1),2):<6}| {round(knn(train,test[-5][:-1],i+1),2):<6}| {round(knn(train,test[-6][:-1],i+1),2):<6}| {round(knn(train,test[-7][:-1],i+1),2):<6}")
    i += 1
