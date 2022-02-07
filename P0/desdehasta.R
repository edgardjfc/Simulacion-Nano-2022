library(pryr)

M = function(n) {k = 2^n; return(matrix(runif(k*k), nrow = k))}

for (n in 9:14) {
cat('Matrix', n, 'with', 2^n, 'elements takes',
system.time(M(n))[3], 'seconds to be created and weights', object_size(M(n)), 'bytes', '\n')
}
