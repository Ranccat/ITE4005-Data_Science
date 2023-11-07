import sys
import math

# Open Files
fileInputTrainName = sys.argv[1]
fileInputTestName = sys.argv[2]
fileOutputTestName = sys.argv[3]
fileInTrain = open(fileInputTrainName, 'r')
fileInTest = open(fileInputTestName, 'r')
fileOutTest = open(fileOutputTestName, 'w')

# Global Variables
transactions = ["list"]
transactions.clear()
labels = []


class Node:
    def __init__(self, db, f_list):
        # For all nodes
        self.db = db
        self.vote = None
        self.is_leaf = False
        # Only for non-leaf node
        self.children = []
        self.feature = None
        self.condList = []
        self.featureList = f_list


def dfs(node):
    # Make vote for all nodes
    votes = {}
    for t in node.db:
        if t[classIdx] not in votes:
            votes[t[classIdx]] = 1
        else:
            votes[t[classIdx]] += 1
    node.vote = max(votes)

    # All labels are same
    if get_info(node.db) == 0:
        node.is_leaf = True
        return

    # Find feature with moth high gain ratio
    feature_vote = {}
    f_idx = -1
    for f in node.featureList:
        for idx in range(0, len(featureNames)):
            if f == featureNames[idx]:
                f_idx = idx
        feature_vote[f] = get_gain_ratio(node.db, f_idx)
    node.feature = max(feature_vote)

    # Indexing Feature
    max_idx = -1
    for idx in range(len(featureNames)):
        if node.feature == featureNames[idx]:
            max_idx = idx

    # Make Conditional Branch List
    for t in node.db:
        if t[max_idx] not in node.condList:
            node.condList.append(t[max_idx])

    # Make Seperated DB
    seperated_db = {}
    for t in node.db:
        if t[max_idx] not in seperated_db:
            seperated_db[t[max_idx]] = []
        seperated_db[t[max_idx]].append(t)

    # Make Next Feature List
    next_feature_list = []
    for f in node.featureList:
        if f == node.feature:
            continue
        next_feature_list.append(f)

    # Make Children
    for idx in range(len(node.condList)):
        child = Node(seperated_db[node.condList[idx]], next_feature_list)
        if len(child.db) == 0:
            continue
        node.children.append(Node(seperated_db[node.condList[idx]], next_feature_list))

    # DFS
    for child in node.children:
        dfs(child)

    return


def get_info(db):
    label_count = {}
    entropy = 0
    total = len(db)
    for t in db:
        if t[classIdx] not in label_count:
            label_count[t[classIdx]] = 1
        else:
            label_count[t[classIdx]] += 1

    for label in label_count:
        entropy -= (label_count[label]/total) * math.log2(label_count[label]/total)

    return entropy


def get_gain_ratio(db, f_idx):
    total_entropy = get_info(db)
    features = []
    info = 0
    split = 0
    total = len(db)
    for t in db:
        if t[f_idx] not in features:
            features.append(t[f_idx])

    for feature in features:
        count = 0
        subset = []
        for t in db:
            if t[f_idx] == feature:
                subset.append(t)
        count += 1
        entropy = get_info(subset)
        probability = count / total
        info += entropy * probability
        split -= probability * math.log2(probability)

    gain = total_entropy - info
    return gain / split


# Read Features
featureNames = fileInTrain.readline().split()
className = featureNames[len(featureNames) - 1]
className = className[0:len(className)]
classIdx = len(featureNames) - 1
featureNames = featureNames[0:len(featureNames)-1]
maxIdx = classIdx - 1

# Make DB
while True:
    transaction = list(map(str, fileInTrain.readline().split()))
    if not transaction:
        break
    transactions.append(transaction)
transLength = len(transactions)

# Read Class Names
for trans in transactions:
    transLabel = trans[classIdx]
    if transLabel not in labels:
        labels.append(transLabel)

# Make Tree
root = Node(transactions, featureNames)
dfs(root)

# Testing
testFeatures = fileInTest.readline().split()
for i in range(len(testFeatures)):
    fileOutTest.write(testFeatures[i] + "\t")
fileOutTest.write(className + "\n")

while True:
    testTrans = list(map(str, fileInTest.readline().split()))
    if not testTrans:
        break

    for i in range(len(testTrans)):
        fileOutTest.write(testTrans[i] + "\t")
    currentNode = root

    # Find the leaf node and write the label or the vote
    while not currentNode.is_leaf:
        exceptionFlag = 0
        myFeature = None
        for idx in range(len(testTrans)):
            if currentNode.feature == testFeatures[idx]:
                myFeature = testTrans[idx]
                break
        for idx in range(len(currentNode.condList)):
            if myFeature == currentNode.condList[idx]:
                currentNode = currentNode.children[idx]
                break
            if idx == len(currentNode.condList) - 1:
                exceptionFlag = 1

        if exceptionFlag == 1:
            break

    fileOutTest.write(currentNode.vote + "\n")

# Close Files
fileInTrain.close()
fileInTest.close()
fileOutTest.close()
