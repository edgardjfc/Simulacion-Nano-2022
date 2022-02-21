import numpy as np
from random import random
import matplotlib.pyplot as plt
import matplotlib.cm as cm

def makeInitialConditions(dimension, density):
    numSquares = dimension**2
    initialConditions = [1 * (random() < density) for i in range(numSquares)]
    initialGrid = np.reshape(initialConditions, (dimension,dimension))
    return initialGrid

def simulate(steps, dimension, density):
    grid = makeInitialConditions(dimension, density)

    for s in range(steps):
        grid = step(grid, dimension)
    
    return grid

isAliveFunc = np.vectorize(lambda x: 1 * (x>0))

def step(grid, dimension):
    nextGrid = np.zeros((dimension,dimension))
    for pos in range(dimension**2):
        x = pos % dimension
        y = pos // dimension
        surroundings = grid[max(0,x-1):min(dimension,x+2),
                            max(0,y-1):min(dimension,y+2)]
        if surroundings.all():
            nextGrid[x,y] = grid[x,y]
        else:              
            alivesurroundings = np.sum(isAliveFunc(surroundings))
            nextGrid[x,y] = grid[x,y] + 1*(alivesurroundings >= 3 and alivesurroundings < 8)
    return nextGrid
        
if __name__ == "__main__":
    var = makeInitialConditions(50,0.15)
    fig = plt.figure()
    plt.imshow(var, interpolation='nearest', cmap=cm.Greys)
    fig.suptitle('Initial Condition')
    plt.savefig('p2_t0_p.png')
    plt.close()
    for i in range(50):
        var = step(var, 50)
        if i%2==0:
            fig=plt.figure()
            plt.imshow(var, interpolation='nearest', cmap=cm.Greys)
            fig.suptitle('State at iteration %d' % i)
            plt.savefig('p2_t%d_p.png' % i)
            plt.close()
            
        

