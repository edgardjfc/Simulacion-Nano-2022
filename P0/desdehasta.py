from random import randint
desde = 1
hasta = 1000
menor = 5
mayor = 15
for k in range(menor, mayor + 1):
    n=2**k
    lista=[ randint(desde, hasta) for i in range(n) ]
    lista.sort()
    print(n, lista[0], lista[-1])
  
%Medir el tiempo y memoria
    

