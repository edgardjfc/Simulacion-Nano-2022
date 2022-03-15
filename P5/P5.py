from math import exp, pi
import numpy as np
from GeneralRandom import GeneralRandom
import multiprocessing
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def f(x):
    return 1 / (exp(x) + exp(-x))

def g(x):
    return (2  / (pi * (exp(x) + exp(-x))))
 
vg = np.vectorize(g)
X = np.arange(-8, 8, 0.05)
Y = vg(X)
 
generator = GeneralRandom(np.asarray(X), np.asarray(Y))
start = 3
finish = 7
chunk = 50000
ammounts = [500, 5000, 50000]
wolfram = 0.04883411112604931084
ae = []
se = []
dec = []
points = []

def part(replica):
    V = generator.random(chunk)[0]
    return ((V >= start) & (V <= finish)).sum() 

def compare_strings(a, b):
    a = str(a)
    b = str(b)
    
    if a is None or b is None:
        return 0
    
    size = min(len(a), len(b))
    count = 0

    for i in range(size):
        if a[i] == b[i]:
            count += 1
        else:
            break
    return count

if __name__ == "__main__":
    with multiprocessing.Pool() as pool:
        for n in ammounts:
            p = n * chunk
            points.append('{:.1e}'.format(p))
            montecarlo = pool.map(part, range(n))
            integral = sum(montecarlo) / p
            integralValues = ((pi / 2) * integral)
            ae.append(abs(integralValues - wolfram))
            se.append(((integralValues - wolfram)**2))
            dec.append(compare_strings(wolfram, integralValues) - 2)
        
        results = {'interactions' : points,
                    'Absolute Error' : ae,
                    'Square Error' : se,
                    'Correct Decimals' : dec}

        df = pd.DataFrame(results)

        sns.barplot(data=df, x='interactions',
                    y= 'Absolute Error',
                    dodge=False)
        plt.savefig('P5_AbsoluteError.png')
        plt.show()

        sns.barplot(data=df, x='interactions',
                    y= 'Square Error',
                    dodge=False)
        plt.savefig('P5_SquareError.png')
        plt.show()

        sns.barplot(data=df, x='interactions',
                    y= 'Correct Decimals',
                    dodge=False)
        plt.savefig('P5_Decimals.png')
        plt.show()

        print(df)
