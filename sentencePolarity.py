import numpy as np

class SentencePolarity:
    def __init__(self, file_name):
        self.positiveProbs, self.negativeProbs = self.readSentimentList(file_name)

    def readSentimentList(self, file_name):
        ifile = open(file_name, 'r')
        happy_log_probs = {}
        sad_log_probs = {}
        ifile.readline() #Ignore title row
    
        for line in ifile:
            tokens = line[:-1].split(',')
            happy_log_probs[tokens[0]] = float(tokens[1])
            sad_log_probs[tokens[0]] = float(tokens[2])

        return happy_log_probs, sad_log_probs

    def classifySentiment(self, words):
        posProbs = [self.positiveProbs[word] for word in words if word in self.positiveProbs]
        negProbs = [self.negativeProbs[word] for word in words if word in self.negativeProbs]

        posLogProbs = np.sum(posProbs)
        negLogProbs = np.sum(negProbs)

        finalPosProb = np.reciprocal(np.exp(posLogProbs - negLogProbs) + 1)
        finalNegProb = 1 - finalPosProb

        return finalPosProb, finalNegProb

    def classifyWord(self, word):
        finalPosProb = 0
        finalNegProb = 0
        negProb = 0

        if word in self.positiveProbs:
            posProb = self.positiveProbs[word]
            negProb = self.negativeProbs[word]
        
            finalPosProb = np.reciprocal(np.exp(posProb - negProb) + 1)
            finalNegProb = 1 - finalPosProb 

        return finalPosProb, finalNegProb
