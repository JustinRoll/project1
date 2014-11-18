import math

def getError(classifier, testSet):
    items = []
    
    for document, label in testSet:
        items.append((label, classifier.classify(document)))
        
    return rmse(items)

def rmse(items):
    squaredDiffs = [(actual-expected)**2 for actual, expected in items]
    return math.sqrt(sum(squaredDiffs) / len(items))

def rmseAuth(items):
    squaredDiffs = [(actual-expected)**2 for actual, expected in items]
    return math.sqrt(sum(squaredDiffs) / len(items)) 
