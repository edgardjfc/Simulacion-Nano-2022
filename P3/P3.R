prime <- function(n) {
    if (n < 4) {
        return(TRUE)
    }
    if (n %% 2 == 0) {
        return(FALSE)
    }
    for (i in seq(3, max(3, ceiling(sqrt(n))), 2)) {
        if (n %% i == 0) {
            return(FALSE)
        }
    }
    return(TRUE)
}

primeAlt <- function(n) {
	if (n < 4) {
		return(TRUE)
	}
	for (i in 2:(n/2)) {
		if (n %% i == 0) {
			return(FALSE)
		}
	}
	return(TRUE)
}
 
startingPoint <- 900
endPoint <-  1500
original <- startingPoint:endPoint
inverted <- endPoint:startingPoint
randomized <- sample(original)
repetitions <- 30

suppressMessages(library(doParallel))
registerDoParallel(makeCluster(detectCores()))
oa <-  numeric()
ia <-  numeric()
ra <-  numeric()
for (r in 1:repetitions) {
    oa <- c(oa, system.time(foreach(n = original,
                                    .combine=c) %dopar% prime(n))[3])
    ia <- c(ia, system.time(foreach(n = inverted,
                                    .combine=c) %dopar% prime(n))[3])
    ra <- c(ra, system.time(foreach(n = randomized,
                                    .combine=c) %dopar% prime(n))[3])
}
stopImplicitCluster()

summary(oa)
summary(ia)
summary(ra)

suppressMessages(library(doParallel))
registerDoParallel(makeCluster(detectCores() / 2))
ob <-  numeric()
ib <-  numeric()
rb <-  numeric()
for (r in 1:repetitions) {
    ob <- c(ob, system.time(foreach(n = original,
                                    .combine=c) %dopar% prime(n))[3])
    ib <- c(ib, system.time(foreach(n = inverted,
                                    .combine=c) %dopar% prime(n))[3])
    rb <- c(rb, system.time(foreach(n = randomized,
                                    .combine=c) %dopar% prime(n))[3])
}
stopImplicitCluster()

summary(ob)
summary(ib)
summary(rb)

suppressMessages(library(doParallel))
registerDoParallel(1)
oc <-  numeric()
ic <-  numeric()
rc <-  numeric()
for (r in 1:repetitions) {
    oc <- c(oc, system.time(foreach(n = original,
                                    .combine=c) %dopar% prime(n))[3])
    ic <- c(ic, system.time(foreach(n = inverted,
                                    .combine=c) %dopar% prime(n))[3])
    rc <- c(rc, system.time(foreach(n = randomized,
                                    .combine=c) %dopar% prime(n))[3])
}
stopImplicitCluster()
summary(oc)
summary(ic)
summary(rc)
