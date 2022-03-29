from random import uniform
import matplotlib.pyplot as plt
import numpy as np
from math import cos, sin, floor, log
import pandas as pd

def g(x, y):
    px = (cos(x))**3 + 0.1 * x
    py = (sin(y))**3 + 0.1 * y
    return px + py

low = -10
high = -low
step = 0.05
p = np.arange(low, high, step)
n = len(p)
z = np.zeros((n, n), dtype=float)
valores=[]
paso = 0.5

digitos = floor(log(100, 10)) + 1
guardar = 0
for i in range(n):
    x = p[i]
    for j in range(n): 
        y = p[n - j - 1] # voltear
        z[i, j] = g(x, y)
        valores.append(g(x, y))

tmax=10
for a in range(10, 31, 10):

    resultados = pd.DataFrame()
    for tiem in range(2, 5):
        agentes =  pd.DataFrame()
        agentes['x'] = [uniform(low, high) for i in range(a)]
        agentes['y'] = [uniform(low, high) for i in range(a)]
        agentes['best'] = [min(valores) for i in range(a)]
        bestx = agentes['x'][0]
        besty = agentes['y'][0]
        best = g(bestx, besty)
        for tiempo in range(tmax**tiem):
            agentes['dx'] = [uniform(0, paso) for i in range(a)]
            agentes['dy'] = [uniform(0, paso) for i in range(a)]
            for i in range(a):
                r = agentes.iloc[i]
                
                xl = r.x - r.dx
                xr = r.x + r.dx
                yd = r.y - r.dy
                yu = r.y + r.dy
                
                if  xl < low+step:
                    xl = r.x
                if  xr > high-step:
                    xr = r.x
                if  yd < low+step:
                    yd = r.y
                if  yu > high-step:
                    yu = r.y
                
                g1 = g(xl, yu)
                g2 = g(r.x, yu)
                g3 = g(xr, yu)
                g4 = g(xl, r.y)
                g5 = g(xr, r.y)
                g6 = g(xl, yd)
                g7 = g(r.x, yd)
                g8 = g(xr, yd)
                lista = [g1,g2,g3,g4,g5,g6,g7,g8]
                mayor = lista.index(max(lista))+1   
                       
                if mayor == 1:
                    agentes.at[i, 'x'] = xl
                    agentes.at[i, 'y'] = yu
                elif mayor ==2:
                    agentes.at[i, 'x'] = r.x
                    agentes.at[i, 'y'] = yu
                elif mayor ==3:
                    agentes.at[i, 'x'] = xr
                    agentes.at[i, 'y'] = yu
                elif mayor ==4:
                    agentes.at[i, 'x'] = xl
                    agentes.at[i, 'y'] = r.y
                elif mayor ==5:
                    agentes.at[i, 'x'] = xr
                    agentes.at[i, 'y'] = r.y
                elif mayor ==6:
                    agentes.at[i, 'x'] = xl
                    agentes.at[i, 'y'] = yd
                elif mayor ==7:
                    agentes.at[i, 'x'] = r.x
                    agentes.at[i, 'y'] = yd
                elif mayor ==8:
                    agentes.at[i, 'x'] = xr
                    agentes.at[i, 'y'] = yd
                
                mejor = g(r.x, r.y)
                if mejor > best:
                    best = g(r.x, r.y)
                    bestx = r.x
                    besty = r.y
                
                if mejor > r.best:
                    agentes.at[i, 'best'] = mejor
                    
        
            xb = ((n-1)/2)+(bestx/step)
            yb= ((n-1)/2)-(besty/step)
            
            if guardar == 0:
                t = range(0, n, 40)
                l = ['{:.1f}'.format(low + i * step) for i in t]
                fig, ax = plt.subplots(figsize=(6, 5), ncols=1)
                pos = ax.imshow(z) 
                for k in range(a):
                    r = agentes.iloc[k]
                    x= ((n-1)/2)+(r.x/step)
                    y= ((n-1)/2)-(r.y/step)     
                    ax.plot(y, x, 'ro')
                ax.plot(yb,xb, 'go')
                plt.xticks(t, l)
                plt.yticks(t, l[::-1]) # arriba-abajo
                fig.colorbar(pos, ax=ax)
                plt.savefig('p7_v_t' + \
                            format(tiempo, '0{:d}'.format(digitos)) + '.png')
        guardar = 1
        resultados[(str(a)+' con ' +str(tmax**tiem))] = agentes['best']
        print(tmax**tiem)
        
    resultados.to_csv('resultados_{:d}.csv'.format(a))
