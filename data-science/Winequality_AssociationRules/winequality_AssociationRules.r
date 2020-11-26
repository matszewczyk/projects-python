library(arules) # association rules
library(arulesViz) # visualization of rules

# Quality of white wine analysis (on the 0-10 scale)
# quality variable levels present in dataset: 3 4 5 6 7 8 9
# where 3 is the worst quality wine and 9 is the best quality wine.

data = read.csv("winequality-white.csv", header=TRUE, sep=";")
View(data)

# Missing values check - there are no missing values
length(which(is.na(data)==TRUE))

# Cheking the number of unique values + summary for every feature
for (colname in colnames(data)){
  unique_values = length(unique(data[[colname]]))
  cat(sprintf("column: %s | unique values: %i\n", colname,unique_values))
  print(summary(data[[colname]]))
  cat(sprintf('____________\n'))
}

### DISCRETIZATION ###
# Taking all the columns except quality, as it's already a categorical feature
cols_without_quality = colnames(data)[-length(colnames(data))]
cols_without_quality

# Decicded to do the split by frequency 
# (n number of ranges, where every range has similar quantity of obs)
# Reason: it gives a good understanding of what is the low/high level of particular feature;
#         outliers don't have such a big influence on ranges
for (colname in cols_without_quality){
  data[[colname]] = discretize(data[[colname]], method="frequency", breaks=4)
}
data[['quality']] = as.factor(data[['quality']])

View(data)
summary(data)

# Convert the dataset to transactional one
dataTR = as(data, "transactions")
View(dataTR)

### DATA ANALYSIS ###
# Check the relative support of all single items
freqTable = itemFrequency(dataTR, type='relative')
summary(freqTable)

plot(freqTable)
itemFrequencyPlot(dataTR, type ="relative", support= 0.2)
# On the plots we can see that almost all the features have support around 25%.
# The only exception is the quality of wine variable.
# The reason behind it is the fact, that we've used frequency as the discretization method.
# In our opinion it shouldn't cause any problems, as we are aiming for the analysis of itemsets
# consisting more than one item, as we would like to see, what determines the high quality of wine.

print(freqTable[freqTable > 0.4])
# 45% of the wine has quality marked as 6 - this is the biggest support for a single item.

### FREQUENT ITEMSETS ###

# So at first, we will use apriori method in order to mine frequent items, (support = 0.2). 
apr <- apriori(dataTR, parameter = list(target = "frequent itemsets", support = 0.2,  maxlen = 10))
apr
# And once again with support set to 0.1,
apr <- apriori(dataTR, parameter = list(target = "frequent itemsets", support = 0.1,  maxlen = 10))
apr
# For this one we will go futher with support set to 0.1, as set of 129 will be more suitable for our expriment. 

summary(apr)

# Searching for the frequent itemsets with higher quality of wine, in order to determine the factors of wine quality.
highQuality_freqItemsets = subset(apr, subset = items %in% c("quality=7","quality=8", "quality=9"))
inspect(highQuality_freqItemsets)
# Unfortunetaly, there are no frequent itemsets for good quality wine, which contain more than 1 item.

# Searching for the frequent itemsets with lower quality of wine, in order to determine the factors of wine quality.
lowQuality_freqItemsets = subset(apr, subset = items %in% c("quality=3","quality=4", "quality=5"))
inspect(lowQuality_freqItemsets)
# The support of the frequent itemsets, which contain quality of wine in range from 3 to 5 & have more then 1 item.
# fluctuates around 10% - there are no obvious raltionships, that may indicate the low quality of wine.
# However we've noticed, that there is a following frequent itemset: {alcohol=[8,9.5),quality=5} with support 0.1267864.
plot(data$alcohol~data$quality)
# There is a relationship between wine quality and the amount of alcohol it contains.
# The plot reveals that high quality wines tend to be stronger, then the low quality ones. 

### RULE INDUCTION ###

#Basing on previoulsy mined set of items we will try to make rule induction.
Rapr <- ruleInduction(apr, dataTR, confidence = 0.8, control = list(verbose = TRUE, method = "apriori"))
Rapr

inspect(Rapr, by = "lift")
# As we can see in rules induction inspection, we have managed to find 9 association rules. 
# All of them have lift > 1 and confidence greater than >80%, if we have changed previously set support to 0.2
# only two of those rules would qualify. When we look closer at our results we will see that we mostly have managed to
# find some dependency between sugar and density, which seems logical. 

# Here we are retaking the rule induction, but with eclat method for mining frequent itemsets.   
ec  <- eclat(dataTR, parameter = list(support = 0.1, maxlen = 50))
ec

summary(ec)


Rec <- ruleInduction(ec, dataTR, confidence = 0.8)
Rec

inspect(Rec, by = "lift")
# The outcome is almost identical, which we assume is good in terms od corectness of previous results.

# To sum up, the quality of wine seems to be the result of many factors working simultaneously, so that finding exact features
# determining the wine quality is not that easy to discover and there are probably better methods for the task, 
# then frequent itemsets analysis & association rules induction. 
