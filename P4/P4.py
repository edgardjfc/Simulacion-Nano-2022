import seaborn as sns
from math import sqrt
from PIL import Image, ImageColor
from random import randint, choice
import matplotlib.pyplot as plt
 
# constant stuff
neighbours = []
for dx in range(-1, 2):
    for dy in range(-1, 2):
        if dx != 0 or dy != 0:
            neighbours.append((dx, dy))
 
n = 80 # size of image
k = [25,50,75,100] # seed densities to use
 
 
# function stuff
def cell(pos, seeds):
    if pos in seeds:
        return seeds.index(pos)
    x, y = pos % n, pos // n
    nearby = None
    minimum = n * sqrt(2)
    for i in range(len(seeds)):
        (xs,ys) = seeds[i]
        dx, dy = x - xs, y - ys
        dist = sqrt(dx**2 + dy**2)
        if dist < minimum:
            nearby, minimum = i, dist
    return nearby
 
def initialise():
    direction = randint(0, 3)
    if direction == 0: # down -> up
        return (0, randint(0, n - 1))
    elif direction == 1: # left -> right
        return (randint(0, n - 1), 0)
    elif direction == 2: # right -> left
        return (randint(0, n - 1), n - 1)
    else: # up -> down
        return (n - 1, randint(0, n - 1))
 
def propagate(vor):
    # initial parameters
    prob, difficulty = 0.9, 0.8
    (x, y) = initialise()
 
    # results
    crackPoints = []
 
    while True:
        # crack this point
        crackPoints.append((x,y))
 
        # determine which neighbours belong to the same cell (interior), and which belong to a different cell (boundary)
        boundary, interior = [], []
        for v in neighbours:
            (dx, dy) = v
            vx, vy = x + dx, y + dy
            if vx >= 0 and vx < n and vy >= 0 and vy < n: # inside the image
               if not (vx,vy) in crackPoints: # no crack
                   if vor[vx, vy] == vor[x, y]: # same cell
                       interior.append(v)
                   else:
                       boundary.append(v)
        
        # select a point to spread to
        selected = None
        if len(boundary) > 0:
            selected = choice(boundary)
            prob = 1
        elif len(interior) > 0:
            selected = choice(interior)
            prob *= difficulty
        
        # if a point is selected, then spread
        if selected is not None:
            (dx, dy) = selected
            x, y = x + dx, y + dy
        else:
            break # stops spreading
    
    return crackPoints
 
def simulate(seedDensity):
    # generate a list of random seeds
    seeds = []
    for s in range(seedDensity):
        while True:
            x, y = randint(0, n - 1), randint(0, n - 1)
            if (x, y) not in seeds:
                seeds.append((x, y))
                break
    
    # generate the initial image
    cells = [cell(i, seeds) for i in range(n * n)]
    voronoi = Image.new('RGB', (n, n))
    vor = voronoi.load()
    c = sns.color_palette("Set3", seedDensity).as_hex()
    for i in range(n * n):
        vor[i % n, i // n] = ImageColor.getrgb(c[cells.pop(0)])
    
    # propagate two cracks across the voronoi diagram
    crack1 = propagate(vor)
    crack2 = propagate(vor)
 
    # draw the cracks on the image
    #white = (255,255,255)
    #black = (0,0,0)
    #for (cx,cy) in crack1:
    #    vor[cx,cy] = white
    #for (cx,cy) in crack2:
    #    vor[cx,cy] = black
    
    # save the image
    #visual = voronoi.resize((10 * n,10 * n))
    #visual.save("vor.png")
 
    # determine if there is overlap
    return any([x==y for x in crack1 for y in crack2])
 
if __name__ == "__main__":
    ys = []
    # run simulations
    for sd in k:
        print("seed = %d..." % sd)
        results = [1 if simulate(sd) else 0 for i in range(200)]
        proportion = sum(results) / len(results)
        ys.append(proportion)
 
    # draw graph of results
    plt.bar(k, ys)
    plt.xlabel('Seed Density')
    plt.ylabel('Probability')
    plt.show()
