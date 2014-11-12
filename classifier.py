import random,operator,nltk
import functools
from nltk.corpus import udhr
from nltk import bigrams, trigrams
from nltk.tokenize import word_tokenize, sent_tokenize 
from nltk.corpus import stopwords, wordnet
from nltk.stem.snowball import SnowballStemmer
from yelpQuery import YelpQuery

class Classifier:

    def __init__(self, reviews):
        self.reviews = reviews
        self.yelpQuery = YelpQuery()
        self.yelpQuery.connect()
    
    def getBucket(self, count):
        if count <= 0:
            returnCount = "none"
        if count >= 1 and count <= 2:
            returnCount = "low"
        elif count >= 3 and count <= 5:
            returnCount = "medium"
        elif count > 6 and count <= 10:
            returnCount = "high"
        elif count > 10 and count <= 20:
            returnCount = "veryHigh"
        else: 
            returnCount = "over20"

        return returnCount
    
    def getOverallFeatures(self, doc):

        featureDict = {}
        wordDict, topicWordDict, sents, stemmedWordDict = self.extractReviewWords(doc)
        wordList = sorted([word.lower() for word in set(stemmedWordDict.keys()) if word not in stopwords.words('English') and word not in ',-.;();$' and word not in '-' and word not in '.'],
                key = lambda x : stemmedWordDict[x], reverse=True)
        top10WordList = [wordList[i] for i in range(0, 10 if len(wordList) > 10 else len(wordList) - 1)]


        #for sent in sents:
        #        wordBigrams = bigrams(word_tokenize(sent))
        #        for bigram in wordBigrams:
        #                featureDict[bigram] = True
        #        tokenizedSent = [word for word in word_tokenize(sent) if ',' not in word and '.' not in word]
        #        wordTrigrams = trigrams(tokenizedSent)
        #        for trigram in wordTrigrams:
        #                featureDict[trigram] = True
        #for unigram in top10WordList:
        #    featureDict[unigram] = self.getBucket(stemmedWordDict[unigram])
        weight = 1
        yelpFeatures = self.yelpQuery.getFeatures(doc.name, doc.city, weight)
        featureDict.update(yelpFeatures)
        
        return featureDict 

    #return a dictionary with words and a count of all the words in the review
    def extractReviewWords(self, doc):
        wordDict = {}
        topicWordDict = {}
        stemmedWordDict = {}
        stemmer = SnowballStemmer('english')
        sents = []        

        for paragraph in doc.paragraphs:
                #tokenize all words
                #to do: pos tag all words?        
                wordTokens = word_tokenize(paragraph)
                for word in wordTokens:
                        self.incrementDictCount(word, wordDict)
                        self.incrementDictCount(stemmer.stem(word), stemmedWordDict)
                        #self.incrementDictCount(key, topicWordDict)
                for sent in sent_tokenize(paragraph):
                        sents.append(sent)
        return wordDict, topicWordDict, sents, stemmedWordDict  

    def incrementDictCount(self, item, incDict):
        if item in incDict:
                incDict[item] += 1
        else:
                incDict[item] = 1        

    def classifyOverallReviews(self):

        docs = [(review, 'Pos') for review in self.reviews if review.rating >= 3] + [(review, 'Neg') for review in self.reviews if review.rating < 3]
        random.shuffle(docs)

        featureSets = [(self.getOverallFeatures(d),label) for (d, label) in docs]
        firstThird = int(len(featureSets)/3)
        train, test = featureSets[:firstThird], featureSets[firstThird:]

        classifier = nltk.NaiveBayesClassifier.train(train)
        print(classifier.show_most_informative_features(20))
 
        return nltk.classify.accuracy(classifier,test) 

    def classifyParagraphs(self):
        pass
 

    def getAverages(self):
        runningTotal = 0.0
        for i in range(1, 5):
            runningTotal += self.classifyOverallReviews()

        print("Overall Positive/Negative prediction accuracy: %f", runningTotal / 5)


    def compareSynsets(self, word):
        posSynsets = wordnet.synsets("positive")
        negSynsets = wordnet.synsets("negative")
        wordSynsets = wordnet.synsets(word)
        
        print(wordSynsets[0].path_similarity(posSynsets[0]))
        print(wordSynsets[0].path_similarity(negSynsets[0]))
               
