import nltk

def printConfusion(classifier, testSet):
    gold = []
    test = []
    for document, label in testSet:
        gold.append(label)
        test.append(classifier.classify(document))
    cm = nltk.ConfusionMatrix(gold, test)
    print(cm.pp())
