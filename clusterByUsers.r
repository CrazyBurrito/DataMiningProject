dataFile = 'data/userSub.csv'
numClus = 60
plotType = "cladogram"

# load data
mydata <- read.table(dataFile, header=TRUE, sep=',', row.names=NULL)

# for phylogenetic tree
require(ape)

# distance matrix
d <- dist(t(mydata), method = "euclidean")

# cluster subreddits
fit <- hclust(d, method="ward")

# plot graph
png("1.png", width=3000, height=8000, unit='px', res=300)
mypal = rep(c("#556270", "#4ECDC4", '#D43700', '#0139bA'), numClus/4)
clus5 = cutree(fit, numClus)
plot(as.phylo(fit), tip.color=mypal[clus5], label.offset=2, no.margin=TRUE, cex=0.4)
#plot(fit)
#rect.hclust(fit, k=numClus, border="red")
