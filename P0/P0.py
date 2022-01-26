import random

x = 21
y = 3
z = 7

var = [ x, y, z ]

print(( x + 2)*( y**3 )*( 2 * z ))

print(sum(var))

myRandom = random.randint(0,30)

print(myRandom)

if myRandom < y:
    print("smol")
elif myRandom > x:
    print("lorge")
else:
    print("avererage")
