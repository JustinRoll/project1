import random,operator,nltk
import functools
from nltk.corpus import udhr
from nltk import bigrams, trigrams, ngrams
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
            returnCount = None
        elif count >= 1 and count <= 5:
            returnCount = "low"
        elif count >= 6:
            returnCount = "high"

        return returnCount
    
    def getOverallFeatures(self, doc):

        featureDict = {}
        wordDict, topicWordDict, sents, stemmedWordDict = self.extractReviewWords(doc)
        wordList = sorted([word.lower() for word in set(stemmedWordDict.keys()) if word not in stopwords.words('English') and word not in ',-.;();$' and word not in '-' and word not in '.'],
                key = lambda x : stemmedWordDict[x], reverse=True)
        top10WordList = [wordList[i] for i in range(0, 10 if len(wordList) > 10 else len(wordList) - 1)]


        for sent in sents:
                tokenizedSent = [word for word in word_tokenize(sent) if ',' not in word and '.' not in word]
                wordTrigrams = trigrams(tokenizedSent)
                for trigram in wordTrigrams:
                        featureDict[trigram] = True
        for unigram in top10WordList:
            featureDict[unigram] = self.getBucket(stemmedWordDict[unigram])
        weight = 1
        yelpFeatures = self.yelpQuery.getFeatures(doc.name, doc.city, weight)
        featureDict.update(yelpFeatures)
        return featureDict

    def getAuthorshipFeatures(self, doc):

        featureDict = {}
        wordDict, topicWordDict, sents, stemmedWordDict = self.extractReviewWords(doc)
        wordList = sorted([word.lower() for word in set(stemmedWordDict.keys()) if word not in stopwords.words('English') and word not in ',-.;();$' and word not in '-' and word not in '.'],
                key = lambda x : stemmedWordDict[x], reverse=True)
        top10WordList = [wordList[i] for i in range(0, 10 if len(wordList) > 10 else len(wordList) - 1)]

        for sent in sents:
                tokenizedSent = [word for word in word_tokenize(sent) if ',' not in word and '.' not in word]
                wordTrigrams = trigrams(tokenizedSent)
                for trigram in wordTrigrams:
                        featureDict[trigram] = True
        for unigram in top10WordList:
            featureDict[unigram] = self.getBucket(stemmedWordDict[unigram])

        return featureDict 

    def getParagraphFeaturesExact(self, doc):

        featureDict = {}
        wordDict, topicWordDict, sents, stemmedWordDict = self.extractReviewWordsFromParagraph(doc)
        wordList = sorted([word.lower() for word in set(stemmedWordDict.keys()) if word.lower() not in stopwords.words('English') and word not in ',-.;();$' and word not in '-' and word not in '.'],
                key = lambda x : stemmedWordDict[x], reverse=True)
        topWordList = [wordList[i] for i in range(0, 10 if len(wordList) > 10 else len(wordList) - 1)]

        for sent in sents:
                tokenizedSent = [word for word in word_tokenize(sent) if ',' not in word and '.' not in word]
                wordTrigrams = trigrams(tokenizedSent)
                for trigram in wordTrigrams:
                        featureDict[trigram] = True
                #wordBigrams = bigrams(tokenizedSent)
                #for bigram in wordBigrams:
                #        featureDict[bigram] = True
                #fourGrams = ngrams(tokenizedSent, 4)
                #for fourGram in fourGrams:
                #        featureDict[fourGram] = True
        for unigram in topWordList:
            featureDict[unigram] = self.getBucket(stemmedWordDict[unigram])
        
        return featureDict   


    def getParagraphFeatures(self, doc):

        featureDict = {}
        wordDict, topicWordDict, sents, stemmedWordDict = self.extractReviewWordsFromParagraph(doc)
        wordList = sorted([word.lower() for word in set(stemmedWordDict.keys()) if word.lower() not in stopwords.words('English') and word not in ',-.;();$' and word not in '-' and word not in '.'],
                key = lambda x : stemmedWordDict[x], reverse=True)
        topWordList = [wordList[i] for i in range(0, 10 if len(wordList) > 10 else len(wordList) - 1)]

        for sent in sents:
                tokenizedSent = [word for word in word_tokenize(sent) if ',' not in word and '.' not in word]
                wordTrigrams = trigrams(tokenizedSent)
                for trigram in wordTrigrams:
                        featureDict[trigram] = True
                #wordBigrams = bigrams(tokenizedSent)
                #for bigram in wordBigrams:
                #        featureDict[bigram] = True
                #fourGrams = ngrams(tokenizedSent, 4)
                #for fourGram in fourGrams:
                #        featureDict[fourGram] = True
        for unigram in topWordList:
            featureDict[unigram] = self.getBucket(stemmedWordDict[unigram])
        
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

    def extractReviewWordsFromParagraph(self, paragraph):
        wordDict = {}
        topicWordDict = {}
        stemmedWordDict = {}
        stemmer = SnowballStemmer('english')
        sents = []        

        
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

        docs = [(review, 'Pos') for review in self.reviews if review.rating > 3] + [(review, 'Neg') for review in self.reviews if review.rating <= 3]
        random.shuffle(docs)

        featureSets = [(self.getOverallFeatures(d),label) for (d, label) in docs]
        firstThird = int(len(featureSets)/3)
        train, test = featureSets[:firstThird], featureSets[firstThird:]

        classifier = nltk.NaiveBayesClassifier.train(train)
        print(classifier.show_most_informative_features(20))
 
        return nltk.classify.accuracy(classifier,test) 

    def classifyOverallReviewsExact(self):

        docs = [(review, review.rating) for review in self.reviews]
        random.shuffle(docs)

        featureSets = [(self.getOverallFeatures(d),label) for (d, label) in docs]
        firstThird = int(len(featureSets)/3)
        train, test = featureSets[:firstThird], featureSets[firstThird:]

        classifier = nltk.NaiveBayesClassifier.train(train)
        print(classifier.show_most_informative_features(20))
 
        return nltk.classify.accuracy(classifier,test)  

    def classifyParagraphReviewsExact(self):
        
        docs = []
        for review in self.reviews:
            for score, paragraph in review.ratingParagraphMap.items():
                docs.append((paragraph, score))

        random.shuffle(docs)

        featureSets = [(self.getParagraphFeaturesExact(d),label) for (d, label) in docs]
        firstThird = int(len(featureSets)/3)
        train, test = featureSets[:firstThird], featureSets[firstThird:]

        classifier = nltk.NaiveBayesClassifier.train(train)
        print(classifier.show_most_informative_features(20))
 
        return nltk.classify.accuracy(classifier,test)  

    def classifyAuthorshipReviews(self):
        
        docs = []
        for review in self.reviews:
            docs.append((review, review.reviewer))

        authors = set([review.reviewer for review in self.reviews])
        print("%d Authors total, baseline is %f" %(len(authors), 1.0/len(authors)))
        random.shuffle(docs)

        featureSets = [(self.getAuthorshipFeatures(d),label) for (d, label) in docs]
        firstThird = int(len(featureSets)/3)
        train, test = featureSets[:firstThird], featureSets[firstThird:]

        classifier = nltk.NaiveBayesClassifier.train(train)
        print(classifier.show_most_informative_features(20))
 
        return nltk.classify.accuracy(classifier,test)   

    def classifyParagraphReviews(self):
        
        docs = []
        for review in self.reviews:
            for score, paragraph in review.ratingParagraphMap.items():
                if score > 3:
                    docs.append((paragraph, 'Pos'))
                else:
                    docs.append((paragraph, 'Neg'))
        random.shuffle(docs)

        featureSets = [(self.getParagraphFeatures(d),label) for (d, label) in docs]
        firstThird = int(len(featureSets)/3)
        train, test = featureSets[:firstThird], featureSets[firstThird:]

        classifier = nltk.NaiveBayesClassifier.train(train)
        print(classifier.show_most_informative_features(20))
 
        return nltk.classify.accuracy(classifier,test)   

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
               
