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
oaa <-  numeric()
iaa <-  numeric()
raa <-  numeric()
for (r in 1:repetitions) {
    oaa <- c(oaa, system.time(foreach(n = original,
                                    .combine=c) %dopar% prime(n))[3])
    iaa <- c(iaa, system.time(foreach(n = inverted,
                                    .combine=c) %dopar% prime(n))[3])
    raa <- c(raa, system.time(foreach(n = randomized,
                                    .combine=c) %dopar% prime(n))[3])
}
stopImplicitCluster()

summary(oaa)
summary(iaa)
summary(raa)

suppressMessages(library(doParallel))
registerDoParallel(makeCluster(detectCores() / 2))
oba <-  numeric()
iba <-  numeric()
rba <-  numeric()
for (r in 1:repetitions) {
    oba <- c(oba, system.time(foreach(n = original,
                                    .combine=c) %dopar% prime(n))[3])
    iba <- c(iba, system.time(foreach(n = inverted,
                                    .combine=c) %dopar% prime(n))[3])
    rba <- c(rba, system.time(foreach(n = randomized,
                                    .combine=c) %dopar% prime(n))[3])
}
stopImplicitCluster()

summary(oba)
summary(iba)
summary(rba)

suppressMessages(library(doParallel))
registerDoParallel(1)
oca <-  numeric()
ica <-  numeric()
rca <-  numeric()
for (r in 1:repetitions) {
    oca <- c(oca, system.time(foreach(n = original,
                                    .combine=c) %dopar% prime(n))[3])
    ica <- c(ica, system.time(foreach(n = inverted,
                                    .combine=c) %dopar% prime(n))[3])
    rca <- c(rca, system.time(foreach(n = randomized,
                                    .combine=c) %dopar% prime(n))[3])
}
stopImplicitCluster()
summary(oca)
summary(ica)
summary(rca)

suppressMessages(library(doParallel))
registerDoParallel(makeCluster(detectCores()))
oab <-  numeric()
iab <-  numeric()
rab <-  numeric()
for (r in 1:repetitions) {
    oab <- c(oab, system.time(foreach(n = original,
                                    .combine=c) %dopar% primeAlt(n))[3])
    iab <- c(iab, system.time(foreach(n = inverted,
                                    .combine=c) %dopar% primeAlt(n))[3])
    rab <- c(rab, system.time(foreach(n = randomized,
                                    .combine=c) %dopar% primeAlt(n))[3])
}
stopImplicitCluster()

summary(oab)
summary(iab)
summary(rab)

suppressMessages(library(doParallel))
registerDoParallel(makeCluster(detectCores() / 2))
obb <-  numeric()
ibb <-  numeric()
rbb <-  numeric()
for (r in 1:repetitions) {
    obb <- c(obb, system.time(foreach(n = original,
                                    .combine=c) %dopar% primeAlt(n))[3])
    ibb <- c(ibb, system.time(foreach(n = inverted,
                                    .combine=c) %dopar% primeAlt(n))[3])
    rbb <- c(rbb, system.time(foreach(n = randomized,
                                    .combine=c) %dopar% primeAlt(n))[3])
}
stopImplicitCluster()

summary(obb)
summary(ibb)
summary(rbb)

suppressMessages(library(doParallel))
registerDoParallel(1)
ocb <-  numeric()
icb <-  numeric()
rcb <-  numeric()
for (r in 1:repetitions) {
    ocb <- c(ocb, system.time(foreach(n = original,
                                    .combine=c) %dopar% primeAlt(n))[3])
    icb <- c(icb, system.time(foreach(n = inverted,
                                    .combine=c) %dopar% primeAlt(n))[3])
    rcb <- c(rcb, system.time(foreach(n = randomized,
                                    .combine=c) %dopar% primeAlt(n))[3])
}
stopImplicitCluster()
summary(ocb)
summary(icb)
summary(rcb)

boxplot(oaa, iaa, raa, oba, iba, rba, oca, ica, rca, oab, iab, rab, obb, ibb, rbb, ocb, icb, rcb)
