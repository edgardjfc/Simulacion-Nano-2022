import numpy as np
import pandas as pd
from random import random, randint, sample
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import f_oneway

def knapsack(permitedWeight, weights, values):
    assert len(weights) == len(values)
    peso_total = sum(weights)
    valor_total = sum(values)
    if peso_total < permitedWeight: 
        return valor_total
    else:
        V = dict()
        for w in range(permitedWeight + 1):
            V[(w, 0)] = 0
        for i in range(len(weights)):
            weight = weights[i]
            value = values[i]
            for w in range(permitedWeight + 1):
                cand = V.get((w - weight, i), -float('inf')) + value
                V[(w, i + 1)] = max(V[(w, i)], cand)
        return max(V.values())
 
def factible(selection, weights, capacity):
    return np.inner(selection, weights) <= capacity
  
def objective(selection, values):
    return np.inner(selection, values)
 
def normalize(data):
    smallest = min(data)
    largest = max(data)
    range  = largest - smallest
    data = data - smallest
    return data / range
  
def weightsGenerator(cuantos, low, high):
    return np.round(normalize(np.random.normal(size = cuantos)) * (high - low) + low)

def valuesGenerator(pesos, low, high):
    return np.round((pesos**2) * (high - low) + low)
 
def poblacion_inicial(n, tam):
    pobl = np.zeros((tam, n))
    for i in range(tam):
        pobl[i] = (np.round(np.random.uniform(size = n))).astype(int)
    return pobl
 
def mutacion(sol, n):
    pos = randint(0, n - 1)
    mut = np.copy(sol)
    mut[pos] = 1 if sol[pos] == 0 else 0
    return mut
  
def reproduccion(x, y, n):
    pos = randint(2, n - 2)
    xy = np.concatenate([x[:pos], y[pos:]])
    yx = np.concatenate([y[:pos], x[pos:]])
    return (xy, yx)
 
n = 100
tmax = 150
iteraciones = 20

pm, rep, init = 0.05, 50, 100
results1 = []

for runs in range(iterations):
    weights = weightsGenerator(n, 15, 80)
    values = valuesGenerator(n, 10, 500)
    capacity = int(round(sum(weights) * 0.65))
    optimal = knapsack(capacity, weights, values)
    p = initialPopulation(n, init)
    size = p.shape[0]
    assert size == init
    better = None
    betterOnes = []
    for t in range(tmax):
        for i in range(size):
            if random() < pm:
                p = np.vstack([p, mutation(p[i], n)])
        for i in range(rep): 
            parents = sample(range(size), 2)
            children = reproduction(p[parents[0]], p[parents[1]], n)
            p = np.vstack([p, children[0], children[1]])
        size = p.shape[0]
        d = []
        for i in range(size):
            d.append({'idx': i, 'obj': objective(p[i], values),
                      'fact': factible(p[i], weights, capacity)})
        d = pd.DataFrame(d).sort_values(by = ['fact', 'obj'], ascending = False)
        mantain = np.array(d.idx[:init])
        p = p[mantain, :]
        size = p.shape[0]
        assert size == init
        factibles = d.loc[d.fact == True,]
        better = max(factibles.obj)
        betterOnes.append(better)
    results1.append((optimal - better) / optimal)

    if runs == 0:
        plt.figure(figsize=(7, 3), dpi=300)
        plt.plot(range(tmax), betterOnes, 'ks--', linewidth=1, markersize=5)
        plt.axhline(y = optimal, color = 'green', linewidth=3)
        plt.xlabel('Step')
        plt.ylabel('Highest value')
        plt.ylim(0.95 * min(betterOnes), 1.05 * optimal)
        plt.savefig('p10p_I3_C1.png', bbox_inches='tight') 
        plt.close()

pm, rep, init = 0.025, 100, 200
results2 = []

for runs in range(iterations):
    weights = weightsGenerator(n, 15, 80)
    values = valuesGenerator(n, 10, 500)
    capacity = int(round(sum(weights) * 0.65))
    optimal = knapsack(capacity, weights, values)
    p = initialPopulation(n, init)
    size = p.shape[0]
    assert size == init
    better = None
    betterOnes = []
    for t in range(tmax):
        for i in range(size):
            if random() < pm:
                p = np.vstack([p, mutation(p[i], n)])
        for i in range(rep):
            parents = sample(range(size), 2)
            children = reproduction(p[parents[0]], p[parents[1]], n)
            p = np.vstack([p, children[0], children[1]])
        size = p.shape[0]
        d = []
        for i in range(size):
            d.append({'idx': i, 'obj': objective(p[i], values),
                      'fact': factible(p[i], weights, capacity)})
        d = pd.DataFrame(d).sort_values(by = ['fact', 'obj'], ascending = False)
        mantain = np.array(d.idx[:init])
        p = p[mantain, :]
        size = p.shape[0]
        assert size == init
        factibles = d.loc[d.fact == True,]
        better = max(factibles.obj)
        betterOnes.append(better)
    results2.append((optimal - better) / optimal)

    if runs == 0:
        plt.figure(figsize=(7, 3), dpi=300)
        plt.plot(range(tmax), betterOnes, 'ks--', linewidth=1, markersize=5)
        plt.axhline(y = optimal, color = 'green', linewidth=3)
        plt.xlabel('Step')
        plt.ylabel('Highest value')
        plt.ylim(0.95 * min(betterOnes), 1.05 * optimal)
        plt.savefig('p10p_I3_C2.png', bbox_inches='tight') 
        plt.close()

df  = pd.DataFrame({'Combination 1': results1, 'Combination 2': results2})
print(df)

sns.violinplot(data=df)
plt.ylabel('Proportion')
plt.savefig('p10p_I3.png', bbox_inches='tight')
plt.close

print('######### Statistical Analysis #########')
stat, p = f_oneway(results1, results2)
print('stat=%.3f, p=%.3f' % (stat, p))
if p > 0.05:
	print('Statistically non-significant')
else:
	print('Statistically significant')
