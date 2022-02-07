def f(x):
    return 2**x

from multiprocessing import Pool
if __name__ == '__main__':
    with Pool(2) as p:
        print(p.map(f, [1, 2, 5]))
