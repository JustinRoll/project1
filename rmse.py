import math

def getError(classifier, testSet):
    items = []
    
    for document, label in testSet:
        items.append((label, classifier.classify(document)))
        
    return rmse(items)

def rmse(items):
    squaredDiffs = [(dist(actual, expected))**2 for actual, expected in items]
    return math.sqrt(sum(squaredDiffs) / len(items))

def dist(actual, expected):
    if type(actual) is str:
        return 1 if actual == expected else 0
    else:
        return actual-expected
