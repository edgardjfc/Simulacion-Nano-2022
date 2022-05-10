expresions <- function(maxdeg, varcount, termcount) {
  f <- data.frame(variable=integer(), coef=integer(), degree=integer())
  for (t in 1:termcount) {
    var <- sample(1:varcount, 1)
    deg <- sample(0:maxdeg, 1)
    f <-  rbind(f, c(var, runif(1), deg))
  }
  names(f) <- c("variable", "coef", "degree")
  return(f)
}

evaluation <- function(pol, vars) {
  value <- 0.0
  terms = dim(pol)[1]
  for (t in 1:terms) {
    term <- pol[t,]
    value <-  value + term$coef * vars[term$variable]^term$degree
  }
  return(value)
}

domin.by <- function(target, challenger) {
  if (sum(challenger < target) > 0) {
    return(FALSE) 
  } 
  return(sum(challenger > target) > 0)
}

vc <- 3
md <- 2
tc <- 4
k <- 2 
obj <- list()
for (i in 1:k) {
  obj[[i]] <- expresions(md, vc, tc)
}
minim <- (runif(k) > 0.5)
sign <- (1 + -2 * minim) 
n <- 200 
sol <- matrix(runif(vc * n), nrow=n, ncol=vc)
val <- matrix(rep(NA, k * n), nrow=n, ncol=k)
for (i in 1:n) { 
  for (j in 1:k) { 
    val[i, j] <- evaluation(obj[[j]], sol[i,])
  }
}
mejor1 <- which.max(sign[1] * val[,1])
mejor2 <- which.max(sign[2] * val[,2])
cual <- c("max", "min")
xl <- paste("First objective (", cual[minim[1] + 1], ")", sep="")
yl <- paste("Second objective (", cual[minim[2] + 1], ")", sep="")
png("p11_R1_init.png", width=15, height=15, units="cm", res=1200)
plot(val[,1], val[,2], xlab=xl, ylab=yl)
graphics.off()
png("p11_R1_mejores.png", width=15, height=15, units="cm", res=1200)
plot(val[,1], val[,2], xlab=paste(xl, "Better marked as blue square"),
     ylab=paste(yl,"Better marked as orange circle"))
points(val[mejor1, 1], val[mejor1, 2], col="blue", pch=15, cex=1.5)
points(val[mejor2, 1], val[mejor2, 2], col="orange", pch=16, cex=1.5)
graphics.off()
no.dom <- logical() 
dominadores <- integer()
for (i in 1:n) { 
  d <- logical() 
  for (j in 1:n) { 
    d <- c(d, domin.by(sign * val[i,], sign * val[j,]))
  }
  cuantos <- sum(d)
  dominadores <- c(dominadores, cuantos)
  no.dom <- c(no.dom, sum(d) == 0) 
}

frente <- subset(val, no.dom) 
png("p11_R1_frente.png", width=15, height=15, units="cm", res=1200)
plot(val[,1], val[,2], xlab=paste(xl, "Better marked as blue square"),
     ylab=paste(yl,"Better marked as orange circle"))
points(frente[,1], frente[,2], col="green", pch=16, cex=0.9)
mejor1 <- which.max((1 + (-2 * minim[1])) * val[,1])
mejor2 <- which.max((1 + (-2 * minim[2])) * val[,2])
points(val[mejor1, 1], val[mejor1, 2], col="blue", pch=15, cex=0.5)
points(val[mejor2, 1], val[mejor2, 2], col="orange", pch=16, cex=0.5)
graphics.off()

library(ggplot2)
data <- data.frame(pos=rep(0, n), dom=dominadores)
png("p11_R1_violin.png", width=15, height=15, units="cm", res=1200)
gr <- ggplot(data, aes(x=pos, y=dom)) + geom_violin(fill="orange", color="red")
gr + geom_boxplot(width=0.2, fill="blue", color="green", lwd=2) +
  xlab("") +
  ylab("Frequency") +
  ggtitle("Amount of Dominant Solutions")
graphics.off()

porcentaje=50
dispersos = kmeans(frente, round(dim(frente)[1]*porcentaje/100), iter.max = 1000, nstart = 50, algorithm = "Lloyd")
dispersos$cluster
dispersos$centers

png("p11_R1_fdispersos.png", width=15, height=15, units="cm", res=1200)
plot(val[,1], val[,2], xlab=paste(xl, "Better marked as blue square"),
     ylab=paste(yl,"Better marked as orange circle"))
points(frente[,1], frente[,2], col="green", pch=16, cex=0.9)
points(dispersos$centers[,1], dispersos$centers[,2], col="red", pch=16, cex=0.9)
mejor1 <- which.max((1 + (-2 * minim[1])) * val[,1])
mejor2 <- which.max((1 + (-2 * minim[2])) * val[,2])
points(val[mejor1, 1], val[mejor1, 2], col="blue", pch=15, cex=0.5)
points(val[mejor2, 1], val[mejor2, 2], col="orange", pch=16, cex=0.5)
