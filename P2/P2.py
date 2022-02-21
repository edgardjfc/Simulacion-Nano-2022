import numpy as np
from random import random
import matplotlib.pyplot as plt

def makeInitialConditions(dimension, density):
    numSquares = dimension**2
    initialConditions = [1 * (random() < density) for i in range(numSquares)]
    initialGrid = np.reshape(initialConditions, (dimension,dimension))
    return initialGrid

def simulate(steps, dimension, density):
    grid = makeInitialConditions(dimension, density)

    for s in range(steps):
        grid = step(grid, dimension)
    
    return 1 * (np.sum(grid) > 0)

def step(grid, dimension):
    nextGrid = np.zeros((dimension,dimension))
    for pos in range(dimension**2):
        x = pos % dimension
        y = pos // dimension
        surroundings = grid[max(0,x-1):min(dimension,x+2),
                            max(0,y-1):min(dimension,y+2)]
        nextGrid[x,y] = 1 * (np.sum(surroundings) - grid[x,y] == 3)
    return nextGrid
        
dim = [10,15,20]
p   = [0.2,0.4,0.6,0.8]

if __name__ == "__main__":
    for d in dim:
        ys = []
        for q in p:
            results = [simulate(50, d, q) for i in range(30)]
            proportion = np.sum(results) / 30
            ys.append(proportion)
        plt.plot(p, ys, label=str(d), marker='o')
    plt.legend()
    plt.title('Game of life survival')
    plt.xlabel('Starting population density')
    plt.ylabel('Survival chance')
    plt.show()
