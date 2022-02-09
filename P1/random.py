from random import random
from math import fabs, sqrt

random()

pos = [0, 0]
dur = 100
largest = 0
returns = 0

print('Walk of', dur, 'steps')

for step in range(dur):
    axis = 0 if random() < 0.5 else 1
    if random()<0.5:
        pos[axis] +=1
    else:
        pos[axis] -=1
    if all([ p==0 for p in pos]):
        returns +=1
    euclidian = sqrt(sum([ p**2 for p in pos ]))
    largest = max(largest, euclidian)
    
print('There were', returns, 'returns')
print('the largest distance was', largest)
