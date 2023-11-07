import sys
import math
from itertools import combinations

# Reading file
supportMinPercent = int(sys.argv[1])
fileInputName = sys.argv[2]
fileOutputName = sys.argv[3]
fileIn = open(fileInputName, 'r')
fileOut = open(fileOutputName, 'w')

database = []  # database
all_large_set = []  # starts from L1 to biggest L
all_large_set_count = []
candidates = []
candidates_count = []
large_set = []
large_set_count = []
totalItems = 0
totalTransactions = 0

# Generating database(transactions) and C1
while True:
    items = list(map(int, fileIn.readline().split()))
    if not items:
        break

    for item in items:
        itemSet = {item}
        if itemSet not in candidates:
            candidates.append(itemSet)
            candidates_count.append(1)
        else:
            candidates_count[candidates.index(itemSet)] += 1
        totalItems += 1

    database.append(frozenset(items))
    totalTransactions += 1

# Calculate minimum support
supMin = math.ceil(totalTransactions * (supportMinPercent / 100))

# Generating L1
for itemSet in candidates:
    if candidates_count[candidates.index(itemSet)] >= supMin:
        large_set.append(itemSet)
        large_set_count.append(candidates_count[candidates.index(itemSet)])

# Add L1 to prepare for later Ls
all_large_set.append(large_set)
all_large_set_count.append(large_set_count)

# Making all Cs
setSize = 2
while True:
    # Fetch and create lists
    preL = all_large_set[setSize - 2]
    preL_count = all_large_set_count[setSize - 2]
    candidates = []
    candidates_count = []

    # Making candidates
    for i in range(len(preL) - 1):
        for j in range(i + 1, len(preL)):
            newItem = (preL[i] | preL[j])

            # Checking set size
            if len(newItem) != setSize:
                continue

            # Checking minimum support
            countingSupMin = 0
            for checkingItem in database:
                if (newItem & checkingItem) == newItem:
                    countingSupMin += 1
            if countingSupMin >= supMin:
                if newItem not in candidates:
                    candidates.append(set(newItem))
                    candidates_count.append(countingSupMin)

    # Checking if no more L can be created
    if len(candidates) == 0:
        break
    setSize += 1

    # Update all sets
    all_large_set.append(candidates)
    all_large_set_count.append(candidates_count)

# Print all frequent item sets
for idx in range(2, setSize):
    # Fetch lists
    largeSet = all_large_set[idx - 1]
    largeSetCount = all_large_set_count[idx - 1]
    largeSetSize = idx

    # For each item sets
    for itemSet in largeSet:
        # Make all subsets
        subsets = set()
        for i in range(1, len(itemSet)):
            for combination in combinations(itemSet, i):
                subsets.add(frozenset(combination))

        # Get association rule for each subset
        for subset in subsets:
            # Get the associated set of a subset
            anotherSet = set()
            for eachSet in itemSet:
                if eachSet not in subset:
                    anotherSet.add(eachSet)
            frozenset(anotherSet)

            # Set index to count if transaction has subset
            supportCount = 0
            confidenceCount = 0
            totalConfidence = 0
            for transaction in database:
                if (subset | anotherSet).issubset(transaction):
                    supportCount += 1
                if subset.issubset(transaction):
                    totalConfidence += 1
                    if anotherSet.issubset(transaction):
                        confidenceCount += 1

            # Print main set
            fileOut.write("{")
            idx = 0
            for element in subset:
                fileOut.write(str(element))
                idx += 1
                if idx < len(subset):
                    fileOut.write(',')
            fileOut.write("}\t")

            # Print associated set
            fileOut.write("{")
            idx = 0
            for element in anotherSet:
                fileOut.write(str(element))
                idx += 1
                if idx < len(anotherSet):
                    fileOut.write(',')
            fileOut.write("}\t")

            # Print support and confidence
            support = round(((supportCount / totalTransactions) * 100), 2)
            fileOut.write(f'{support:.2f}\t')
            confidence = round(((confidenceCount / totalConfidence) * 100), 2)
            fileOut.write(f'{confidence:.2f}\n')

# Close files
fileIn.close()
fileOut.close()
