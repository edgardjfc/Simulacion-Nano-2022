from random import random, randint, getrandbits
from math import fabs, sqrt
import matplotlib.pyplot as plt
import numpy as np
from time import time

runs = 30
steps = [100, 1000, 10000]
results = []

for i in range(3):
    dur = steps[i]
    for dim in range(1, 6): 
        mayores = []
        for rep in range(runs):
            before = time()*1000
            pos = [0] * dim
            mayor = 0
            for paso in range(dur):
                eje = randint(0, dim - 1)
                if pos[eje] > -100 and pos[eje] < 100:
                    if random() < 0.5:
                        pos[eje] += 1
                    else:
                        pos[eje] -= 1
                else:
                    if pos[eje] == -100:
                        pos[eje] += 1
                    if pos[eje] == 100:
                        pos[eje] -= 1
                mayor = max(mayor, sqrt(sum([p**2 for p in pos])))
            mayores.append(mayor)
            after = time()*1000
        results.append(mayores)
tiempo = after - before
print(tiempo)

walks_1 = results[0:5]
walks_2 = results[5:10]
walks_3 = results[10:15]

ticks = ['1', '2', '3', '4', '5']

def set_box_color(bp, color):
    plt.setp(bp['boxes'], color=color)
    plt.setp(bp['whiskers'], color=color)
    plt.setp(bp['caps'], color=color)
    plt.setp(bp['medians'], color='orange')

plt.figure()

bpl = plt.boxplot(walks_1, positions=np.array(range(len(walks_1)))*5.0-1.0, sym='', widths=0.8)
bpc = plt.boxplot(walks_2, positions=np.array(range(len(walks_2)))*5.0, sym='', widths=0.8)
bpr = plt.boxplot(walks_3, positions=np.array(range(len(walks_3)))*5.0+1.0, sym='', widths=0.8)
set_box_color(bpl, '#D7191C')
set_box_color(bpc, '#2CB62C')
set_box_color(bpr, '#2C7BB6')

plt.plot([], c='#D7191C', label='100 steps')
plt.plot([], c='#2CB62C', label='1000 steps')
plt.plot([], c='#2C7BB6', label='10000 steps')
plt.legend()

plt.xticks(range(0, len(ticks)*5, 5), ticks)
plt.xlim(-2, len(ticks)*5)
plt.title('Euclidean distance')
plt.xlabel('Dimensions')
plt.ylabel('Max distance')
plt.tight_layout()
plt.savefig('EuclideanDistance.png')
plt.show()
